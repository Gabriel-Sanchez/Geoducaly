from django.db import models

from django.urls import reverse
from embed_video.fields import EmbedVideoField
from cursosLeccionesapp.models import course, Lesson


# Create your models here.

class datos(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(max_length=120)
    position = models.IntegerField(blank=True, null=True)
    video_url = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to='datos', blank=True, null=True)
    description = models.TextField(blank=True)
    alt = models.TextField(blank=True)
    #course = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.title
