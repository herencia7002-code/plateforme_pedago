from django.contrib import admin
from .models import Document
from .models import Ressource
from .models import Comment
from .models import Tag
from .models import Rating

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'matiere', 'niveau', 'auteur', 'uploaded_by', 'created_at',)
    search_fields = ('title', 'description', 'auteur__username',)
    list_filter = ('created_at', 'niveau', 'matiere',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
  

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre','matiere', 'niveau', 'auteur', 'type_document', 'is_approved', 'nb_telechargements', 'created_at' )
    list_filter = ( 'is_approved','matiere', 'niveau', 'type_document')
    search_fields = ('titre', 'description', 'auteur__username')
    ordering = ('-created_at',)
    list_editable = ('is_approved',)
    readonly_fields = ('nb_telechargements', 'created_at',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'fichier', 'type_document')
        }),
        ('Catégorisation', {
            'fields': ('matiere', 'niveau', 'auteur')
        }),
        ('Statut & statistiques', {
            'fields': ('is_approved', 'nb_telechargements', 'created_at')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'document', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "document", "stars")
