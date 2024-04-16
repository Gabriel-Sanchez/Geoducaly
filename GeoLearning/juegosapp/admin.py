from django.contrib import admin
from django.db import models
from nested_admin import NestedStackedInline, NestedModelAdmin
from django import forms

# Register your models here.

from .models import ijuegos, Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario, ListQuiz, UserNumQuiz, Country, CardPar, Lesson_cards
# Register your models here.

from .forms import ElegirInlineFormset

admin.site.register(ijuegos)


class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    # can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTAS
    min_num = ElegirRespuesta.MAXIMO_RESPUESTAS
    formset = ElegirInlineFormset

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline,)
    list_display = ['texto','listquiz']
    search_fields = ['text', 'preguntas__texto']

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas

class ListQuizAdmin(admin.ModelAdmin):
    list_display = ['titulo','leccion']


admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)
# admin.site.register(ListQuiz,ListQuizAdmin)
admin.site.register(UserNumQuiz)


admin.site.register(PreguntasRespondidas)

admin.site.register(Country)
admin.site.register(CardPar)
# admin.site.register(Lesson_cards)


class CardParInline(admin.TabularInline):
    model = CardPar

class lesson_cards_Admin(admin.ModelAdmin):
    inlines = [CardParInline]
    list_filter = ('leccion',)
    list_display = ('name','leccion')

admin.site.register(Lesson_cards, lesson_cards_Admin)


class ElegirRespuestaForm(forms.ModelForm):
    
    texto = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 2}))
    class Meta:
        model = ElegirRespuesta
        fields = ('texto', 'correcta','pregunta') 
    
    class Media:
        css = {
            'all': ('GeoLearning/GBcss/adming.css',)  # Indica la ubicación de tu archivo CSS
        }


class ElegirRespuestaInline(NestedStackedInline):
    model = ElegirRespuesta
    extra = 4  # Cuántos campos de respuesta mostrar por defecto
    formset = ElegirInlineFormset
    form = ElegirRespuestaForm

class PreguntaInline(NestedStackedInline):
    model = Pregunta
    inlines = [ElegirRespuestaInline]
    extra = 1  # Cuántas preguntas mostrar por defecto

class ListQuizAdmin(NestedModelAdmin):
    inlines = [PreguntaInline]
    list_display = ['titulo','leccion']

admin.site.register(ListQuiz, ListQuizAdmin)