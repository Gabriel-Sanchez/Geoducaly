from django.contrib import admin

# Register your models here.

from .models import course, Lesson, Comment, Question, Answer,Quiz,Result, parrafoLeccion, Grupo, GrupoNotas, GrupoEstudiante

admin.site.register(Quiz)
# admin.site.register(Result)

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

admin.site.register(course)
# admin.site.register(Lesson)
admin.site.register(Comment)
# admin.site.register(clase)
admin.site.register(parrafoLeccion)
admin.site.register(Grupo)
admin.site.register(GrupoEstudiante)
admin.site.register(GrupoNotas)









from ckeditor.widgets import CKEditorWidget
from django.db import models
from django import forms

# class LessonAdmin(admin.ModelAdmin):
#     ['slug', 'title', 'course', 'position']

#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget},  # Configura RichTextField con CKEditor
#     }
    
#     list_filter = ('course',)

# admin.site.register(Lesson, LessonAdmin)

# # @admin.register(Lesson)
# # class LessonAdminF(admin.ModelAdmin):
# #     list_filter = ('course',)

class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['slug', 'title', 'course', 'position', 'video_url', 'thumbnail', 'video_e', 'description', 'content', 'ejercicio', 'alt', 'contentenido', 'mostrar', 'color']

        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),  # Utiliza un input de tipo 'color' para el campo de color
            'content': CKEditorWidget(),  # Configura RichTextField con CKEditor
            'description': CKEditorWidget(),  # Configura RichTextField con CKEditor
            'contentenido': CKEditorWidget(),  # Configura RichTextField con CKEditor
        }

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_filter = ('course','mostrar')
    list_display = ('id','title', 'color','mostrar')



@admin.register(Result)
class MiModeloAdmin(admin.ModelAdmin):

    list_display = ('id','quiz', 'user', 'score')
    list_editable = ( 'user', 'score')
    list_display_links = ('quiz',)