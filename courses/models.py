from django.db import models
from accounts.models import Interest

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    career = models.CharField(max_length=100, verbose_name="Carrera")
    description = models.TextField(verbose_name="Descripción")
    interests = models.ManyToManyField(Interest, related_name='courses', verbose_name="Intereses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.career}"
