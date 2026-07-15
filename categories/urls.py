from django.urls import path

from .views import (
    MatiereDashboardView,
    MatiereListView,
    MatiereCreateView,
    MatiereUpdateView,
    MatiereDeleteView,

    NiveauListView,
    NiveauDetailView,
    NiveauCreateView,
    NiveauUpdateView,
    NiveauDeleteView,
)

app_name = "categories"
urlpatterns = [
    path("dashboard/", MatiereDashboardView.as_view(),name="matiere_dashboard",),
    path("", MatiereListView.as_view(), name="matiere_list", ),
    path("ajouter/", MatiereCreateView.as_view(), name="matiere_add",),
    path("<int:pk>/modifier/", MatiereUpdateView.as_view(),name="matiere_edit",),
    path("<int:pk>/supprimer/", MatiereDeleteView.as_view(), name="matiere_delete",),
    path("niveaux/",NiveauListView.as_view(), name="niveau_list", ),
    path("niveaux/ajouter/",NiveauCreateView.as_view(),name="niveau_add", ),
    path("niveaux/<int:pk>/",NiveauDetailView.as_view(),name="niveau_detail",),
    path( "niveaux/<int:pk>/modifier/",  NiveauUpdateView.as_view(),  name="niveau_update",),
    path("niveaux/<int:pk>/supprimer/",NiveauDeleteView.as_view(), name="niveau_delete", ),

]