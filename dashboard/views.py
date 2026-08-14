from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
import hashlib
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.core.paginator import Paginator
from .models import ParametresPlateforme
from resources.forms import DocumentForm
from settings_app.models import PlatformSettings
from settings_app.forms import PlatformSettingsForm
from accounts.models import User
from resources.models import Document, Comment, calculate_file_hash
from categories.models import Matiere, Niveau
from django.db.models import Q

@staff_member_required
def dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Accès interdit")
        
    derniers_utilisateurs = (
    User.objects
    .order_by("-date_joined")[:8]
)
    derniers_documents = (
        Document.objects
        .filter(status="approved")
        .select_related("auteur", "matiere", "niveau")
        .order_by("-created_at")[:10]
    )
    context = {
        "nb_users": User.objects.count(),
        "nb_documents": Document.objects.count(),
        "nb_comments": Comment.objects.count(),
        "nb_teachers": User.objects.filter(role="teacher").count(),
        "nb_students": User.objects.filter(role="student").count(),
        "nb_matieres": Matiere.objects.count(),
        "nb_niveaux": Niveau.objects.count(),
        "derniers_utilisateurs": derniers_utilisateurs,
        "derniers_documents": derniers_documents,
    }
    return render(request, "dashboard/dashboard.html", context)

@staff_member_required
def documents(request):
    documents = (
        Document.objects
        .select_related("auteur", "matiere", "niveau")
        .order_by("-created_at")
    )
    q = request.GET.get("q", "").strip()
    matiere = request.GET.get("matiere", "")
    niveau = request.GET.get("niveau", "")
    if q:
        documents = documents.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(auteur__username__icontains=q) |
            Q(auteur__first_name__icontains=q) |
            Q(auteur__last_name__icontains=q)
        )
    if matiere and matiere != "all":
        documents = documents.filter(
            matiere_id=matiere
        )
    if niveau and niveau != "all":
        documents = documents.filter(
            niveau_id=niveau
        )
    if q:
        documents = documents.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(auteur__username__icontains=q)
        )
    if matiere and matiere != "all":
        documents = documents.filter(matiere_id=int(matiere))
    if niveau and niveau != "all":
        documents = documents.filter(niveau_id=int(niveau))
    paginator = Paginator(documents, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "documents": page_obj,
        "page_obj": page_obj,
        "matieres": Matiere.objects.all(),
        "niveaux": Niveau.objects.all(),
    }

    return render( request, "dashboard/documents.html", context)

@staff_member_required
def utilisateurs(request):
    recent_utilisateurs = User.objects.order_by("-date_joined")[:10]

    context = {
        "total_utilisateurs": User.objects.count(),
        "recent_utilisateurs": recent_utilisateurs,
    }

    return render(
        request,
        "dashboard/utilisateurs.html",
        context,
    )

@staff_member_required
def matieres(request):
    recent_matieres = Matiere.objects.order_by("-id")[:10]

    context = {
        "total_matieres": Matiere.objects.count(),
        "recent_matieres": recent_matieres,
    }

    return render(
        request,
        "dashboard/matieres.html",
        context,
    )

@staff_member_required
def niveaux(request):
    context = {
        "nb_niveaux": Niveau.objects.count(),
        "derniers_niveaux": Niveau.objects.order_by("-id")[:10],
    }

    return render(
        request,
        "dashboard/niveaux.html",
        context,
    )

@staff_member_required
def commentaires(request):
    commentaires = (
        Comment.objects
        .select_related("auteur", "document")
        .order_by("-created_at")
    )
    return render(
        request,
        "dashboard/commentaires.html",
        {"commentaires": commentaires},
    )


@staff_member_required
def parametres(request):
    settings = PlatformSettings.get_solo()
    if request.method == "POST":
        form = PlatformSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request,"Les paramètres ont été enregistrés avec succès.")
            return redirect("dashboard_parametres")
    else:
        form = PlatformSettingsForm(
            instance=settings
        )
    context = {
        "page_title": "Paramètres de la plateforme",
        "form": form,
    }

    return render(
        request,
        "dashboard/parametres.html",
        context
    )

@staff_member_required
def document_create(request):
    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            document = form.save(commit=False)
            if document.file:
                hash_fichier = calculate_file_hash(document.file)
                doublon = Document.objects.filter(file_hash=hash_fichier).exists()
                if doublon:
                    messages.error( request, "Ce document existe déjà sur la plateforme.")
                    return render( request, "dashboard/document_form.html", { "form": form, "action": "Ajouter"})
                document.file_hash = hash_fichier
            document.save()
            form.save_m2m()
            messages.success( request, "Document ajouté avec succès." )
            return redirect("dashboard_documents")
    else:
        form = DocumentForm()
    return render( request,"dashboard/document_form.html",{"form": form,"action": "Ajouter"}
    )
@staff_member_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document
        )
        if form.is_valid():
            form.save()
            return redirect("dashboard_documents")
    else:
        form = DocumentForm(instance=document)
    return render(
        request,
        "dashboard/document_form.html",
        {
            "form": form,
            "titre": "Modifier un document"
        }
    )
@staff_member_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        document.delete()
        return redirect("dashboard_documents")

    return render(
        request,
        "dashboard/document_confirm_delete.html",
        {
            "document": document,
        }
    )
@staff_member_required
def document_approve(request, pk):
    document = get_object_or_404(Document, pk=pk)

    document.status = "approved"
    document.save(update_fields=["status"])

    return redirect("dashboard_documents")


@staff_member_required
def document_reject(request, pk):
    document = get_object_or_404(Document, pk=pk)

    document.status = "rejected"
    document.save(update_fields=["status"])

    return redirect("dashboard_documents")
    

@staff_member_required
def commentaires(request):
    context = {
        "nb_commentaires": Comment.objects.count(),
        "derniers_commentaires": Comment.objects.order_by("-created_at")[:10],
    }

    return render(
        request,
        "dashboard/commentaires.html",
        context,
    )

class ChangerMotDePasseView(PasswordChangeView):
    template_name = "dashboard/changer_mot_de_passe.html"
    success_url = reverse_lazy("password_change_done")


class ChangementMotDePasseEffectueView(PasswordChangeDoneView):
    template_name = "dashboard/password_change_done.html"