from django import forms
from resources.models import Document
from .models import ParametresPlateforme


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = [
            'title',
            'description',
            'file',
            'auteur',
            'matiere',
            'niveau',
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),

            "file": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "auteur": forms.Select(attrs={
                "class": "form-select"
            }),

            "matiere": forms.Select(attrs={
                "class": "form-select"
            }),

            "niveau": forms.Select(attrs={
                "class": "form-select"
            }),
        }


class ParametresForm(forms.ModelForm):

    class Meta:
        model = ParametresPlateforme

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
                "placeholder": "Numéro de téléphone",
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