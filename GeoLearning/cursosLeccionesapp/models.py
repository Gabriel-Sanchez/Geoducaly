

# Create your models here.

from django.db import models

from django.urls import reverse

from embed_video.fields import EmbedVideoField

from django.contrib.auth.models import User

from usersapp.models import Estudiante, Profesor
# Create your models here.
from ckeditor.fields import RichTextField

import random
import string


def generate_random_code():
    characters = string.ascii_letters + string.digits
    code_length = 8
    random_code = ''.join(random.choice(characters) for i in range(code_length))
    return random_code




class course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    miniatura = models.ImageField(upload_to='imgcouses')
    anio = models.CharField(max_length=120)
    alt = models.TextField(blank=True)



    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    @property
    def lessons(self):
        # return self.lesson_set.all().order_by('position')
        return self.lesson_set.filter(mostrar=True).order_by('position')
    
    

class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='lesson')
    video_e = EmbedVideoField()
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    ejercicio = models.CharField(max_length=100, blank=True)
    alt = models.TextField(blank=True)
    contentenido = RichTextField(blank=True)
    
    mostrar = models.BooleanField(verbose_name='mostrar leccion', default=False, null=False)
    color = models.CharField(max_length=7, default='#ffffff')




    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail', 
        kwargs={'course_slug': self.course.slug,
        'lesson_slug':self.slug
        })


class parrafoLeccion(models.Model):
    Nposition = models.IntegerField()
    leccion = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    contenido = models.TextField(blank=True)
    imagen = models.ImageField(upload_to = "LessonImages",blank= True, null= True)
    alt = models.TextField(blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lessson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username
    

    

import random

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)
class Grupo(models.Model):    
    name = models.CharField(max_length=120)
    course = models.ForeignKey(course, on_delete=models.CASCADE, blank= True, null=True)
    # estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    privado = models.BooleanField(default=False)
    imagen_grupo = models.ImageField(upload_to = "images_groups",blank= True)
    codigo_unico = models.CharField(max_length=8, default=generate_random_code, unique=True, blank=True)
    
    def __str__(self):
        # return str(self.course) + str(self.name)
        return str(self.name)

    def get_absolute_url(self):
        return reverse('view_grupo_general', 
        kwargs={'id_grupo': self.id
        })

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    lessson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    fk_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    n_orden = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
    
    
    
class GrupoNotas(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nota = models.ForeignKey(Result, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.nota.user) +  str(self.nota.score) + str(self.nota.quiz) + str(self.grupo)
    
class GrupoEstudiante(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.estudiante) + str(self.grupo)
        
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    fk_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fk_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name) 

class TaskScore(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.task.name} - {self.estudiante.name}: {self.score}"