from django import forms
from resources.models import Document


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = [
            "title",
            "description",
            "file",
            "auteur",
            "matiere",
            "niveau",
            "tags",
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
            "tags": forms.SelectMultiple(attrs={
                "class": "form-select"
            }),
        }