from django.contrib import admin

# Register your models here.

from ciertoFalsoapp.models import Pregunta, test_True_false


admin.site.register(Pregunta)

class PreguntaInline(admin.TabularInline):
    model = Pregunta

class Test_True_falseAdmin(admin.ModelAdmin):
    inlines = [PreguntaInline]
    list_display = ('name','leccion')

admin.site.register(test_True_false, Test_True_falseAdmin)