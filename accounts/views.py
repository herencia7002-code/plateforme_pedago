from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.db.models import Count, Sum
from django.views.generic import TemplateView
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from resources.models import Document, Comment
from categories.models import Matiere, Niveau
from .forms import UserForm, UserUpdateForm
from resources.forms import DocumentForm

# Create your views here.

User = get_user_model()
class AdminRequiredMixin(UserPassesTestMixin):
    """Autorise uniquement les administrateurs."""

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == "admin"
        )

# Liste des utilisateurs

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 10
    ordering = ["last_name", "first_name"]

# Ajouter

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

# Modifier

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

# Supprimer

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("accounts:user_list")

# Activer/Désactiver

class ToggleUserStatusView(LoginRequiredMixin, AdminRequiredMixin, View):

    def post(self, request, pk):
        user = User.objects.get(pk=pk)

        # Empêcher la désactivation de son propre compte
        if user != request.user:
            user.is_active = not user.is_active
            user.save()

        return redirect("accounts:user_list")

class UserDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "dashboard/utilisateurs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_users"] = User.objects.count()
        context["total_admins"] = User.objects.filter(role="admin").count()
        context["total_teachers"] = User.objects.filter(role="teacher").count()
        context["total_students"] = User.objects.filter(role="student").count()
        context["recent_users"] = User.objects.order_by("-date_joined")[:10]

        return context
    
@login_required
def profil(request):
    return render(request, "accounts/profil.html", {"user": request.user })

@login_required
def user_dashboard(request):

    mes_documents = Document.objects.filter(auteur=request.user)
    nb_publications = mes_documents.count()
    nb_telechargements = mes_documents.aggregate( total=Sum("nb_telechargements"))["total"] or 0
    context = {
        "nb_publications": nb_publications,
        "nb_telechargements": nb_telechargements,
        "nb_commentaires": Comment.objects.filter( document__auteur=request.user).count(),
    }
    return render( request, "accounts/dashboard.html", context)

@login_required
def downloads(request):
    return render( request, "accounts/downloads.html", { "downloads": []} )

@login_required
def comments(request):
    commentaires = (
        Comment.objects
        .filter(auteur=request.user)
        .select_related("document")
        .order_by("-created_at")
    )
    return render(request, "accounts/comments.html",{ "commentaires": commentaires, },
    )

@login_required
def document_create(request):
    if request.user.role != "teacher":
        return HttpResponseForbidden( "Cette page est réservée aux enseignants." )
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.auteur = request.user
            document.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect("accounts:publications")
        else:
            print(form.errors)
    else:
        form = DocumentForm()
    return render( request, "accounts/document_form.html", {"form": form, "action": "Ajouter"},
    )

@login_required
def document_update(request, pk):
    
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document modifié avec succès.')
            return redirect('accounts:publications')
        else:
            print(form.errors)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'accounts/document_form.html', {'form': form, 'action': 'Modifier', 'document': document})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('accounts:publications')
    return render(request, 'accounts/document_confirm_delete.html', {'document': document})


@login_required
def publications(request):
    if request.user.role != "teacher":
        return HttpResponseForbidden(
            "Cette page est réservée aux enseignants."
        )
    documents = (
        Document.objects
        .filter(auteur=request.user)
        .select_related("matiere", "niveau")
        .order_by("-created_at")
    )
    return render( request, "accounts/publications.html", { "documents": documents,},
    )

@login_required
def parametres(request):
    return render(request,"accounts/parametres.html", { "user": request.user,},
    )
