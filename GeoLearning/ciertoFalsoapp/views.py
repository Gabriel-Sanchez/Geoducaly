from datetime import date
import random
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Pregunta

# def jugar(request):
#     if request.method == 'POST':
#         pregunta_id = request.POST.get('pregunta_id')
#         respuesta = request.POST.get('respuesta')

#         pregunta = Pregunta.objects.get(id=pregunta_id)
#         es_correcta = pregunta.es_verdadera == (respuesta == 'verdadero')

#         return render(request, 'ciertoFalsoapp/result.html', {'es_correcta': es_correcta})

#     else:
#         pregunta = Pregunta.objects.order_by('?').first()
#         return render(request, 'ciertoFalsoapp/jugar.html', {'pregunta': pregunta})

# from django.http import JsonResponse

# def jugar(request):
#     if request.method == 'POST':
#         pregunta_id = request.POST.get('pregunta_id')
#         respuesta = request.POST.get('respuesta')

#         pregunta = Pregunta.objects.get(id=pregunta_id)
#         es_correcta = pregunta.es_verdadera == (respuesta == 'verdadero')

#         if request.is_ajax():
#             pregunta = Pregunta.objects.order_by('?').first()
#             return JsonResponse({'pregunta_texto': pregunta.texto, 'pregunta_id': pregunta.id, 'es_correcta': es_correcta})

#         return render(request, 'ciertoFalsoapp/result.html', {'es_correcta': es_correcta})

#     else:
#         pregunta = Pregunta.objects.order_by('?').first()
#         return render(request, 'ciertoFalsoapp/jugar.html', {'pregunta': pregunta})


from django.http import JsonResponse

# def jugar(request):
#     if 'preguntas' not in request.session or not request.session['preguntas']:
#         preguntas = list(Pregunta.objects.values_list('id', flat=True))
#         random.shuffle(preguntas)
#         print(len(preguntas))
#         request.session['preguntas'] = preguntas
#         request.session['puntaje'] = {'correctas': 0, 'incorrectas': 0}

#     print(request.session['preguntas'])
#     tamanio_listaP = len(request.session['preguntas'])
#     pregunta_id = request.session['preguntas'].pop()
#     pregunta = Pregunta.objects.get(id=pregunta_id)
#     print(request.session['preguntas'])
#     print('salia al principio')

#     if request.method == 'POST':
#         respuesta = request.POST.get('respuesta')
#         es_correcta = pregunta.es_verdadera == (respuesta == 'verdadero')

#         if es_correcta:
#             request.session['puntaje']['correctas'] += 1
#         else:
#             request.session['puntaje']['incorrectas'] += 1

#         request.session.modified = True

#         if request.is_ajax():
#             if request.session['preguntas']:
#                 pregunta_id = request.session['preguntas'][-1]
#                 pregunta = Pregunta.objects.get(id=pregunta_id)
#                 tamanio_listaP = len(request.session['preguntas'])
#                 return JsonResponse({'pregunta_texto': pregunta.texto, 
#                                      'pregunta_id': pregunta.id, 
#                                      'es_correcta': es_correcta, 
#                                      'tamanio_listP': tamanio_listaP,
#                                      'imagen_url': pregunta.imagen.url if pregunta.imagen else None})

#             else:
#                 puntaje = request.session['puntaje']
#                 del request.session['preguntas']
#                 del request.session['puntaje']
#                 return JsonResponse({'puntaje': puntaje})

#     return render(request, 'ciertoFalsoapp/jugar.html', {'pregunta': pregunta, 'tamanio_listaP': tamanio_listaP})

from gamesUnityapp.models import Score_juegos_lesson, HistorialExperiencia, Score_juegos_Group, Juegos_lesson


def guardar_score(user, score, juego_leccion, is_not_group):
    if user.is_authenticated:
        nombre_estudiante = user.estudiante
        print(nombre_estudiante)
        print('es jjuego_leccion:')
        print(juego_leccion) 
        
        if is_not_group:
            print('no se grupo')
            juego_lessonObject = Juegos_lesson.objects.get(lesson_id=juego_leccion)
            print("el juego lesson es:",juego_lessonObject)
            obj_score, created = Score_juegos_lesson.objects.get_or_create(juego_lesson = juego_lessonObject, estudiante = nombre_estudiante )
        else:
            obj_score, created = Score_juegos_Group.objects.get_or_create(juego_group_id = juego_leccion, estudiante = nombre_estudiante )
            
        print(obj_score)
        print(int(score))
        if created:
            obj_score.score = int(score)
        else:
            obj_score.score = obj_score.score + int(score)
        
        print(obj_score)
        obj_score.save()
        
        #guarda el historial gab
        object_historial , created = HistorialExperiencia.objects.get_or_create(estudiante = nombre_estudiante, fecha=date.today() )
        
        print(object_historial)
        
        if created:
            object_historial.puntos_obtenidos = int(score)
        else:
            object_historial.puntos_obtenidos =  object_historial.puntos_obtenidos + int(score)
        
        object_historial.save()
            
    else:
        print(score)


import json
def guardar_score_Post(request):
    
    
    if request.method == 'POST':
        data = json.loads(request.body)
        is_not_group = int( data.get('is_not_group', '')  )
        score = data.get('score', '')
        print(score)
        id_juego = data.get('id_lesson','')
        print('id lecciones :')
        print(id_juego)
        if request.user.is_authenticated:
            nombre_estudiante = request.user.estudiante
            print(nombre_estudiante)
            print(id_juego)
            print(is_not_group)
            
            if is_not_group:
                obj_score, created = Score_juegos_lesson.objects.get_or_create(juego_lesson_id = id_juego, estudiante = nombre_estudiante )
                print(obj_score.juego_lesson)
            else:
                obj_score, created = Score_juegos_Group.objects.get_or_create(juego_group_id = id_juego, estudiante = nombre_estudiante )
            #obj_score, created = Score_juegos_lesson.objects.get_or_create(juego_lesson__lesson__id = id_juego, estudiante = nombre_estudiante )

            print(obj_score)
            print(int(score))
            if created:
                obj_score.score = int(score)
            else:
                obj_score.score = obj_score.score + int(score)
            
            print(obj_score)
            obj_score.save()
            
            #guarda el historial gab
            object_historial , created = HistorialExperiencia.objects.get_or_create(estudiante = nombre_estudiante, fecha=date.today() )
            
            print(object_historial)
            
            if created:
                object_historial.puntos_obtenidos = int(score)
            else:
                object_historial.puntos_obtenidos =  object_historial.puntos_obtenidos + int(score)
            
            object_historial.save()
                
        else:
            print(score)
        # Ahora puedes usar la variable 'score'
        # ...
        return JsonResponse({'message': 'Datos recibidos correctamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)















from django.http import JsonResponse
from django.shortcuts import render
from .models import Pregunta
import random
from ciertoFalsoapp.models import test_True_false

def jugar(request, leccion_id):
    if 'preguntas' not in request.session or not request.session['preguntas']:
        #agregar una condicion aqui dondo leccion_id es un texto y si es un texto especifico
        #is_group y hacer otro filtro dependiendo de un grupo 
        print(leccion_id)
        print(  request.session['lesson_dificultad']['lesson'])
        numero_dificultad = int (request.session['lesson_dificultad']['difficultad'])
        print( numero_dificultad )
        text_all = test_True_false.objects.get(id = leccion_id )
        print('el text all es: ')
        print(text_all.get_preguntas(numero_dificultad))
        preguntas = list(text_all.get_preguntas(numero_dificultad).values_list('id', flat=True))
        # preguntas = list(Pregunta.objects.values_list('id', flat=True))
        random.shuffle(preguntas)
        request.session['preguntas'] = preguntas
        request.session['puntaje'] = {'correctas': 0, 'incorrectas': 0}
    
    if request.session['preguntas']:
        pregunta_id = request.session['preguntas'][-1]
        pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        print(respuesta)
        es_correcta = pregunta.es_verdadera == (respuesta == 'verdadero')

        if es_correcta:
            request.session['puntaje']['correctas'] += 1
        else:
            request.session['puntaje']['incorrectas'] += 1

        if request.session['preguntas']:
            pregunta_id = request.session['preguntas'].pop()


        request.session.modified = True

    if request.is_ajax():
        if request.session['preguntas']:
            pregunta_id = request.session['preguntas'][-1]
            pregunta = Pregunta.objects.get(id=pregunta_id)
            tamanio_listaP = len(request.session['preguntas'])
            return JsonResponse({'pregunta_texto': pregunta.texto, 
                                 'pregunta_id': pregunta.id, 
                                 'es_correcta': es_correcta, 
                                 'tamanio_listP': tamanio_listaP,
                                'leccion_id':leccion_id,
                                # 'titulo_leccion': pregunta.test_TF.leccion,
                                 'imagen_url': pregunta.imagen.url if pregunta.imagen else None})

        else:
            puntaje = request.session['puntaje']
            
            test_true_false_Obj = test_True_false.objects.get(id = leccion_id )
             
            if test_true_false_Obj.leccion is not None:
                is_not_group = True
                id_relacion = test_true_false_Obj.leccion.id
            else:
                is_not_group = False
                id_relacion = test_true_false_Obj.grupofk.id
            
            guardar_score(request.user,request.session['puntaje']['correctas'], id_relacion,  is_not_group  )
            del request.session['preguntas']
            del request.session['puntaje']
            return JsonResponse({'puntaje': puntaje, 'leccion_id':leccion_id
                                #  ,'titulo_leccion': pregunta.test_TF.leccion
                                 })
    tamanio_listaP = len(request.session['preguntas'])
    return render(request, 'ciertoFalsoapp/jugar.html', {'pregunta': pregunta , 'tamanio_listP': tamanio_listaP, 'leccion_id':leccion_id, 'titulo_leccion': pregunta.test_TF })



from django.shortcuts import redirect


def terminar(request):
    if request.method == 'POST':
        if 'preguntas' in request.session:
            del request.session['preguntas']
        if 'puntaje' in request.session:
            del request.session['puntaje']
        
        dificultad_CF = request.POST.get('dropdown')
        lesson_id = request.POST.get('lesson_id')    
        request.session['lesson_dificultad'] = {'lesson': lesson_id, 'difficultad': dificultad_CF}
        return redirect('jugar_cf', leccion_id= lesson_id )
    
    
    
    
# def terminar(request):
#     if request.method == 'POST':
#         if 'preguntas' in request.session:
#             del request.session['preguntas']
#         if 'puntaje' in request.session:
#             del request.session['puntaje']
#         return JsonResponse({})
