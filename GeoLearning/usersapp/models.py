from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    alt = models.TextField(blank=True)
    total_score_perfect = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)

    picture = models.ImageField(
        upload_to = "userimage",
        blank= True, null= True


    )
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    alt = models.TextField(blank=True)

    picture = models.ImageField(
        upload_to = "Profimage",
        blank= True, null= True


    )
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username