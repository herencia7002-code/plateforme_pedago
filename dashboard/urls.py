from django.urls import path
from accounts.views import UserDashboardView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("documents/", views.documents, name="dashboard_documents"),
    path("utilisateurs/",UserDashboardView.as_view(),name="dashboard_utilisateurs"),
    path("matieres/", views.matieres, name="dashboard_matieres"),
    path("niveaux/", views.niveaux, name="dashboard_niveaux"),
    path("commentaires/", views.commentaires, name="dashboard_commentaires"),
    path("parametres/", views.parametres, name="dashboard_parametres"),
    path("documents/ajouter/", views.document_create, name="dashboard_document_create"),
    path("documents/<int:pk>/modifier/", views.document_update, name="dashboard_document_update"),
    path("documents/<int:pk>/supprimer/", views.document_delete, name="dashboard_document_delete"),
    path("documents/liste/", views.documents, name="dashboard_documents_list"),
    
]