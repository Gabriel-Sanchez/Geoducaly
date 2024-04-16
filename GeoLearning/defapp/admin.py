from django.contrib import admin

# Register your models here.

from defapp.models import datos
# Register your models here.

class DatosAdmin(admin.ModelAdmin):
    list_filter = ('leccion',)
    save_as = True

admin.site.register(datos, DatosAdmin)

