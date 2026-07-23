from django import forms
from .models import Document, Comment


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'matiere', 'niveau']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'matiere': forms.Select(attrs={
                'class': 'form-select'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Écrivez votre commentaire...'
                }
            )
        }