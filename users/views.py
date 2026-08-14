from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import UserRegisterForm
from settings_app.models import PlatformSettings
from categories.models import Matiere, Niveau
from django.shortcuts import redirect, render
from django.db.models import Q
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
    recherche = request.GET.get("q", "").strip()
    niveau_filtre = request.GET.get('niveau', '').strip()
    matiere_filtre = request.GET.get('matiere', '').strip()

    documents = (
        Document.objects
        .filter(status="approved")
        .select_related("auteur", "matiere", "niveau")
        .order_by("-created_at")
    )
    documents = Document.objects.filter(type_ressource="cours",status="approved")
    type_filtre = request.GET.get("type")

    if type_filtre:
        documents = documents.filter(type_ressource=type_filtre)
    if recherche:
        documents = documents.filter(
            Q(title__icontains=recherche) |
            Q(description__icontains=recherche) |
            Q(matiere__nom__icontains=recherche) |
            Q(niveau__nom__icontains=recherche) |
            Q(auteur__username__icontains=recherche) |
            Q(auteur__first_name__icontains=recherche) |
            Q(auteur__last_name__icontains=recherche)
        )
    if matiere_filtre:
        documents = documents.filter(
            matiere__nom=matiere_filtre
        )

    if niveau_filtre:
        documents = documents.filter(
            niveau__nom=niveau_filtre
        )

    if type_filtre:
        documents = documents.filter(
            type_ressource=type_filtre
        )

    matieres = Matiere.objects.all()
    niveaux = Niveau.objects.all()
    types_ressources = [
        "Cours",
        "Exercices",
        "Fiches pédagogiques"
    ]
    context = {
        "documents": documents,
        "matieres": matieres,
        "niveaux": niveaux,
        "types_ressources": types_ressources,
    }
    return render( request, "index.html", context
    )
def redirect_after_login(user):
    if user.role == "admin":
        return redirect("dashboard")

    return redirect("accounts:user_dashboard")


def inscription(request):
    settings = PlatformSettings.get_solo()
    if not settings.autoriser_inscriptions:
        messages.error(request,"Les inscriptions sont actuellement désactivées.")
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_after_login(user)
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
                return redirect_after_login(user)
            form.add_error(None, 'Email ou mot de passe incorrect.')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'connexion.html', {'form': form})


def profil(request):
    return render(request, 'profil.html', {'user': request.user})