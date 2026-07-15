from django.urls import path

from .views import (
    CommentListView,
    CommentDetailView,
    CommentDeleteView,
)

app_name = "comments"

urlpatterns = [

    path(
        "",
        CommentListView.as_view(),
        name="comment_list",
    ),

    path(
        "<int:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),

    path(
        "<int:pk>/supprimer/",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),

]