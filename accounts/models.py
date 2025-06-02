from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# accounts/models.py

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Estudiante'),
        ('admin', 'Administrador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    interests = models.ManyToManyField('Interest', blank=True)
    career = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.role}"

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
