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
)

app_name = "accounts"
urlpatterns = [
    path( "users/", UserListView.as_view(),name="user_list" ),
    path( "users/add/", UserCreateView.as_view(), name="user_add" ),
    path( "users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit" ),
    path( "users/<int:pk>/delete/", UserDeleteView.as_view(),name="user_delete"),
    path( "users/<int:pk>/toggle/", ToggleUserStatusView.as_view(), name="user_toggle"),
    path( "utilisateurs/",UserDashboardView.as_view(), name="admin_users_dashboard"),
    path( "logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path( "dashboard/", user_dashboard, name="user_dashboard"),
    path( "profil/", profil, name="profil"),
    path( "downloads/", downloads, name="downloads"),
    path( "comments/", comments, name="comments"),
    path( "publications/", publications,name="publications"),
    path( "parametres/",parametres, name="parametres"),

]