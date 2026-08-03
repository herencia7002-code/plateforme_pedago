
from django.db import models

class PlatformSettings(models.Model):
    nom_plateforme = models.CharField(max_length=255, default="Plateforme pédagogique")
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)

    autoriser_inscriptions = models.BooleanField(default=True)
    validation_documents = models.BooleanField(default=True)
    autoriser_commentaires = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètres de la plateforme"

    def save(self, *args, **kwargs):
        self.pk = 1  
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Paramètres généraux"