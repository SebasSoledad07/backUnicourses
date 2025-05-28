
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
class Interest(models.Model):
    name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest)

    def __str__(self):
        return self.name
