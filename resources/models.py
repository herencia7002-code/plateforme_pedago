from django.conf import settings
from django.db import models
import hashlib
from django.db.models import F


class Document(models.Model): 
      
    TYPE_RESSOURCE_CHOICES = [
    ("cours", "Cours"),
    ("exercices", "Exercices"),
    ("annales", "Annales"),
    ("annales_sujet_corriges", "Annales avec sujets et corrigés"),
    ("fiche_pedagogique", "Fiche pédagogique"),
]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    type_ressource = models.CharField(
    max_length=30,
    choices=TYPE_RESSOURCE_CHOICES,
    verbose_name="Type de ressource",
                )
    auteur  = models.ForeignKey(
                  settings.AUTH_USER_MODEL,
                  on_delete=models.PROTECT,
                  verbose_name='Auteur'
              )
    niveau  = models.ForeignKey(
                  'categories.Niveau',
                  on_delete=models.PROTECT,
                  verbose_name='Niveau'
              )
    matiere = models.ForeignKey(
                  'categories.Matiere',
                  on_delete=models.PROTECT,
                  verbose_name='Matière'
              )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nb_telechargements = models.PositiveIntegerField(
        default=0,
        verbose_name="Téléchargements"
)
    
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("approved", "Validé"),
        ("rejected", "Refusé"),
]

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
)
    
    file_hash = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        editable=False
)

    class Meta:
        verbose_name        = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def incrementer_telechargements(self):
        self.nb_telechargements = F("nb_telechargements") + 1
        self.save(update_fields=["nb_telechargements"])
        self.refresh_from_db()
    
    def save(self, *args, **kwargs):
        if self.file:
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.file_hash = sha256.hexdigest()
            self.file.seek(0)
        super().save(*args, **kwargs)
        
def calculate_file_hash(file):
    sha256 = hashlib.sha256()

    for chunk in file.chunks():
        sha256.update(chunk)

    file.seek(0)

    return sha256.hexdigest()

class Comment(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField("Commentaire")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.auteur.username} - {self.document.title}"

