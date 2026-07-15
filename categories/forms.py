from django import forms
from .models import Matiere, Niveau


class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = "__all__"

class NiveauForm(forms.ModelForm):
    class Meta:
        model = Niveau
        fields = "__all__"
        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nom du niveau"
                }
            ),
        }