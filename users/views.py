from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import UserRegisterForm
from django.shortcuts import redirect, render
from resources.models import Document

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre adresse e-mail"
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre mot de passe"
        })
    )

def home(request):
    documents = Document.objects.select_related("auteur", "matiere", "niveau"
    ).order_by("-created_at")
    return render(request,"index.html",{    "documents": documents}
    )


def inscription(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profil")
    else:
        form = UserRegisterForm()

    return render(request, "inscription.html", {"form": form})

def connexion(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user_model = get_user_model()
            user = user_model.objects.filter(email__iexact=email).first()
            if user is not None and user.check_password(password):
                login(request, user)
                return redirect('profil')
            form.add_error(None, 'Email ou mot de passe incorrect.')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'connexion.html', {'form': form})


def profil(request):
    return render(request, 'profil.html', {'user': request.user})
