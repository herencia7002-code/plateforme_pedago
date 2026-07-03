from django.urls import path
from .views import (
    document_list,
    document_create,
    document_update,
    document_delete,
)

urlpatterns = [
    path('', document_list, name='document_list'),
    path('ajouter/', document_create, name='document_create'),
    path('modifier/<int:pk>/', document_update, name='document_update'),
    path('supprimer/<int:pk>/', document_delete, name='document_delete'),
]
