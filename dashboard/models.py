from django.db import models


class ParametresPlateforme(models.Model):
    nom_plateforme = models.CharField(
        max_length=200,
        default="Plateforme pédagogique"
    )

    email = models.EmailField(
        blank=True,
        default=""
    )

    telephone = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    autoriser_inscriptions = models.BooleanField(
        default=True
    )

    validation_documents = models.BooleanField(
        default=True
    )

    autoriser_commentaires = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Paramètres de la plateforme"
        verbose_name_plural = "Paramètres de la plateforme"

    def __str__(self):
        return self.nom_plateforme