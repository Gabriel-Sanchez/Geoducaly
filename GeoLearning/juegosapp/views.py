from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import Prefetch
from django.shortcuts import redirect, render, get_object_or_404
from .models import ListQuiz, Pregunta, ijuegos, QuizUsuario, PreguntasRespondidas, UserNumQuiz, ElegirRespuesta

from django.db.models import Q
import random

from usersapp.models import Estudiante

from django.contrib.auth.decorators import login_required

from gamesUnityapp.models import Juegos_lesson
# Create your views here.


def llenarJuegosRapido(request):
    

    
    return  JsonResponse({'bien': 'bien'})

@login_required
def alljuegos(request):
    iju = ijuegos.objects.all()

    #trivias
    listaTrivias = ListQuiz.objects.all()
    
    # importante, revisar este funcionamiento
    
    estudent = Estudiante.objects.filter(user = request.user).first()

    usernumquiz = UserNumQuiz.objects.filter(usuario=estudent)
    
 
        
    

    listNumero = []
    

    for trivia in listaTrivias:
        for usertrivia in usernumquiz:
            if trivia == usertrivia.listquiz:
                print(trivia,"  ",usertrivia)
                l = [trivia, usertrivia.Num_veces_jugadas]
                break
                # listNumero.append(l)
            else:
                l = [trivia, 0]
                # listNumero.append(l)
        if  usernumquiz.exists():
            listNumero.append(l)

        if not usernumquiz.exists():
            l = [trivia, 0]
            listNumero.append(l)
    
    
    
    # listNumeronoRepet = []

    # noRepet = set(listNumero)
    # listNumeronoRepet = list(noRepet)
    

    print(listNumero)

    context = {
        'juegos': iju,
        'listaTrivias': listaTrivias,
        'listNumero': listNumero
    }
    return render(request,"juegosapp/juegos.html", context )

def juegos(request, eljuego):
    print(eljuego)
    iju = ijuegos.objects.get(id = eljuego)
    allj = ijuegos.objects.all()

    

    context = {
        'juegos': iju,
        'alljuegos': allj
    }
    return render(request,"juegosapp/jueg.html", context )
    

def juegos2(request):
    return render(request,"juegosapp/Juego_Scratch.html" )



def Juegotrivia(request,n_jugada, Lquiz):
    
    #revisar funcionamiento, se cambió la base de datos
    
    estudent = Estudiante.objects.filter(user = request.user).first()

    if n_jugada == 1:
        # QuizUserNUM, created = UserNumQuiz.objects.get_or_create(usuario=request.user, listquiz_id=Lquiz)
        QuizUserNUM, created = UserNumQuiz.objects.get_or_create(usuario=estudent, listquiz_id=Lquiz)
        QuizUserNUM = QuizUserNUM.first()
        QuizUserNUM.Num_veces_jugadas = 1
        QuizUserNUM.save()
    else:
        QuizUserNUM = UserNumQuiz.objects.filter(usuario=estudent, listquiz_id=Lquiz)
        # QuizUserNUM = UserNumQuiz.objects.filter(usuario=request.user, listquiz_id=Lquiz)
        if QuizUserNUM.exists():
            QuizUserNUM = QuizUserNUM.first()
            QuizUserNUM.Num_veces_jugadas = n_jugada
            QuizUserNUM.save()

    # UserNumQuiz.objects.get_or_create(usuario=request.user, listquiz_id=Lquiz)
    UserNumQuiz.objects.get_or_create(usuario=estudent, listquiz_id=Lquiz)
    

    listquiz = ListQuiz.objects.get(id = Lquiz)

    QuizUser, created = QuizUsuario.objects.filter(Q(Num_jugada=n_jugada)).get_or_create(usuario=request.user.estudiante,Num_jugada=n_jugada)

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
        
        except ObjectDoesNotExist:
            raise 'Http404'
        

        QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)

        return redirect('resultado', n_jugada, pregunta_respondida.pk)

    
    else:
        pregunta = QuizUser.obtener_nuevas_preguntas(listquiz)
        
        
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)

            opcionesP = pregunta.opciones.all()
            opcionesP = list(opcionesP)
            random.shuffle(opcionesP)

            context = {
            'pregunta' : pregunta,
            'opcionesP' : opcionesP 
            }
        
        else:
            #se realizaron cambios al codigo luego de modificar la base de datos
            estudent = Estudiante.objects.filter(user = request.user).first()
            puntaje =  QuizUsuario.objects.filter(usuario=estudent)
            sum = 0

            for i in puntaje:
                 sum = sum + i.puntaje_total 

            context = {
                'pregunta' : pregunta,
                'puntaje' : sum

            }




    return render(request, 'juegosapp/Juegotrivia.html', context)



def resultado_pregunta(request, n_jugada, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)
    context = {
        'respondida': respondida,
        'n_jugada': n_jugada
    }
    return render(request, 'juegosapp/resultadotrivia.html', context)

def tablero(request):
    total_usuario_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usuario_quiz.count()
    context = {
        'usuario_quiz': total_usuario_quiz,
        'contar_user': contador
    }

    return render(request, 'juegosapp/tablero.html', context)


def listaTrivias(request):

    numUserquiz = UserNumQuiz.objects.all()


    context = {

        'User_Num_Quiz': numUserquiz

    }

    return render(request, 'juegosapp/listaTrivias.html', context)



from django.shortcuts import render
from django.http import JsonResponse
from .models import Country
import random

from django.shortcuts import render
from .models import Country
import random

def home(request):
    countries = Country.objects.order_by('?')
    return render(request, 'juegosapp/home.html', {'countries': countries})


def get_countries(request):
    countries = list(Country.objects.values('name', 'size', 'image'))
    print(countries)
    random.shuffle(countries)
    return JsonResponse(countries, safe=False)


# En tu archivo views.py

# from django.http import JsonResponse
# from .models import CardPar

# def get_cards(request):
#     cards = CardPar.objects.all().values('id', 'image', 'name')
#     return JsonResponse(list(cards), safe=False)


from django.shortcuts import render
from .models import CardPar

# def game_view(request):
#     # Obtener las cartas desde la base de datos o cualquier otra fuente de datos
#     cards = CardPar.objects.all().values('id', 'image', 'name')
#     context = {'cards': cards}
#     return render(request, 'juegosapp/gameCardPar.html', context)

def get_card_pair(request):
    cards = list(CardPar.objects.all().values('id', 'image', 'name'))
    print(cards)
    random.shuffle(cards)
    return JsonResponse(cards, safe=False)


from django.shortcuts import render
from .models import CardPar

def game_view(request):
    # Obtener las cartas desde la base de datos o cualquier otra fuente de datos
    # cards = list(CardPar.objects.all().values('id', 'name', 'image') )

    # cards = CardPar.objects.order_by('?')
    # cards2 = CardPar.objects.order_by('?')
    
    id_lesson = int (request.session['lesson_dificultad_cards']['lesson'])
    lesson_cards = Lesson_cards.objects.get(id=id_lesson)
    
    cards = list(lesson_cards.get_cards(2) )
    cards2 = copy.deepcopy(cards )
    
    for card in cards:
        card.set = 1

    for card in cards2:
        card.set = 2
        
    lista = list(cards)  +  list(cards2 )
    random.shuffle(lista)
    
    if lesson_cards.leccion is not None:
        is_not_group = 1
        # id_relacion = lesson_cards.leccion.id
        id_de_leccion = lesson_cards.leccion.id
        id_relacion = Juegos_lesson.objects.get(lesson_id = id_de_leccion)
        id_relacion = id_relacion.id
    else:
        is_not_group = 0
        id_relacion = lesson_cards.grupofk.id
    
    context = {
        'cards': cards,
        'cards2': cards2,
        'cartas': lista,
        'id_lesson': id_lesson,
        'titulo_leccion': lesson_cards,
        'is_not_group': is_not_group,
        'id_relacion': id_relacion
               }
    return render(request, 'juegosapp/gameCardPar.html', context)

from juegosapp.models import Lesson_cards
import copy

def cardsPareo(request):
    # Obtener las cartas desde la base de datos o cualquier otra fuente de datos
    # cards = list(CardPar.objects.all().values('id', 'name', 'image') )
    id_lesson = int (request.session['lesson_dificultad_cards']['lesson'])
    
    lesson_cards = Lesson_cards.objects.get(id=id_lesson)

    # print('cards2 antes de 0 = '+cards2)
    # print('cards antes de 0 = '+cards)
    cards = []
    cards2 = []
    print('cards 1 despues de 0 =')
    print(cards)
    print('cards 2 despues de 0 =')
    print(cards2)
    cards = list(lesson_cards.get_cards(2) )
    cards2 = copy.deepcopy(cards )
    print("cards 1 despues de fultro")
    print(cards)
    print("cards 2 despues de fultro")
    print(cards2)
    
    # cards2 = lesson_cards.get_cards(2)
    # cards = CardPar.objects.order_by('?')
    # cards2 = CardPar.objects.order_by('?')
    
    for card in cards:
        card.set = 1

    for card in cards2:
        card.set = 2
        
    lista = list(cards)  +  list(cards2 )
    random.shuffle(lista)
    

    if lesson_cards.leccion is not None:
        is_not_group = 1
        # id_relacion = lesson_cards.leccion.id
        id_de_leccion = lesson_cards.leccion.id
        id_relacion = Juegos_lesson.objects.get(lesson_id = id_de_leccion)
        id_relacion = id_relacion.id
        
    else:
        is_not_group = 0
        id_relacion = lesson_cards.grupofk.id
    
    context = {
        'cards': cards,
        'cards2': cards2,
        'cartas': lista,
        'id_lesson': id_lesson,
        'titulo_leccion': lesson_cards,
        'is_not_group': is_not_group,
        'id_relacion': id_relacion
               }
    return render(request, 'juegosapp/pareoCartas.html', context)


   
def card_difuculty(request):
    if request.method == 'POST':
        print('post trivia')
        if 'preguntas' in request.session:
            del request.session['preguntas']
        if 'puntaje' in request.session:
            del request.session['puntaje']
        
        
        dificultad = request.POST.get('dropdown')
        lesson_id = request.POST.get('lesson_id')
        request.session['lesson_dificultad_cards'] = {'lesson': lesson_id, 'difficultad': dificultad}
        
        if dificultad == '1': 
            return redirect('cardsPareo' )
        else:
            return redirect('get_cards' )


# def card_dificulty_group(request):
#     if request.method == 'POST':
#         print('post trivia')
#         if 'preguntas' in request.session:
#             del request.session['preguntas']
#         if 'puntaje' in request.session:
#             del request.session['puntaje']
        
        
#         dificultad = request.POST.get('dropdown')
#         lesson_id = request.POST.get('lesson_id')
#         request.session['lesson_dificultad_cards'] = {'lesson': lesson_id, 'difficultad': dificultad}
        
#         if dificultad == '1': 
#             return redirect('cardsPareo' )
#         else:
#             return redirect('get_cards' )
            
#         # return redirect('jugar_trivia', leccion_id= lesson_id )



from ciertoFalsoapp.views import guardar_score

import json

from django.http import JsonResponse
from django.shortcuts import render
import random
from ciertoFalsoapp.models import test_True_false
from .models import ListQuiz, Pregunta,PreguntasRespondidas
from django.core import serializers


def jugar_trivia(request, leccion_id):
    if 'preguntas' not in request.session or not request.session['preguntas']:
        print(leccion_id)
        print(  request.session['lesson_dificultad']['lesson'])
        numero_dificultad = int (request.session['lesson_dificultad']['difficultad'])
        print( numero_dificultad )
        text_all = ListQuiz.objects.get(id = leccion_id )
        print('el text all es: ')
        print(text_all.get_preguntas(numero_dificultad))
        preguntas = list(text_all.get_preguntas(numero_dificultad).values_list('id', flat=True))
        # preguntas = list(Pregunta.objects.values_list('id', flat=True))
        random.shuffle(preguntas)
        request.session['preguntas'] = preguntas
        request.session['puntaje'] = {'correctas': 0, 'incorrectas': 0}
    pregunta = None
    if request.session['preguntas']:
        pregunta_id = request.session['preguntas'][-1]
        pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == 'POST':
        
        pregunta_pk = request.POST.get('pregunta_pk')
        # pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')
        
        respondida = pregunta.verificar_respuesta(respuesta_pk)
        
        print(pregunta_pk)
        print(respuesta_pk)
        
        print(pregunta.verificar_respuesta(respuesta_pk).correcta)
        print(pregunta.verificar_respuesta(respuesta_pk))
        
        if respondida.correcta:
            LaRespuesta = respondida.texto
            request.session['puntaje']['correctas'] += 1
        else:
            LaRespuesta = pregunta.get_respuesta_correcta().texto
            request.session['puntaje']['incorrectas'] += 1
        
        
        
        
        
        
        
        # respuesta = request.POST.get('respuesta')
        # print(respuesta)
        # es_correcta = pregunta.es_verdadera == (respuesta == 'verdadero')

        # if es_correcta:
        #     request.session['puntaje']['correctas'] += 1
        # else:
        #     request.session['puntaje']['incorrectas'] += 1

        if request.session['preguntas']:
            pregunta_id = request.session['preguntas'].pop()


        request.session.modified = True

    if request.is_ajax():
        if request.session['preguntas']:
            pregunta_id = request.session['preguntas'][-1]
            pregunta = Pregunta.objects.get(id=pregunta_id)
            tamanio_listaP = len(request.session['preguntas'])
            
            print(respondida)
            opcionesP = pregunta.opciones.all()
            opcionesP = list(opcionesP)
            random.shuffle(opcionesP)
            
            
            opcionesP = serializers.serialize('json', opcionesP)
            
            data = {'pregunta_texto': pregunta.texto, 
                                 'pregunta_id': pregunta.id, 
                                #  'es_correcta': es_correcta, 
                                 'respondida': { 
                                                'pregunta': respondida.pregunta.texto ,
                                                'correcta': respondida.correcta, 
                                                'texto': respondida.texto,
                                                'LaRespuesta': LaRespuesta 
                                                } ,
                                 'opcionesP': opcionesP,
                                 'tamanio_listP': tamanio_listaP,
                                'leccion_id':leccion_id,
                                # 'titulo_leccion': pregunta.test_TF.leccion,
                                 'imagen_url': pregunta.picture.url if pregunta.picture else None}
            
            return JsonResponse(data, safe=False)

        else:
            #mandar la ultima respuesta aqui para poder mostrarla en el template
            puntaje = request.session['puntaje']
            
            listquiz_leccion = ListQuiz.objects.get(id = leccion_id )
             
            if listquiz_leccion.leccion is not None:
                is_not_group = True
                id_relacion = listquiz_leccion.leccion.id
            else:
                is_not_group = False
                id_relacion = listquiz_leccion.grupofk.id
            
            
            guardar_score(request.user,request.session['puntaje']['correctas'], id_relacion, is_not_group )
            del request.session['preguntas']
            del request.session['puntaje']
            return JsonResponse({'puntaje': puntaje, 'leccion_id':leccion_id, 
                                 
                                 'respondida': { 
                                                'pregunta': respondida.pregunta.texto ,
                                                'correcta': respondida.correcta, 
                                                'texto': respondida.texto,
                                                'LaRespuesta': LaRespuesta 
                                                }
                                #  ,'titulo_leccion': pregunta.test_TF.leccion
                                 })
    tamanio_listaP = len(request.session['preguntas'])
    opcionesP = pregunta.opciones.all()
    opcionesP = list(opcionesP)
    random.shuffle(opcionesP)
    
    context = {'pregunta': pregunta , 
               'tamanio_listP': tamanio_listaP, 
               'leccion_id':leccion_id, 
               'titulo_leccion': pregunta.listquiz.leccion ,
                'opcionesP' : opcionesP 
               
               }
    return render(request, 'juegosapp/Juegotrivia_leccion.html', context)


from django.shortcuts import redirect


def terminar_trivia(request):
    if request.method == 'POST':
        print('post trivia')
        if 'preguntas' in request.session:
            del request.session['preguntas']
        if 'puntaje' in request.session:
            del request.session['puntaje']
        
        dificultad_CF = request.POST.get('dropdown')
        lesson_id = request.POST.get('lesson_id')    
        request.session['lesson_dificultad'] = {'lesson': lesson_id, 'difficultad': dificultad_CF}
        return redirect('jugar_trivia', leccion_id= lesson_id )