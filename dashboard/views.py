from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


from accounts.models import User
from resources.models import Document, Comment
from categories.models import Matiere, Niveau

@staff_member_required
def dashboard(request):

    derniers_utilisateurs = (
    User.objects
    .order_by("-date_joined")[:8]
)
    derniers_documents = (
        Document.objects
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