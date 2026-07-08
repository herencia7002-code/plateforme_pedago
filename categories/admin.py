from django.contrib import admin
from .models import Niveau, Matiere


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ("nom", "niveau")
    list_filter = ("niveau",)
    search_fields = ("nom",)