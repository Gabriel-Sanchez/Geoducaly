# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class CategoriaForo(models.Model):
    name = models.CharField(max_length=100)
    

class Hilo(models.Model):
    category = models.ForeignKey(CategoriaForo, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    

class MensajeForo(models.Model):
    hilo = models.ForeignKey(Hilo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    
