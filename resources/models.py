from django.conf import settings
from django.db import models
from django.db.models import F


class Document(models.Model): 
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
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
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
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
