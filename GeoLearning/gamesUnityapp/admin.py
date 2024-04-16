from django.contrib import admin
from .models import Juegos_lesson, Score_juegos_lesson, HistorialExperiencia
# Register your models here.

class Score_juegos_lessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'estudiante', 'juego_lesson' )
class juegos_lessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruta_juego', 'lesson' )

admin.site.register(Juegos_lesson, juegos_lessonAdmin)
admin.site.register(Score_juegos_lesson, Score_juegos_lessonAdmin)
admin.site.register(HistorialExperiencia)