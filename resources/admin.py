from django.contrib import admin
from .models import Document, Comment

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "matiere", "niveau", "auteur", "status", "nb_telechargements","created_at")
    search_fields = ("title", "description", "auteur__username",)
    list_filter = ( "status","matiere","niveau","created_at")
    ordering = ("-created_at",)
    list_editable = ("status" , )
    readonly_fields = ("nb_telechargements","created_at","updated_at",)
    fieldsets = (
        ("Informations générales", {"fields": ("title","description", "file" )}),
        ("Catégorisation", { "fields": ( "matiere", "niveau", "auteur")}),
        ("Validation", { "fields": ( "status",)}),
        ("Statistiques", {"fields": ( "nb_telechargements", "created_at", "updated_at")}),
    )
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'document', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('auteur__username', 'content',)

