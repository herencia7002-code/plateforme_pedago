from django.contrib import admin
from .models import Niveau, Matiere


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom", "description")


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ("nom","description")
    search_fields = ("nom","description")