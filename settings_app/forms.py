from django import forms
from .models import PlatformSettings


class PlatformSettingsForm(forms.ModelForm):

    class Meta:
        model = PlatformSettings

        fields = [
            "nom_plateforme",
            "email",
            "telephone",
            "autoriser_inscriptions",
            "validation_documents",
            "autoriser_commentaires",
        ]

        widgets = {
            "nom_plateforme": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de la plateforme",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Adresse email",
            }),

            "telephone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Téléphone",
            }),

            "autoriser_inscriptions": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),

            "validation_documents": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),

            "autoriser_commentaires": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }