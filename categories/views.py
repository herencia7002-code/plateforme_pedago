from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Matiere
from .forms import MatiereForm
from .models import Niveau
from .forms import NiveauForm

# Create your views here.

class MatiereDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/matieres.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_matieres"] = Matiere.objects.count()
        context["recent_matieres"] = Matiere.objects.order_by("-id")[:5]

        return context

class MatiereListView(LoginRequiredMixin, ListView):
    model = Matiere
    template_name = "categories/matiere_list.html"
    context_object_name = "matieres"
    paginate_by = 10
    ordering = ["nom"]

    def get_queryset(self):
        queryset = Matiere.objects.all().order_by("nom")

        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(
                Q(nom__icontains=q)
            )

        return queryset

class MatiereCreateView(LoginRequiredMixin, CreateView):
    model = Matiere
    form_class = MatiereForm
    template_name = "categories/matiere_form.html"
    success_url = reverse_lazy("categories:matiere_list")

class MatiereUpdateView(LoginRequiredMixin, UpdateView):
    model = Matiere
    form_class = MatiereForm
    template_name = "categories/matiere_form.html"
    success_url = reverse_lazy("categories:matiere_list")

class MatiereDeleteView(LoginRequiredMixin, DeleteView):
    model = Matiere
    template_name = "categories/matiere_confirm_delete.html"
    success_url = reverse_lazy("categories:matiere_list")

def dashboard_matieres(request):
    matieres = Matiere.objects.all().order_by("nom")
    context = {
        "matieres": matieres,
        "nb_matieres": matieres.count(),
    }
    return render(
        request,
        "dashboard/matieres.html",
        context,
    )

class NiveauListView(ListView):
    model = Niveau
    template_name = "categories/niveau_list.html"
    context_object_name = "niveaux"
    paginate_by = 10

    def get_queryset(self):
        queryset = Niveau.objects.all().order_by("nom")

        recherche = self.request.GET.get("q")

        if recherche:
            queryset = queryset.filter(
                Q(nom__icontains=recherche)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recherche"] = self.request.GET.get("q", "")
        context["nb_niveaux"] = Niveau.objects.count()

        return context
class NiveauCreateView(CreateView):
    model = Niveau
    form_class = NiveauForm
    template_name = "categories/niveau_form.html"
    success_url = reverse_lazy("categories:niveau_list")

class NiveauUpdateView(UpdateView):
    model = Niveau
    form_class = NiveauForm
    template_name = "categories/niveau_form.html"
    success_url = reverse_lazy("categories:niveau_list")

class NiveauDetailView(DetailView):
    model = Niveau
    template_name = "categories/niveau_detail.html"
    context_object_name = "niveau"

class NiveauDeleteView(DeleteView):
    model = Niveau
    template_name = "categories/niveau_confirm_delete.html"
    success_url = reverse_lazy("categories:niveau_list")

