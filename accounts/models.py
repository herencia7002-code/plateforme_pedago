from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# accounts/models.py

class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Enseignant'),
        ('student', 'Elève'),
        ('admin', 'Administrateur'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    school = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == "student"

    def is_admin(self):
        return self.role == "admin"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
