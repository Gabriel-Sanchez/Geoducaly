

# Create your models here.
from django.db import models
from cursosLeccionesapp.models import Lesson, Grupo

import random

class test_True_false(models.Model):
    name = models.TextField()
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True,  blank=True)
    grupofk = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True,  blank=True)
    
    def get_preguntas_list(self, numero_preguntas):
        questions = list(self.preguntas_test_tf.all())
        random.shuffle(questions)
        return questions[:numero_preguntas]
    
    def get_preguntas(self, numero_preguntas):
        # preguntas_test = self.preguntas_test_tf.all().order_by('?')[:numero_preguntas]
        preguntas_test = self.preguntas_test_tf.all().order_by('?')
        
        total = preguntas_test.count()
        
        if numero_preguntas == 1:
            total_nivel = preguntas_test[:total//3]
        elif numero_preguntas == 2:
            total_nivel = preguntas_test[:total//2]
        elif numero_preguntas == 3:
            total_nivel = preguntas_test[:total]
        
        if len(total_nivel) == 0:
            total_nivel = preguntas_test[:1]
        return total_nivel
    
    def __str__(self):
        return self.name
    
    
class Pregunta(models.Model):
    texto = models.TextField()
    es_verdadera = models.BooleanField()
    imagen = models.ImageField(upload_to='preguntas/', blank=True, null=True)
    test_TF = models.ForeignKey(test_True_false, on_delete=models.SET_NULL, null=True, related_name='preguntas_test_tf')

    def __str__(self):
        return self.texto

    