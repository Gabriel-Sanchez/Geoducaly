from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from gamesUnityapp.models import Juegos_lesson, Score_juegos_lesson, HistorialExperiencia
from django.db.models import Sum, F

from usersapp.models import Estudiante
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def tabla_puntuacion_list():
    try:
        estudiantes_con_suma = Score_juegos_lesson.objects.values('estudiante').annotate(total_score=Sum('score'))

        estudiantes = Estudiante.objects.filter(pk__in=[item['estudiante'] for item in estudiantes_con_suma])

        clasificacion = []
        for estudiante_con_suma in estudiantes_con_suma:
            estudiante = estudiantes.filter(pk=estudiante_con_suma['estudiante']).first()
            if estudiante:
                estudiante_con_suma['estudiante_obj'] = estudiante
                clasificacion.append(estudiante_con_suma)

        clasificacion = sorted(clasificacion, key=lambda x: x['total_score'], reverse=True)

        # clasificacion = Score_juegos_lesson.objects.all()
        # clasificacion = Score_juegos_lesson.objects.values(estudiante_obj=F('estudiante')).annotate(total_score=Sum('score')).order_by('-total_score')
    except Exception as error:
        clasificacion = []
    return clasificacion

@login_required
def score_table(request):
    clasificacion = tabla_puntuacion_list()

    
    print(clasificacion)
    context = {
        'clasificacion': clasificacion,
        'name_path_game': 'juegoprovincias',
        'es_general': True
    }
    return render(request, 'gamesUnityapp/score_table.html', context)


@ensure_csrf_cookie
def get_csrf_token(request):
    print('quiere token')
    return JsonResponse({'csrfToken': get_token(request)})


from django.http import JsonResponse


from datetime import date
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.core.serializers.json import DjangoJSONEncoder
import json

# importing the modules
from bokeh.plotting import figure, output_file, show
  


#@csrf_exempt
def post_data(request):
    print('quiereee post')
    if request.method == 'POST':
        print('entro al post de unity')
        score = request.POST.get('score')
        nombrejuego = request.POST.get('Nombrejuego')
        
        juego_leccion = Juegos_lesson.objects.filter(ruta_juego = nombrejuego)
        juego_leccion = juego_leccion.first()
        print(juego_leccion)
        
        if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
            print(nombrejuego+'-'+score)
            nombre_estudiante = request.user.estudiante
            print(nombre_estudiante)
            obj_score, created = Score_juegos_lesson.objects.get_or_create(juego_lesson = juego_leccion, estudiante = nombre_estudiante )

            print(obj_score)
            print(int(score))
            if created:
                obj_score.score = int(score)
            else:
                obj_score.score = obj_score.score + int(score)
            
            print(obj_score.score_perfecto)
            print(juego_leccion.score_max)
            if ( int(score) ==  juego_leccion.score_max) and (obj_score.score_perfecto == False):
                obj_score.score_perfecto = True
                esPerfecto = True
                if nombre_estudiante.total_score_perfect is None:
                    nombre_estudiante.total_score_perfect = 1
                else:
                    nombre_estudiante.total_score_perfect += 1
                nombre_estudiante.save()
            else:
                esPerfecto = False

                
            obj_score.save()
            
            #guarda el historial gab
            
            
            object_historial , created = HistorialExperiencia.objects.get_or_create(estudiante = nombre_estudiante, fecha=date.today() )
            
            print(object_historial)
            
            if created:
                object_historial.puntos_obtenidos = int(score)
            else:
                object_historial.puntos_obtenidos =  object_historial.puntos_obtenidos + int(score)
            
            object_historial.save()
            
            try:
                clasificacion = Score_juegos_lesson.objects.filter(juego_lesson = juego_leccion).order_by('-score')[:5]
                clasificacion = list(clasificacion)
                
            except Exception as error:
                clasificacion = []
            
            
            script, div =  grafico_EXP(clasificacion)
            # clasificacion = serializers.serialize('json', clasificacion)
            clasificacion = [obj.serialize() for obj in clasificacion]
            clasificacion = json.dumps(clasificacion, cls=DjangoJSONEncoder)
            
            
            
            
        else:
            print(nombrejuego+'-'+score)
            mensaje = "¡Inicia sesión como estudiante para guardar el progreso !"
            messagetag = "info"
            # tipo_alerta = "success"
            # messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return JsonResponse({'esEstudiante': False,  'message':mensaje, 'messagetag': messagetag})
        return JsonResponse({'clasificacion': clasificacion, 'script':script, 'div': div, 'esEstudiante': True, 'esPerfecto': esPerfecto})
        return JsonResponse({'message': 'Data received successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
    
from bokeh.plotting import figure
from bokeh.embed import components
from django.db.models import Count
from bokeh.models import HoverTool

def grafico_EXP(clasificacion):
    
    clasificacion = clasificacion[::-1]
    
     # Preparar los datos para el gráfico.
    estudiantes = [dato.estudiante.user.username for dato in clasificacion]
    scores = [float(dato.score) for dato in clasificacion] 

    # Crear una nueva figura.
    p = figure(y_range=estudiantes, height=250, title="Puntuación por Estudiante",
               x_axis_label='Puntos', y_axis_label='Estudiante', tools="",  toolbar_location=None)

    # Crear un gráfico de barras horizontales.
    p.hbar(y=estudiantes, right=scores, height=0.5, color='#3466c8')
    
    hover = HoverTool(tooltips=[("Puntaje:", "@right")])
    p.add_tools(hover) 

    # Preparar el gráfico para ser usado en la plantilla de Django.
    script, div = components(p)
 
    
    return script, div


from django.http import HttpResponse

def serve_audio_file(request):
    with open('gamesUnityapp/static/gamesUnityapp/juegos_unity/audios/wind.mp3', 'rb') as f:
        data = f.read()
    response = HttpResponse(data, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="file.mp3"'
    return response
    

from cursosLeccionesapp.models import GrupoEstudiante, Grupo
from juegosapp.models import Lesson_cards
from ciertoFalsoapp.models import test_True_false

from cursosLeccionesapp.views import tabla_por_grupo
from cursosLeccionesapp.forms import GrupoForm_estudiante


def view_grupo_general(request, id_grupo):

    list_grupos = GrupoEstudiante.objects.filter(estudiante__user=request.user )
    mensajeVacio = ''
    if id_grupo == 'general':
        #grupoEstudiante = GrupoEstudiante.objects.filter(estudiante=request.user).order_by('?').first()
        #grupo = grupoEstudiante.grupo
        grupo = GrupoEstudiante.objects.filter(estudiante__user=request.user).order_by('?').first()
        if grupo:
            grupo = grupo.grupo
            mensajeVacio = ''
            juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
            test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
        else:
            grupo = []
            clasificacion = []
            mensajeVacio = 'Aún no te unes a ningún grupo'
            juegos_carta_por_grupo = []
            test_True_false_por_grupo = []
            
    else:
        grupo = GrupoEstudiante.objects.get(grupo=id_grupo, estudiante__user=request.user )
        grupo = grupo.grupo
        print(grupo)
        print(grupo.id)
        
        juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
        test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
    
    #agregar una comparacion del profesor que accede sea el mismo que tiene control del grupo

    #profesor_id = request.user  # Aquí puedes cambiar el ID del profesor
    if request.method == 'POST':
        form = GrupoForm_estudiante(request.POST, grupo_id=list_grupos)
        if form.is_valid():
            # ...
            print('valid')
            grupo = form.cleaned_data['grupo']
            
            print(form.cleaned_data['grupo'])
            print(type(form.cleaned_data['grupo']  ))
            juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
            test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
    else:
        form = GrupoForm_estudiante(grupo_id=list_grupos)
    #return render(request, 'mi_vista.html', {'form': form})
    
    print(grupo)
    # print(grupo.id)
    if grupo:
        clasificacion = tabla_por_grupo(grupo.id)
    
    

    # estudiantesPorGrupo = GrupoEstudiante.objects.filter(grupo = id_grupo)
    # estudiantes_Score_juegos_lesson = Score_juegos_lesson.objects.filter(estudiante__in = [estu.estudiante for estu in estudiantesPorGrupo])
    # print(estudiantesPorGrupo)
    # print(estudiantes_Score_juegos_lesson)
    # try:
        
    #     estudiantes_con_suma = estudiantes_Score_juegos_lesson.values('estudiante').annotate(total_score=Sum('score'))
    #     # estudiantes_con_suma = Score_juegos_lesson.objects.values('estudiante').annotate(total_score=Sum('score'))

    #     estudiantes = Estudiante.objects.filter(pk__in=[item['estudiante'] for item in estudiantes_con_suma])

    #     clasificacion = []
    #     for estudiante_con_suma in estudiantes_con_suma:
    #         estudiante = estudiantes.filter(pk=estudiante_con_suma['estudiante']).first()
    #         if estudiante:
    #             estudiante_con_suma['estudiante_obj'] = estudiante
    #             clasificacion.append(estudiante_con_suma)

    #     clasificacion = sorted(clasificacion, key=lambda x: x['total_score'], reverse=True)

    #     # clasificacion = Score_juegos_lesson.objects.all()
    #     # clasificacion = Score_juegos_lesson.objects.values(estudiante_obj=F('estudiante')).annotate(total_score=Sum('score')).order_by('-total_score')
    # except Exception as error:
    #     clasificacion = []
    
    
    # juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = id_grupo)
    # test_True_false_por_grupo = test_True_false.objects.filter(grupofk = id_grupo)
    
    #agregar una comparacion del profesor que accede sea el mismo que tiene control del grupo
    
  
 
    #print(clasificacion)
    context = {
        'clasificacion': clasificacion,
        'estudiantesPorGrupo': grupo,
        'Nombre_grupo': grupo,
        # 'estudiantesPorGrupo': estudiantesPorGrupo,
        # 'Nombre_grupo': estudiantesPorGrupo.first().grupo,
         'juegos_cartas': juegos_carta_por_grupo,
         'juegos_TF': test_True_false_por_grupo,
         'form': form,
        'mensajeVacio': mensajeVacio
    }
    return render(request, 'gamesUnityapp/template_grupo.html', context)