from django.urls import path
from .views import (
    document_list,
    document_create,
    document_update,
    document_delete,
    add_comment,
    download_document,
)

urlpatterns = [
    path('', document_list, name='document_list'),
    path('ajouter/', document_create, name='document_create'),
    path('modifier/<int:pk>/', document_update, name='document_update'),
    path('supprimer/<int:pk>/', document_delete, name='document_delete'),
    path('documents/<int:pk>/comment/', add_comment, name='add_comment'),
    path('documents/<int:pk>/download/',download_document,name="download_document",),
]

