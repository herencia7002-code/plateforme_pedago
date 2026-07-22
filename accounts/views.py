from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 10
    ordering = ["last_name", "first_name"]

# Ajouter

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

# Modifier

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

# Supprimer

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
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
    return render(request, "users/profil.html", {"user": request.user })

@login_required
def user_dashboard(request):

    context = {
        "nb_publications": 0,
        "nb_telechargements": 0,
        "nb_commentaires": 0,
        "nb_vues": 0,
        "nb_consultations": 0,
    }
    return render( request, "accounts/dashboard.html", context)

@login_required
def downloads(request):
    return render( request, "accounts/mes_telechargements.html", { "downloads": []} )

@login_required
def comments(request):
    commentaires = (
        Comment.objects
        .filter(auteur=request.user)
        .select_related("document")
        .order_by("-created_at")
    )
    return render(request, "accounts/mes_commentaires.html",{ "commentaires": commentaires, },
    )

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
    return render( request, "accounts/mes_publications.html", { "documents": documents,},
    )

@login_required
def parametres(request):
    return render(request,"accounts/parametres.html", { "user": request.user,},
    )
