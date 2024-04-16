from django.db import models

from cursosLeccionesapp.models import Lesson, Grupo
from usersapp.models import Estudiante
from ckeditor.fields import RichTextField

# Create your models here.

    

class Juegos_lesson(models.Model):
    ruta_juego = models.TextField(blank=True)
    nombre_juego = models.TextField(blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    instrucciones = RichTextField(blank=True)
    score_max = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.ruta_juego
    
class Score_juegos_lesson(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    juego_lesson = models.ForeignKey(Juegos_lesson, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    score_perfecto = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.score) 
    
    def serialize(self):
        return {
            'estudiante': str(self.estudiante),
            'juego_lesson': self.juego_lesson.id,
            'fecha': self.fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'score': str(self.score)
        }
class Score_juegos_Group(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    juego_group = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.score) 
    
    def serialize(self):
        return {
            'estudiante': str(self.estudiante),
            'juego_lesson': self.juego_lesson.id,
            'fecha': self.fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'score': str(self.score)
        }

class HistorialExperiencia(models.Model):
    fecha = models.DateField()
    puntos_obtenidos = models.IntegerField(blank=True, null=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

