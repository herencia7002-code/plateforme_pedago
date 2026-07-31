from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    ToggleUserStatusView,
    UserDashboardView,
    user_dashboard,
    profil,
    downloads,
    comments,
    publications,
    parametres,
    document_create,
    document_update,
    document_delete,
    documents_publies,
    modifier_profil,
    modifier_photo,
    ChangerMotDePasseView,
    ChangementMotDePasseEffectueView,
    
)

app_name = "accounts"
urlpatterns = [
    path( "users/", UserListView.as_view(),name="user_list" ),
    path( "users/add/", UserCreateView.as_view(), name="user_add" ),
    path( "users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit" ),
    path( "users/<int:pk>/delete/", UserDeleteView.as_view(),name="user_delete"),
    path( "users/<int:pk>/toggle/", ToggleUserStatusView.as_view(), name="user_toggle"),
    path( "utilisateurs/",UserDashboardView.as_view(), name="admin_users_dashboard"),
    path( "logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path( "dashboard/", user_dashboard, name="user_dashboard"),
    path( "profil/", profil, name="profil"),
    path( "downloads/", downloads, name="downloads"),
    path( "comments/", comments, name="comments"),
    path( "publications/", publications,name="publications"),
    path( "parametres/",parametres, name="parametres"),
    path( "documents/publier/", document_create, name="document_create"),
    path('modifier/<int:pk>/', document_update, name='document_update'),
    path('supprimer/<int:pk>/', document_delete, name='document_delete'),
    path("documents/", documents_publies,name="documents_publies",),
    path("profil/modifier/", modifier_profil, name="modifier_profil"),
    path("photo/modifier/", modifier_photo, name="modifier_photo"),
    path("mot-de-passe/", ChangerMotDePasseView.as_view(),name="password_change",),
    path("mot-de-passe/succes/", ChangementMotDePasseEffectueView.as_view(), name="password_change_done",),

]