from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [('teacher', 'Enseignant'), ('student', 'Élève'), ('admin', 'Admin')]
    role     = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    school   = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField('categories.Subject', blank=True)

