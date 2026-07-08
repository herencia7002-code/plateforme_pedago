from django.db import models


class Niveau(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE,
        related_name="matieres"
    )

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ["nom"]

    def __str__(self):
        return self.nom