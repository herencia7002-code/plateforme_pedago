from django.urls import path
from . import views

urlpatterns = [
    path("parametres/", views.parametres_generaux, name="parametres_generaux"),
]