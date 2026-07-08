from django import forms
from .models import Document, Comment


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Titre du document'}),
            'description': forms.Textarea(attrs={'class': 'textarea-field', 'placeholder': 'Description du document', 'rows': 4}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'rows':4,
                'placeholder':"Écrivez votre commentaire..."
            })
        }