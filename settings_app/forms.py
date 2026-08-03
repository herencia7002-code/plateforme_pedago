from django import forms
from .models import PlatformSettings

class PlatformSettingsForm(forms.ModelForm):
    class Meta:
        model = PlatformSettings
        fields = [
            "nom_plateforme", "nom_etablissement", "email", "telephone",
            "autoriser_inscriptions", "validation_documents",
            "autoriser_commentaires", "mode_maintenance",
        ]
        widgets = {
            "nom_plateforme": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "autoriser_inscriptions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "validation_documents": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "autoriser_commentaires": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }