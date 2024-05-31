from django.db import models

from django.contrib.auth.models import User
from usersapp.models import Estudiante
from cursosLeccionesapp.models import course, Lesson, Grupo


import random

class Game(models.Model):
    name = models.CharField(max_length=100)
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    summary = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    

class Score(models.Model):
    student = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.

class ijuegos(models.Model):
    title = models.CharField(max_length=120)
    iframe = models.TextField(blank=True)
    type = models.IntegerField(blank=True)
    url = models.CharField(max_length=320)
    alt = models.TextField(blank=True)
    course = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)


    picture = models.ImageField(
    upload_to = "juegosimage",
    blank= True, null= True
    )
     

    def __str__(self):
        return self.title

class ListQuiz(models.Model):
    titulo = models.TextField(verbose_name='titulo del quiz')
    alt = models.TextField(blank=True)
    
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True , blank=True)
    grupofk = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)

    picture = models.ImageField(
    upload_to = "triviaImage",
    blank= True, null= True
    )
    
    
    
    def get_preguntas(self, numero_preguntas):
        # preguntas_test = self.preguntas_test_tf.all().order_by('?')[:numero_preguntas]
        preguntas_test = self.listquiz.all().order_by('?')
        
        total = preguntas_test.count()
        
        if numero_preguntas == 1:
            total_nivel = preguntas_test[:total//3]
        elif numero_preguntas == 2:
            total_nivel = preguntas_test[:total//2]
        elif numero_preguntas == 3:
            total_nivel = preguntas_test[:total]
        return total_nivel
    def __str__(self):
        return self.titulo
    

class UserNumQuiz(models.Model):
    usuario = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    listquiz = models.ForeignKey(ListQuiz, on_delete=models.CASCADE)
    Num_veces_jugadas = models.IntegerField(default=0, null=True)

class Pregunta(models.Model):
    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1

    listquiz = models.ForeignKey(ListQuiz, related_name='listquiz', on_delete=models.CASCADE)
    texto = models.TextField(verbose_name='texto de la pregunta')
    listquices = models.IntegerField(null=True)
    max_puntaje = models.DecimalField(verbose_name='maximo puntaje', default=1, decimal_places=2, max_digits=6)
    alt = models.TextField(blank=True)

    picture = models.ImageField(
    upload_to = "TriviaPreguntaimage",
    blank= True, null= True
    )
    
    
    def verificar_respuesta(self, respuesta_pk):
        valor_respuesta = self.opciones.get(id= respuesta_pk)
        return valor_respuesta
    
    def get_respuesta_correcta(self):
        respuestaCorrecta = self.opciones.get(correcta=True)
        return respuestaCorrecta

    def __str__(self):
        return self.texto


class ElegirRespuesta(models.Model):

    MAXIMO_RESPUESTAS = 4

    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='¿es esta la pregunta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='texto de la respuesta')

    def __str__(self):
        return self.texto

class QuizUsuario(models.Model):
    usuario = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje total', default=0, decimal_places=2, max_digits=10)
    Num_jugada = models.IntegerField(null=True)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def obtener_nuevas_preguntas(self,listquiz):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self ).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        preguntas_restantes = preguntas_restantes.filter(listquiz = listquiz)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)
    
    def validar_intento(self, pregunta_respondida, respuesta_selecionada):
        if pregunta_respondida.pregunta_id != respuesta_selecionada.pregunta_id:
            return
        pregunta_respondida.respuesta_selecionada = respuesta_selecionada
        if respuesta_selecionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_selecionada
        else:
            pregunta_respondida.respuesta = respuesta_selecionada

        pregunta_respondida.save()

        self.actualizar_puntaje()
    
    def actualizar_puntaje(self):
        puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
        if puntaje_actualizado:
            self.puntaje_total = puntaje_actualizado
            self.save()
        else:
            self.puntaje_total = 0
            self.save()



class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE,related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True )
    correcta = models.BooleanField(verbose_name='¿es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)


from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    image = models.ImageField(upload_to='country_images')



#gabo pareos


from django.db import models
from cursosLeccionesapp.models import Lesson

import random

class Lesson_cards(models.Model):
    name = models.TextField()
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    grupofk = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_cards_list(self, numero_preguntas):
        questions = list(self.cartas_de_leccion.all())
        random.shuffle(questions)
        return questions[:numero_preguntas]
    def get_cards_lend(self):
        number = self.cartas_de_leccion.all().count()
        return number
    
    def get_cards(self, numero_preguntas):
        # cards_lesson = self.preguntas_test_tf.all().order_by('?')[:numero_preguntas]
        cards_lesson = self.cartas_de_leccion.all().order_by('?')
        
        total = cards_lesson.count()
        
        if numero_preguntas == 1:
            total_nivel = cards_lesson[:total//3]
        elif numero_preguntas == 2 and total >= 3:
            total_nivel = cards_lesson[:3]
        elif numero_preguntas == 3:
            total_nivel = cards_lesson[:total]
        return total_nivel
    
    def __str__(self):
        return self.name

from django.db import models

class CardPar(models.Model):
    image = models.ImageField(upload_to='card_images')
    name = models.CharField(max_length=100)
    lesson_cards = models.ForeignKey(Lesson_cards, on_delete=models.SET_NULL, null=True, related_name='cartas_de_leccion')

    def __str__(self):
        return self.name


