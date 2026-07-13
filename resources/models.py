from django.conf import settings
from django.db import models
from django.db.models import Avg


class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents'
    )
    auteur  = models.ForeignKey(
                  settings.AUTH_USER_MODEL,
                  on_delete=models.SET_NULL,
                  null=True,
                  verbose_name='Auteur'
              )
    niveau  = models.ForeignKey(
                  'categories.Niveau',
                  on_delete=models.SET_NULL,
                  null=True,
                  verbose_name='Niveau'
              )
    matiere = models.ForeignKey(
                  'categories.Matiere',
                  on_delete=models.SET_NULL,
                  null=True,
                  verbose_name='Matière'
              )
    tags = models.ManyToManyField(
                'Tag',
                 blank=True,
                 related_name="documents"
)           

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nb_telechargements = models.PositiveIntegerField(default=0)
    @property
    def average_rating(self):
        return self.ratings.aggregate(
            Avg("stars")
        )["stars__avg"] or 0


    class Meta:
        verbose_name        = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Ressource(models.Model):
    TYPE_CHOICES = [
        ('cours',     'Cours'),
        ('exercice',  'Exercice'),
        ('fiche',     'Fiche pédagogique'),
        ('correction', 'Correction'),
    ]

    titre            = models.CharField(max_length=255, verbose_name='Titre')
    description      = models.TextField(verbose_name='Description')
    file             = models.FileField(
                           upload_to='resources/%Y/%m/',
                           max_length=100,
                           verbose_name='Fichier'
                       )
    type_document    = models.CharField(
                           max_length=20,
                           choices=TYPE_CHOICES,
                           default='cours',
                           verbose_name='Type de document'
                       )
    created_at = models.DateTimeField(
                           auto_now_add=True,
                           verbose_name='Date de publication'
                       )
    is_approved      = models.BooleanField(
                           default=False,
                           verbose_name='Approuvée'
                       )
    nb_telechargements = models.PositiveIntegerField(
                           default=0,
                           verbose_name='Téléchargements'
                       )
    auteur  = models.ForeignKey(
                  settings.AUTH_USER_MODEL,
                  on_delete=models.SET_NULL,
                  null=True,
                  related_name='ressources',
                  db_column='auteur_id',
                  verbose_name='Auteur'
              )
    niveau  = models.ForeignKey(
                  'categories.Niveau',
                  on_delete=models.SET_NULL,
                  null=True,
                  related_name='ressources',
                  db_column='niveau_id',
                  verbose_name='Niveau'
              )
    matiere = models.ForeignKey(
                  'categories.Matiere',
                  on_delete=models.SET_NULL,
                  null=True,
                  related_name='ressources',
                  db_column='matiere_id',
                  verbose_name='Matière'
              )

    class Meta:
        verbose_name        = 'Ressource'
        verbose_name_plural = 'Ressources'
        ordering            = ['-created_at']

    def __str__(self):
        return self.titre

    def incrementer_telechargements(self):
        self.nb_telechargements += 1
        self.save(update_fields=['nb_telechargements'])


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

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    stars = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("user", "document")

    def __str__(self):
        return f"{self.document.title} ({self.stars})"
