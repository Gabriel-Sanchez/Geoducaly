# from GeoLearning.cursosLeccionesapp.models import Quiz
import json
from django import setup
from django.http import request
from django.shortcuts import render

from bokeh.models import HoverTool
from django.contrib import messages

import pandas as pd

# Create your views here.

#para el login
from django.contrib.auth import authenticate, get_user,login,logout
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from usersapp.models import Estudiante, Profesor
from cursosLeccionesapp.models import  Result, Lesson, Quiz, course, Grupo, GrupoNotas, GrupoEstudiante

from usersapp.forms import ProfileForm, ProfileFormImage, ProfileFormPass,ProfileFormUserE

from django.views.generic import TemplateView, View

from usersapp.decorators import non_staff_required

import statistics

#antes de editar
from copy import deepcopy




#exceptions
from django.db.utils import IntegrityError

# Create your views here.

@login_required
@non_staff_required
def update_profile(request):
    p = request.user
    user = User.objects.get(username=p.username)

    try:
        p2 = p
        estudiante =Estudiante.objects.get(user = p2)
    except Exception as error:
        estudiante = request.user.profesor


    #deberia guardarse como profile_ no como estudiante porque es general
    #pero se deja asi por el momento para evitar problemas, se arreglará
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and form_type == 'form2':
            data = form.cleaned_data

            estudiante.phone_number = data['phone_number']
            estudiante.biography = data['biography']
            user.first_name = data['firstname']
            user.last_name = data['lastname']
            estudiante.country = data['country']
            estudiante.city = data['city']

            user.save()
            estudiante.save()

            print(form.cleaned_data)
            mensaje = 'Los cambios se guardaron correctamente'
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return redirect('details_profile')

        form_image = ProfileFormImage(request.POST, request.FILES)
        if form_image.is_valid() and form_type == 'form1':
            data = form_image.cleaned_data

            estudiante.picture = data['picture']

            estudiante.save()

            print(form_image.cleaned_data)
            mensaje = 'Los cambios se guardaron correctamente'
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return redirect('details_profile')

        FormPass = ProfileFormPass(request.POST, request.FILES)
        if FormPass.is_valid() and form_type == 'form4':
            data = FormPass.cleaned_data

            currentPass = data['currentPass']
            newPass = data['newPass']
            confirmPass = data['confirmPass']


            if not(user.check_password(currentPass)):
                return render(request=request, template_name='users/update_profile.html',
                context={'estudiante': estudiante, 'user': request.user, 'form':form, 'error': 'contraseña actual incorrecta'} )

            elif newPass != confirmPass:
                return render(request=request, template_name='users/update_profile.html',
                context={'estudiante': estudiante, 'user': request.user, 'form':form, 'error': 'Las nuevas contraseñas no coinciden'} )
            elif (user.check_password(newPass)):
                return render(request=request, template_name='users/update_profile.html',
                context={'estudiante': estudiante, 'user': request.user, 'form':form, 'error': 'La nueva contraseña no puede ser la misma que la contraseña actual'} )
            else:
                try:
                    validate_password(newPass)
                except ValidationError as e:
                    errors = ', '.join(e.messages)
                    return render(request=request, template_name='users/update_profile.html',
                    context={'estudiante': estudiante, 'user': request.user, 'form':form, 'error': errors} )
                user.set_password(newPass)
                user.save()

            print(FormPass.cleaned_data)
            mensaje = 'Los cambios se guardaron correctamente'
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return redirect('logout')

        FormUserE = ProfileFormUserE(request.POST, request.FILES)
        if FormUserE.is_valid() and form_type == 'form3':
            data = FormUserE.cleaned_data

            user.email = data['email']
            user.username = data['username']
            
            
            if request.user.username != user.username:
                user_base = User.objects.filter(username=user.username).exists()
            else:
                user_base = False
            print("ss----------------------")
            print(user_base)
            
            if request.user.email != user.email:
                existe_email = User.objects.filter(email=user.email).exists()
            else:
                existe_email = False
            
            
            if user_base:
                if existe_email:
                    mensaje = 'El email y nombre de usuario ya existen'

                mensaje = 'El nombre de usuario ya existe'
                tipo_alerta = "error"
                messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            elif existe_email:
                mensaje = 'El email ya existe'
                tipo_alerta = "error"
                messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
                
            else:
                user.save()
                mensaje = 'Los cambios se guardaron correctamente'
                tipo_alerta = "success"
                messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
                return redirect('details_profile')

            print(FormUserE.cleaned_data)
                
    else:
        form = ProfileForm()

    return render(request=request, template_name='users/update_profile.html',
    context={'estudiante': estudiante, 'user': request.user, 'form':form} )


from gamesUnityapp.models import Score_juegos_lesson, HistorialExperiencia
from datetime import datetime, timedelta

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd
import random

from bokeh.embed import components
from bokeh.models import Range1d

from gamesUnityapp.models import Juegos_lesson

from babel.dates import format_date
@login_required
@non_staff_required
def details_profile(request):
    p = request.user
    user = User.objects.get(username=p.username)
    
    #se realizaron cambios al modificar la base de datos
    try:
        estudiante = Estudiante.objects.get(user = p)
        # clases = clase.objects.filter(estudiante__user__username=estudiante.user)
        clases = GrupoEstudiante.objects.filter(estudiante__user=estudiante.user)
    except Exception as error:
        # estudiante = request.user.profesor
        
        estudiante = Profesor.objects.get(user = p)
        # clases = clase.objects.filter(profesor__user__username=estudiante.user)
        clases = Grupo.objects.filter(profesor__user=estudiante.user)

    print(clases)

    resultantList = []
    listcourse = []

    for element in clases:
        # if element.codigo not in resultantList:
        # resultantList.append(element.codigo)
        listcourse.append(element)
    # for element in clases:
    #     if element.codigo not in resultantList:
    #         resultantList.append(element.codigo)
    #         listcourse.append(element)
        
    notas = []

    # quices = Lesson.objects.all()
    
    list_notas_por_grupo = []
    list_notas_por_grupolista = []

    try:
        from collections import defaultdict 
        # for qui in quices:
        #     filtro1 = Result.objects.filter(user__username = p, quiz__lessson__id = qui.id)
        #     filtro1 = filtro1.order_by('-score')[0]
        #     if filtro1:
        #         notas.append(filtro1)
        for clase in clases:
            users = defaultdict(list)
            # users = defaultdict(list)
            notas_por_Grupo_Estudiante = GrupoNotas.objects.filter(nota__quiz__lessson__course = clase.grupo.course, nota__user= p)
            # notas_por_Grupo_EstudianteOrdenado =  notas_por_Grupo_Estudiante.order_by('-nota__score')[0]
            for result in notas_por_Grupo_Estudiante.values('nota__quiz__name','nota__score','nota__quiz__lessson__course').order_by('nota__quiz__name','nota__score'):
                users[result['nota__quiz__name']].append(result['nota__score'])
            
            
            print(users.keys())
            print(users.values())
            for (u,v) in zip(users.keys(),users.values()):
                print(u,v)
                users[u] = max(v)
            
            notasOrd = []
            # for dato in user:
            #     notasOrd.append([ x for x in zip( dato.keys() ,dato.values() )  ])
            notasOrd = [ x for x in zip( users.keys() ,users.values() )  ]
            
            
            list_notas_por_grupo.append(
                {
                    'curso':clase.grupo.course.title,
                    'notas':notasOrd,
                    # 'notas':users,
                }
                
                )
                # print(users)
        
        # for dato in list_notas_por_grupo:
        #     list_notas_por_grupolista.append([ x for x in zip( dato.keys() ,dato.values() )  ]) 
       
       
        # ordenado = []
        # for i in list_notas_por_grupo:
        #     ordenado = []
        #     for j,t in i.values(),i.keys():
        #         ordenado.append(j,t)
        #     list_notas_por_grupolista.append(ordenado)
            
        print("list_notas_por_grupo",list_notas_por_grupo)
        print("list_notas_por_grupolista",list_notas_por_grupolista)
        
        
        for i in list_notas_por_grupolista:
            print(i)
            

    except Exception as error:
        a = error
    
    List_estudiantesPorCurso = []
    
    try:
        
        #obtiene todos los grupos del profesor
        profGrupo = Grupo.objects.filter(profesor=request.user.profesor)
        print(profGrupo)
        
        # List_quicesPorCurso = []
            
        #obtener lista de quices y estudiantes separados por los grupos
        for grupoprof in profGrupo:
            # quices = Quiz.objects.filter(lessson__course=grupoprof.course)
            # List_quicesPorCurso.append(quices)
            estudiantes = GrupoEstudiante.objects.filter(grupo=grupoprof)
            if estudiantes.exists(): 
                List_estudiantesPorCurso.append(estudiantes)

        print(List_estudiantesPorCurso)
        
    except Exception as error:
        print(error)
        
    print(list_notas_por_grupolista)
    print(list_notas_por_grupo)
    
    try:
        notas = Score_juegos_lesson.objects.filter(estudiante=estudiante)
        
    except Exception as error:
        clasificacion = []
    
    
    
    #grafico experiencia
    ahoraM = datetime.now()
    hace_siete_dias = datetime.now() - timedelta(days=7)
    try:

        historialExp = HistorialExperiencia.objects.filter(fecha__gte=hace_siete_dias, estudiante=estudiante)
        data = [{'Fecha': registro.fecha.strftime('%Y-%m-%d'), 'Exp': registro.puntos_obtenidos} for registro in historialExp]
        df = pd.DataFrame(data)

        fechas = pd.date_range(start=hace_siete_dias, end=datetime.now())
        df_todos_los_dias = pd.DataFrame(fechas, columns=['Fecha'])

        df['Fecha'] = df['Fecha'].astype(str)
        df_todos_los_dias['Fecha'] = df_todos_los_dias['Fecha'].dt.strftime('%Y-%m-%d')
        df_final = pd.merge(df_todos_los_dias, df, how='left', on='Fecha')
        df_final['Exp'] = df_final['Exp'].fillna(0)

        df_final['Fecha'] = pd.to_datetime(df_final['Fecha']).dt.strftime('%d')
        # df_final['Fecha'] = pd.to_datetime(df_final['Fecha']).dt.strftime('%d-%m')
        
        rangomax = df_final['Exp'].max()

    
    except Exception as error:
        fecha_actual = datetime.now()
        hace_siete_dias = fecha_actual - timedelta(days=7)
        rango_fechas = pd.date_range(start=hace_siete_dias, end=fecha_actual, freq='D').date
        data = [{'Fecha': dia.strftime('%d'), 'Exp': 0} for dia in rango_fechas]
        df_final = pd.DataFrame(data)
        rangomax = 10


    source = ColumnDataSource(df_final)

    p = figure(width=700, height=160, x_range=df_final['Fecha'].tolist(), tools="",  toolbar_location=None)
    
    p.xaxis.axis_label = 'Fecha - Días- ' + format_date(ahoraM, 'MMMM', locale='es')
    p.yaxis.axis_label = 'Experiencia'
    
    p.y_range = Range1d(0, rangomax)

    # Agregar barras verticales al gráfico
    p.vbar(x='Fecha', top='Exp', source=source, width=0.5, bottom=0, color='#3466c8')
    
    #ver valor con el cursos gab
    
    hover = HoverTool(tooltips=[("Exp", "@Exp")])
    p.add_tools(hover) 

    # Generar el código HTML y la representación JavaScript del gráfico
    script, div = components(p)
    print(datetime.now())
    
    num_total_juegos = Juegos_lesson.objects.count()


    context={
        'estudiante': estudiante,
        'clases': clases,
        'listaCursos': listcourse,
        'notas': notas,
        'List_estudiantesPorCurso': List_estudiantesPorCurso,
        'list_notas_por_grupo':list_notas_por_grupo,
        'notas': notas,
        'script': script, 
        'div': div,
        'num_total_juegos': num_total_juegos

        }

    return render(request, 'users/details_profile.html', context )


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'users/login.html', {'error': ' Nombre de usuario o contraseña incorrectas'} )

    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def signup(request):
    if request.method == 'POST':
        opcion = request.POST['options']

        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        
        if User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'users/signup.html', {'error': 'El correo electrónico ya está en uso'})

        if password != password_confirmation:
            return render(request, 'users/signup.html', {'error': 'Las contraseñas no coincide'})

        # Añade esta parte para validar la contraseña
        try:
            validate_password(password)
        except ValidationError as e:
            errors = ', '.join(e.messages)
            return render(request, 'users/signup.html', {'error': errors})

        if opcion == "on":
            return render(request, 'users/signup.html', {'error': 'debe elegir el tipo de usuario'})

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return render(request, 'users/signup.html', {'error': 'El nombre de usuario ya existe'})
        
        
        

        #user.first_name = request.POST['First_name']
        #user.last_name = request.POST['Last_name']
        user.email = request.POST['email']

        user.save()

        if opcion == "1":
            estudiante = Estudiante(user=user)
            estudiante.type = 1
            estudiante.save()
        elif opcion == "2":
            estudiante = Profesor(user=user)
            estudiante.type = 2
            estudiante.save()

        return redirect('login')

    return render(request, 'users/signup.html')


from juegosapp.models import Lesson_cards
from ciertoFalsoapp.models import test_True_false, Pregunta

from django.shortcuts import render
from .forms import PreguntaForm, TestForm, LessonCardsForm, CardParForm
from django.shortcuts import render, redirect, get_object_or_404

from django.forms import formset_factory

from juegosapp.models import CardPar

def crear_cf(request, id_grupo):
    grupo_para_Crear = Grupo.objects.get(id=id_grupo)
    PreguntaFormSet = formset_factory(PreguntaForm, extra=1)

    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES)
        preguntas_formset = PreguntaFormSet(request.POST, request.FILES, prefix='preguntas')
        if form.is_valid() and preguntas_formset.is_valid():
            #test = form.save()
            test = form.save(commit=False)
            test.grupofk = Grupo.objects.get(id=id_grupo)
            test.save()
            for pregunta_form in preguntas_formset:
                if pregunta_form.cleaned_data.get('texto') != None:
                    # print(pregunta_form.cleaned_data.get('texto'))
                    pregunta = pregunta_form.save(commit=False)
                    pregunta.test_TF = test
                    if pregunta_form.cleaned_data.get('imagen'):
                        pregunta.imagen=pregunta_form.cleaned_data.get('imagen') 
                    
                    pregunta.save()
            
            mensaje = "¡El juego " + test.name + " se creó correctamente !"
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            if 'accion1' in request.POST:
                return redirect('prof_edit_CF', id_juego=test.pk)
                # Realiza la acción específica para el botón 1 aquí
            elif 'accion2' in request.POST:
                return redirect('courses:detalles_grupo', grupo_id=id_grupo)
                return render(request, 'juegos_grupo/crear_juego_cf.html', {'form': form, 'preguntas_formset': preguntas_formset, 'grupo_obj': grupo_para_Crear })
    else:
        form = TestForm()
        preguntas_formset = PreguntaFormSet(prefix='preguntas')

    return render(request, 'juegos_grupo/crear_juego_cf.html', {'form': form, 'preguntas_formset': preguntas_formset, 'grupo_obj': grupo_para_Crear })


def editar_cf(request, id_juego):
    test = get_object_or_404(test_True_false, id=id_juego)
    PreguntaFormSet = formset_factory(PreguntaForm, extra=0)

    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES, instance=test)
        preguntas_formset = PreguntaFormSet(request.POST,  request.FILES, prefix='preguntas')
        if form.is_valid() and preguntas_formset.is_valid():
            test = form.save()
            for pregunta_form in preguntas_formset:
                id = pregunta_form.cleaned_data.get('id')
                print(id)
                if id:
                    # Si el ID existe, obtén la instancia de la pregunta
                    pregunta = Pregunta.objects.get(id=id)
                    print(pregunta_form.cleaned_data.get('eliminar'))
                    print(type(pregunta_form.cleaned_data.get('eliminar')))
                    if pregunta_form.cleaned_data.get('eliminar'):
                        # Si el campo 'eliminar' es verdadero, elimina la pregunta
                        print('delete')
                        pregunta.delete()
                    else:
                        # De lo contrario, actualiza la pregunta
                        pregunta.texto = pregunta_form.cleaned_data.get('texto')
                        pregunta.es_verdadera = pregunta_form.cleaned_data.get('es_verdadera')
                        pregunta.test_TF = test
                        if pregunta_form.cleaned_data.get('imagen'):
                            pregunta.imagen=pregunta_form.cleaned_data.get('imagen') 
                        pregunta.save()
                else:
                    if pregunta_form.cleaned_data.get('eliminar') != True:
                        if pregunta_form.cleaned_data.get('eliminar') != None:
                            Pregunta.objects.create(
                                texto=pregunta_form.cleaned_data.get('texto'),
                                es_verdadera=pregunta_form.cleaned_data.get('es_verdadera'),
                                imagen=pregunta_form.cleaned_data.get('imagen') if pregunta_form.cleaned_data.get('imagen') else None,
                                test_TF=test
                            )
            mensaje = "¡El juego " + test.name + " se guardó correctamente !"
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            if 'accion1' in request.POST:
                return redirect('prof_edit_CF', id_juego=test.pk)
                return redirect('prof_edit_CF', id_juego=test.pk)
                # Realiza la acción específica para el botón 1 aquí
            elif 'accion2' in request.POST:
                return redirect('courses:detalles_grupo', grupo_id=test.grupofk.id)
                return render(request, 'juegos_grupo/editar_juego_cf.html', {'form': form, 'preguntas_formset': preguntas_formset, 'grupo_obj': test.grupofk})

    else:
        form = TestForm(instance=test)
        initial_data = [{'id': pregunta.id, 'texto': pregunta.texto, 'es_verdadera': pregunta.es_verdadera, 'imagen': pregunta.imagen } for pregunta in test.preguntas_test_tf.all()]
        preguntas_formset = PreguntaFormSet(initial=initial_data, prefix='preguntas')

    return render(request, 'juegos_grupo/editar_juego_cf.html', {'form': form, 'preguntas_formset': preguntas_formset, 'grupo_obj': test.grupofk})


def editar_carta(request, id_juego):
    lesson = get_object_or_404(Lesson_cards, id=id_juego)
    CardParFormSet = formset_factory(CardParForm, extra=0)

    if request.method == 'POST':
        form = LessonCardsForm(request.POST,  request.FILES, instance=lesson)
        cards_formset = CardParFormSet(request.POST, request.FILES, prefix='cards')
        if form.is_valid() and cards_formset.is_valid():
            lesson = form.save()
            for card_form in cards_formset:
                id = card_form.cleaned_data.get('id')
                print(id)
                if id:
                    # If the ID exists, get the instance of the card
                    card = CardPar.objects.get(id=id)
                    print(card_form.cleaned_data.get('eliminar'))
                    print(type(card_form.cleaned_data.get('eliminar')))
                    if card_form.cleaned_data.get('eliminar'):
                        # If the 'eliminar' field is true, delete the card
                        print('delete')
                        card.delete()
                    else:
                        # Otherwise, update the card
                        card.name = card_form.cleaned_data.get('name')
                        card.lesson_cards = lesson
                        if card_form.cleaned_data.get('image'):
                            card.image=card_form.cleaned_data.get('image') 
                        # if 'image' in request.FILES:
                        #     card.image = request.FILES['image']
                        card.save()
                else:
                    if card_form.cleaned_data.get('eliminar') != True :
                        if card_form.cleaned_data.get('eliminar') != None :
                            CardPar.objects.create(
                                name=card_form.cleaned_data.get('name'),
                                lesson_cards=lesson,
                                image=card_form.cleaned_data.get('image') if card_form.cleaned_data.get('image') else None
                            )
            mensaje = "¡El juego " + lesson.name + " se guardó correctamente !"
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            if 'accion1' in request.POST:
                return redirect('editar_carta', id_juego=lesson.pk)

            elif 'accion2' in request.POST:
                return redirect('courses:detalles_grupo', grupo_id=lesson.grupofk.id)
        # else:
        #     for card_form in cards_formset:
        #         id = card_form.cleaned_data.get('id')
        #         if id:
        #             card = CardPar.objects.get(id=id)
        #             card_form.instance.image = card.image
        #             print(card_form.instance.image)
    else:
        form = LessonCardsForm(instance=lesson)
        initial_data = [{'id': card.id, 'name': card.name, 'image': card.image} for card in lesson.cartas_de_leccion.all()]
        cards_formset = CardParFormSet(initial=initial_data, prefix='cards')

    return render(request, 'juegos_grupo/editar_juego_carta.html', {'form': form, 'cards_formset': cards_formset, 'grupo_obj': lesson.grupofk})



def crear_carta(request, id_grupo):
    print('crea carta')
    grupo_para_Crear = Grupo.objects.get(id=id_grupo)
    LessonCardsFormSet = formset_factory(LessonCardsForm, extra=1)
    CardParFormSet = formset_factory(CardParForm, extra=1)

    if request.method == 'POST':
        form = LessonCardsForm(request.POST, request.FILES,)
        cards_formset = CardParFormSet(request.POST, request.FILES, prefix='cards')
        if form.is_valid() and cards_formset.is_valid():
            lesson = form.save(commit=False)
            lesson.grupofk = Grupo.objects.get(id=id_grupo)
            lesson.save()
            for card_form in cards_formset:
                print(card_form)
                # card = card_form.save(commit=False)
                # card.lesson_cards = lesson
                # card.save()
                if card_form.cleaned_data.get('name') != None:
                    CardPar.objects.create(
                                name=card_form.cleaned_data.get('name'),
                                image=card_form.cleaned_data.get('image') if card_form.cleaned_data.get('image') else None,
                                lesson_cards=lesson
                            )
                    print('guerdado')
            mensaje = "¡El juego " + lesson.name + " se creó correctamente !"
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            if 'accion1' in request.POST:
                return redirect('editar_carta', id_juego=lesson.pk)
                return redirect('editar_carta', id_juego=lesson.pk)

            elif 'accion2' in request.POST:

                return redirect('courses:detalles_grupo', grupo_id=id_grupo)
    else:
        form = LessonCardsForm()
        cards_formset = CardParFormSet(prefix='cards')

    return render(request, 'juegos_grupo/crear_juego_carta.html', {'form': form, 'cards_formset': cards_formset, 'grupo_obj': grupo_para_Crear })




class Obquiz:
    name = ""
    nota = 0
    estudiant = ""

class Obleccion:
    name = ""
    quiz = Obquiz()
class Obcurso:
    name = 0
    lecc = Obleccion()
    

class claseCompleta:
    name = ""
    curso = Obcurso()



class prof(TemplateView):
    template_name = "users/prof_charts.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def p(self):

        p = self.request.user
        # user = User.objects.get(username=p.username)
        try:
            estudiante = Estudiante.objects.get(user = p)
            # clases = clase.objects.filter(estudiante__user__username=estudiante.user)
            clases = []
        except Exception as error:
            estudiante = self.request.user.profesor
            # clases = clase.objects.filter(profesor__user__username=estudiante.user)
            clases = []

        resultantList = []
        listcourse = []

        for element in clases:
            if element.codigo not in resultantList:
                resultantList.append(element.codigo)
                listcourse.append(element)

        datosChart = []
        classEstudianteNotas = []


        for estudiantes in clases:
            print(estudiantes.estudiante.user.id, "----------------------------")
            estudianteClass = Result.objects.filter(user = estudiantes.estudiante.user.id, quiz__lessson__course = estudiantes.course)
            if estudianteClass:
                datosChart.append(estudianteClass)
                
                ResNotas = []
                orden = []
                for notas in estudianteClass:
                    # ResNotas.append(notas.score)
                    # max(ResNotas)
                    # orden = []
                    print(notas.quiz.lessson, "   " ,notas.quiz, notas.score )
                # classEstudianteNotas.append(orden)
                print(estudianteClass)
            else:
                print("pos no")


        print("ooooooooooooooooooooooooooooooooooo")
        # print(datosChart)


        for x in datosChart:
            print("xxxxxxxxxxxxxx")
            for orden in x:
                print(orden.quiz.lessson, "   " ,orden.quiz, orden.score )


        print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")






        # a = Result.objects.all()
        # print(a)
        # for i in a:
        #     print(i.user.pk)



        for i in datosChart:
            print(i)


        claseEstudiante = []

        for lista in listcourse:
            estudiante = []
            for clasel in clases:
                if lista.codigo == clasel.codigo:
                    estudiante.append(str(clasel.estudiante))
            claseEstudiante.append(estudiante)

        print(claseEstudiante)

        l = [5,7,3,1,87,3,465,41,21,56]
        mean = statistics.mean(l)

        print(max(l))
        print(mean)

        nombreclasescursos = []

        for clasescursos in clases:
            nombreclasescursos.append(clasescursos.course)



        listaDeLecciones = Lesson.objects.filter(course__in=nombreclasescursos)
        listDEQuices = Quiz.objects.all()

        for est in claseEstudiante:
            for e in est:
                for less in listaDeLecciones:
                    for Nquiz in listDEQuices:
                        for x in datosChart:
                            for orden in x:
                                if Nquiz == orden.quiz and less == orden.quiz.lessson and e == orden.user:
                                    print(orden.quiz.lessson, "   " ,orden.quiz, orden.score, orden.user )
        
        allll = []
        ordenCursos = []
        ordenlecciones = []
        ordenquiz = []
        ordenuser = []
        ob = [] 
        for less in listaDeLecciones:
            lessAux = []
            for Nquiz in listDEQuices:
                NquizAux = []
                for est in claseEstudiante:
                    for e in est:
                        eAux = []
                        try:
                            filtro1 = Result.objects.filter(user__username = e, quiz__lessson = less, quiz = Nquiz)
                            filtro1 = filtro1.order_by('-score')[0]
                            if filtro1:
                                

                                allll.append(filtro1)
                                print(filtro1.user)
                                lessAux.append("")
                                NquizAux.append("")
                                eAux.append("")
                                ordenuser.append("")
                        except Exception as error:
                            print("")
        
        for k in ob:
            print(k.name, k.lecc.name, k.lecc.quiz.name, k.lecc.quiz.estudiant)
                        
        print("--------------------------------------------")


        for Nquiz in listDEQuices:
            for f in allll:
                # for f in c:
                if Nquiz == f.quiz:
                    print(f.user, f.quiz, f.score, f.quiz.lessson, f.quiz.lessson.course)

        print("ÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑÑ")
        for f in allll:
            obc = Obcurso()
            obc.lecc = Obleccion()
            obc.lecc.quiz = Obquiz()
            obc.name = f.quiz.lessson.course
            obc.lecc.name = f.quiz.lessson
            obc.lecc.quiz.name = f.quiz
            obc.lecc.quiz.nota = f.score
            obc.lecc.quiz.estudiant = f.user
            ob.append(obc)
            print(f.user, f.quiz, f.score, f.quiz.lessson, f.quiz.lessson.course)
        
        print("--------------------------------------------")
        # obc = Obcurso()
        # obc.lecc = Obleccion()
        # obc.lecc.quiz = Obquiz()
        # obc.name = 1
        # obc.lecc.name = 1
        # obc.lecc.quiz.name = 1
        # obc.lecc.quiz.nota = 1
        # obc.lecc.quiz.estudiant = 1
        # ob.append(obc)

        for k in ob:
            print(k.name, k.lecc.name, k.lecc.quiz.name, k.lecc.quiz.estudiant, k.lecc.quiz.nota)
                        
        print("--------------------------------------------")


        Cu1 = []
        Cu2 = []
        Le2 = []
        Qu2 = []
        Es2 = []


        for k in ob:
            Le1 = []
            Qu1 = []
            a = [k.lecc.quiz.name, k.lecc.quiz.estudiant, k.lecc.quiz.nota]
            Qu1.append(a)
            b = [k.lecc.name,Qu1]
            Le1.append(b)
            c = [k.name,Le1]
            Cu1.append(c)


            Cu2.append(str(k.name))
            Le2.append(str(k.lecc.name))
            Qu2.append(str(k.lecc.quiz.name.id))
            Es2.append(str(k.lecc.quiz.estudiant))
            print(k.name, k.lecc.name, k.lecc.quiz.name, k.lecc.quiz.estudiant, k.lecc.quiz.nota)
        

        convetCU2_set =  set(Cu2)
        n1 = list(convetCU2_set)
        # n1.reverse()
        print(n1)


        convetCU2_set =  set(Le2)
        n2 = list(convetCU2_set)
        n2.reverse()

        # print(n2)

        

        convetCU2_set =  set(Qu2)
        n3 = list(convetCU2_set)
        # n3.reverse()


        
        convetCU2_set =  set(Es2)
        n4 = list(convetCU2_set)
        # n4.reverse()
        
        print(n4)

        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


        

        for m in Cu1:
            print(m[0])
            for n in m[1]:
                print(n[0])
                for h in n[1]:
                    for g in h:
                        print(g)

        
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")



        # for e in ob:
        #     if e.codigo not in resultantList:
        #         resultantList.append(element.codigo)
        #         listcourse.append(element)
        Lcurse2 = []

        for pos in n1:
            Lcurse1 = course.objects.filter(title=pos)
            if Lcurse1:
                Lcurse2.append(Lcurse1)

        
        for j in Lcurse2:
            print(j)


        
        Llesson2 = []

        for pos in n2:
            Llesson1 = Lesson.objects.filter(title=pos)
            if Llesson1:
                Llesson2.append(Llesson1)

        
        for j in Llesson2:
            print(j)
        

        LQuiz2 = []
        for pos in n3:
                LQuiz1 = Quiz.objects.filter(id=pos)
                if LQuiz1:
                    LQuiz2.append(LQuiz1)

        
        for j in LQuiz2:
            print(j)
        
        # for j in n3:
        #     print(j)


        



    
        for i in allll:

            print(i.user, i.quiz.lessson, i.score, i.quiz.name)

        
        print("antes de sacar promedio-------------")

        estudianteNotas = []

        
        for ei in claseEstudiante:
            ex1 = []
            for e in ei:
                print(e)
                estuX = []
                for i in allll:
                    for j in LQuiz2:
                        for k in j:
                            if i.quiz == k and i.user.username == e:
                                print(i.user, i.quiz.lessson, i.score, i.quiz.name)
                                estuX.append(i.score)
                            
                if estuX == []:
                    estuX.append(0)
                ex1.append(estuX)
            estudianteNotas.append(ex1)

        
        print(estudianteNotas)

        l = [5,7,3,1,87,3,465,41,21,56]
        mean = statistics.mean(l)

        print(max(l))
        print(mean)

        mediaDENotas = []

        for Enotas in estudianteNotas:
            auxN = []
            for nota1 in Enotas:
                media = statistics.mean(nota1)
                auxN.append(media)
            mediaDENotas.append(auxN)

        print(mediaDENotas)
        # mediaDENotasConuser = []
        # for e in n4:
        #     Nuser = [e]

        zz= []
        # zz.append(claseEstudiante)
        # zz.append(mediaDENotas)

        

        for k,i in enumerate(claseEstudiante):
            x = []
            x = [i]
            x.append(mediaDENotas[k])
            zz.append(x)

        
        print(zz)





        for jjkjk in LQuiz2:
            print(jjkjk)

        print("lista de quices ")
        for Nquiz in listDEQuices:
            print(Nquiz)

        listclases = []
        resultantList = []

        for element in clases:
            if element.codigo not in resultantList:
                resultantList.append(element.codigo)
                listclases.append(element)
        
        
        
        
        profGrupo = Grupo.objects.filter(profesor=self.request.user.profesor)
        print(profGrupo)
        
        profNotasGrupo = GrupoNotas.objects.filter(grupo=profGrupo.first())
        print(profNotasGrupo)
        
        print(Lcurse2)
        print(Llesson2)
        print(LQuiz2)
        
        todasLasNotasnombres = []
        todasLasNotas = []
        
        quizAndNotas = []
        
        for quiz in LQuiz2:
            # print(quiz.first() , " quiz")
            for nota in profNotasGrupo:
                # print(nota.nota.quiz , " nota")
                if nota.nota.quiz == quiz.first():
                    if not (quiz.first() in todasLasNotasnombres):
                        todasLasNotasnombres.append(quiz.first())
                        todasLasNotas.append(nota.nota)
                        quizAndNotas.append([quiz.first(), nota.nota])
                elif not (quiz.first() in todasLasNotasnombres):
                    todasLasNotasnombres.append(quiz.first())
                    todasLasNotas.append(0)
                    quizAndNotas.append([quiz.first(), 0])
        
        # for quiz in LQuiz2:
        #     # print(quiz.first() , " quiz")
        #     for nota in profNotasGrupo:
        #         # print(nota.nota.quiz , " nota")
        #         if nota.nota.quiz == quiz.first():
        #             if not ([quiz.first(), not None ] in quizAndNotas):
        #                 quizAndNotas.append([quiz.first(), nota.nota])
        #         elif not ([quiz.first(), not None ] in quizAndNotas):
        #             quizAndNotas.append([quiz.first(), 0])
        
        print("---------------")
        print(todasLasNotas)
        print(todasLasNotasnombres)
        print(quizAndNotas)
        
        for curso in profGrupo:
            # print(curso.first() , " curso")
            for lesson in Llesson2:
                print("")
                # print(lesson.first() , " lesson")
                        
                        # if quiz.first().lessson.course == curso.course and quiz.first().lessson == lesson.first():

                                
                        # if nota.nota.quiz == quiz.first() and nota.nota.quiz.lessson == lesson.first() and nota.nota.quiz.lessson.course == curso.first() :
        
        
        abbbet = []
        abbbet.append(['a',1])
        abbbet.append(['a',2])
        abbbet.append(['b',2])
        
        print(['a', not None] in abbbet)
        
        print(" profNotasGrupo ", profNotasGrupo)
        
        ordeando1 = profNotasGrupo.order_by('nota__user', 'nota__quiz__lessson','nota__quiz__name')
        
        for i in ordeando1:
            print(i.nota.user, " ", i.nota, " ", i.nota.quiz.lessson, " ", i.nota.quiz.lessson.course, ' ', i.nota.quiz.name )
        
        # print(ordeando1.all().values('nota', 'nota__user__username' ))
        print(ordeando1.all().values('nota', 'nota__user' ))
        # print(ordeando1.values('nota__user__username' ).annotate(sum( 'nota__score' ) ))
        
        print("ssssssssssssssssssss")
        for quiz in LQuiz2:
            for NotOrd in ordeando1:
                print(quiz, " ", NotOrd.nota)
                if quiz == NotOrd:
                    print(quiz, " ", NotOrd)
                else:
                    print(quiz, "  0")
                    
        todasLasNotasnombres = []
        todasLasNotas = []
    
        quizAndNotas = []
        
        print("ordeando1", ordeando1)
        print("LQuiz2", LQuiz2)
                    
        for quiz1 in LQuiz2:
            # print(quiz.first() , " quiz")
            for nota in ordeando1:
                # print(nota.nota.quiz , " nota")
                if nota.nota.quiz == quiz1.first():
                    if not (quiz1.first() in todasLasNotasnombres):
                        todasLasNotasnombres.append(quiz1.first())
                        todasLasNotas.append(nota.nota)
                        quizAndNotas.append([quiz1.first(), nota.nota])
                elif not (quiz1.first() in todasLasNotasnombres):
                    todasLasNotasnombres.append(quiz1.first())
                    todasLasNotas.append(0)
                    quizAndNotas.append([quiz1.first(), 0])
        
        print("---------------")
        print(todasLasNotas)
        print(todasLasNotasnombres)
        print(quizAndNotas)
        
        for i in quizAndNotas:
            print(i)
        
        
        # ulimoArray = []
        
        # print("@" * 18)
        # print(LQuiz2)
        
        # for i in LQuiz2:
        #     ulimoArray.append(i.first().name)
            
        # print("*" * 28)
        # print(ulimoArray)
        
        # newwaaa = []
        # newwaaa.append(
        #     {
        #         for i in ulimoArray:
        #             i : "0"            
        #             }
        # )
        
        # print(newwaaa)
        
        notasfinalahorasi = []
        
        print("aa"*32)
        
        for i in LQuiz2:
            print(i.first())
            
        estudiantesyNotas = []
        
        listaDeEstudiantesDelGrupo = Grupo.objects.filter(profesor=self.request.user.profesor)
            
        # for i in listaDeEstudiantesDelGrupo:
        #     resultado = filtroDeNotasGeneralesDelGrupo.filter(user=i.name)
        #     estudiantesyNotas.append(resultado)   
            
        #iterar el listaDeEstudiantesDelGrupo y dentro guardar los nombres y sus notas
        
        # for estud in listaDeEstudiantesDelGrupo:
        
        for quiz in LQuiz2:
            resultadoxd = ordeando1.filter(nota__quiz=quiz.first())
            resultadoxd = resultadoxd.first()
            if resultadoxd:
                notasfinalahorasi.append(resultadoxd)
            else:
                nombreclasescursos.append(0)
        
        print(notasfinalahorasi)
        for n in notasfinalahorasi:
            print(n.nota.score , " ", n.nota.user, " ", n.nota.quiz.name)

            
        print(listaDeEstudiantesDelGrupo)
        for grup in listaDeEstudiantesDelGrupo:
            print(grup.course)
        
        
        #obtiene todos los grupos del profesor
        profGrupo = Grupo.objects.filter(profesor=self.request.user.profesor)
        print(profGrupo)
        
        
        
        #obtener todas las notas por el grupo 
        List_profNotasGrupo = GrupoNotas.objects.none()
        List_profNotasGrupoArray = []
        for grupoprof in profGrupo:    
            profNotasGrupo = GrupoNotas.objects.filter(grupo=grupoprof)
            List_profNotasGrupoArray.append(profNotasGrupo)
            List_profNotasGrupo = List_profNotasGrupo | profNotasGrupo
        
        print(List_profNotasGrupo)
        
        # listadeTodasLasNotasAsOneArray = []
        # for grupnotaelemen in List_profNotasGrupo:
        #     print("e"*100)
        #     for Gnota in grupnotaelemen:
        #         print(Gnota.nota, " ", Gnota.nota.user, Gnota.nota.quiz)
        #         listadeTodasLasNotasAsOneArray.append(Gnota)
                
        print(LQuiz2)
        
        List_quicesPorCurso = []
        List_estudiantesPorCurso = []
        
        #obtener lista de quices y estudiantes separados por los grupos
        for grupoprof in profGrupo:
            quices = Quiz.objects.filter(lessson__course=grupoprof.course)
            List_quicesPorCurso.append(quices)
            estudiantes = GrupoEstudiante.objects.filter(grupo=grupoprof)
            List_estudiantesPorCurso.append(estudiantes)
            
        #junta la lista de los quices
        ListQuicesAsOneArray = Quiz.objects.none()
        for quicesG in List_quicesPorCurso:
            # for quiz in quicesG:
            ListQuicesAsOneArray = ListQuicesAsOneArray | quicesG
        
        #juntar las lista de los estudiantes
        ListEstudiantesAsOneArray = GrupoEstudiante.objects.none()
        for estudiantesG in List_estudiantesPorCurso:
            # for estudiante in estudiantesG:
            ListEstudiantesAsOneArray = ListEstudiantesAsOneArray | estudiantesG
                
            
        
        
        
        
        notasfinalahorasi2 = []
        #intento fallido de agregar 0 a las clases inexistentes
        
        # for estudianteGrupoN in List_estudiantesPorCurso:
        #     for estudiantex in estudianteGrupoN:
        #         for listadenotas in List_profNotasGrupo:
        #             for quizgrupo in List_quicesPorCurso:
        #                 for quiz in quizgrupo:
        #                     resultadoxd2 = listadenotas.filter(nota__quiz=quiz, nota__user=estudiantex.estudiante.user)
        #                     # resultadoxd2 = resultadoxd2.first()
        #                     if resultadoxd2:
        #                         notasfinalahorasi2.append(resultadoxd2)
        #                     # else:
        #                     #     notasfinalahorasi2.append(0)
            
        print("a"*100)
        print(notasfinalahorasi2)
        print("a"*100)
        print(List_quicesPorCurso)
        print("a"*100)
        for i in notasfinalahorasi2:
            print(i)
            # if i != 0:
            #     print(i.nota, " ",i.nota.user, " ", i.nota.quiz)
            # else: 
            #     print(i)
        
        print(List_estudiantesPorCurso)
        
        print(ListQuicesAsOneArray)
        print(ListEstudiantesAsOneArray)
        
        List_profNotasGrupo2 = GrupoNotas.objects.none()
        
        listaOrdenadaDeNotas = []
        listaOrdenadaDeNotasArrayCon0 = []
        for estudi in ListEstudiantesAsOneArray:
            print(type(estudi), " ", estudi.estudiante.user)
            for quiz in ListQuicesAsOneArray: 
                # print(quiz)
                # print(listadeTodasLasNotasAsOneArray(nota))
                if quiz.lessson.course==estudi.grupo.course:
                    # filtroNotaOrdenado = List_profNotasGrupo.filter(nota__quiz=quiz, nota__user=estudi.estudiante.user, nota__quiz__lessson__course=estudi.grupo.course).order_by('nota__user', 'nota__quiz__lessson','nota__quiz__name')
                    filtroNotaOrdenado = List_profNotasGrupo.filter(nota__quiz=quiz, nota__user=estudi.estudiante).order_by('nota__user', 'nota__quiz__lessson','nota__quiz__name')
                    listaOrdenadaDeNotas.append(filtroNotaOrdenado)
                    print("esta buscando ", quiz, " ", estudi.estudiante.user, " encontro:",filtroNotaOrdenado)
                    
                    if filtroNotaOrdenado:
                        listaOrdenadaDeNotasArrayCon0.append(
                            {
                                "nombre": filtroNotaOrdenado.first().nota.user,
                                "nota": filtroNotaOrdenado.order_by("-nota__score").first().nota.score,
                                "quiz": filtroNotaOrdenado.first().nota.quiz,
                                "grupo": estudi.grupo.course
                            }
                            
                            )
                    else:
                        listaOrdenadaDeNotasArrayCon0.append( {
                                "nombre": estudi.estudiante.user,
                                "nota": 0,
                                "quiz": quiz,
                                "grupo": estudi.grupo.course
                            })
                    
        """
        posible forma de buscar la nota maxima del estudiante
        from django.db.models import Max
        args = Argument.objects.filter(name='foo') # or whatever arbitrary queryset
        args.aggregate(Max('rating')) # {'rating__max': 5}
        """
                    
                    
        #recordar utilizar la lista de los grupos por profesor para volver a agrupar por grupo o clases con  profGrupo        
        #existe el problema que se estan buscando todos los quices para todos los estudiantes, arreglar eso
        print(type(List_profNotasGrupo))
        print(List_profNotasGrupoArray)
        for i in List_profNotasGrupoArray:
            print("aaaaaa")
            i_ordenado = i.order_by('nota__user', 'nota__quiz__lessson','nota__quiz__name')
            for notasordenadas in i_ordenado:
                print(notasordenadas)
                
        #prueba impresion
        print("p"*100)
        for i in listaOrdenadaDeNotas:
            print(i)
        
        notasOrdenadasPorGrupo = []
        notasParaOrdenadarPorGrupo = []
        ordenaNombreArray = []
        ordenaNombre = ""
        aa1 = []
        aa2 = []
        aa3 = []
        aa4 = []
        for h in profGrupo:
            for i in listaOrdenadaDeNotasArrayCon0:
                print(i["grupo"],i["nombre"], h.course)
                # aa3.append(
                    
                #     list(filter( lambda x: x['nombre'] == i["nombre"], listaOrdenadaDeNotasArrayCon0 ))
                # )
                if i["grupo"] == h.course:
                    aa1.append(i)
                    
                    if ordenaNombre == "":
                        ordenaNombre = i["nombre"]
                        ordenaNombreArray.append(i["nombre"])
                        ordenaNombreArray.append(i)
                        
                    # elif ordenaNombre == i["nombre"] and listaOrdenadaDeNotasArrayCon0[-1] == i:
                    #     ordenaNombreArray.append(i)
                    #     notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                    #     ordenaNombreArray = []
                        
                    # elif ordenaNombre != i["nombre"] and listaOrdenadaDeNotasArrayCon0[-1] == i:
                    #     notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                    #     ordenaNombreArray = []
                    #     ordenaNombre = i["nombre"]
                    #     ordenaNombreArray.append(i["nombre"])
                    #     ordenaNombreArray.append(i)
                    #     notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                    elif ordenaNombre == i["nombre"]:
                        # print(i.nota.user)
                        # print(i["nombre"], "               ", i["nota"], "            ", i["quiz"])
                        ordenaNombre = i["nombre"]
                        ordenaNombreArray.append(i)
                    elif ordenaNombre != i["nombre"]:
                        notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                        ordenaNombreArray = []
                        ordenaNombre = i["nombre"]
                        ordenaNombreArray.append(i["nombre"])
                        ordenaNombreArray.append(i)
                    else:
                        print("elsee"*29)
                        #antes estaba abajo y parecia funcionar 
                        # notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                        # ordenaNombreArray = []
                    # elif listaOrdenadaDeNotasArrayCon0[-1] == i:
                    #     ordenaNombreArray.append(i)
                    #     notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                    # else:
                    #     ordenaNombreArray.append(i)
                    #     notasParaOrdenadarPorGrupo.append(ordenaNombreArray)
                
                        
            # ordenaNombreArray = []
                # print("tt"*100)
                # print(notasParaOrdenadarPorGrupo)
            notasOrdenadasPorGrupo.append(notasParaOrdenadarPorGrupo)
            notasParaOrdenadarPorGrupo = []
            aa2.append(aa1)
            aa1 = []
            aa4.append(aa3)
            aa3 = []
            
            print("11"*100)
            for i in notasOrdenadasPorGrupo:
                print(i)
                print()
            print("11"*100)
        
        # guardado por si la prueba de juntar los nombres no funciona 
        # notasOrdenadasPorGrupo = []
        # notasParaOrdenadarPorGrupo = []
        # for h in profGrupo:
        #     for i in listaOrdenadaDeNotasArrayCon0:
        #         # print(i["grupo"])
        #         # print(h.course)
        #         if i["grupo"] == h.course:
                    
        #             # print(i.nota.user)
        #             print(i["nombre"], "               ", i["nota"], "            ", i["quiz"])
        #             notasParaOrdenadarPorGrupo.append(i)
        #     print(notasParaOrdenadarPorGrupo)
        #     notasOrdenadasPorGrupo.append(notasParaOrdenadarPorGrupo)
        #     notasParaOrdenadarPorGrupo = []
        
        
        
        #llenar una nueva lista solo con los numeros, y el nombre al principio, 
        #si es la posicion 0 de la lista agregar el nombre, sino agregar la nota 
        print("aaa"*100)
        notasOrdenadasParaelHtml = []
        notasOrdenadasParaelHtml2 = []
        notasOrdenadasParaelHtmlFull = []
        notasOrdenadasParaelHtmltitulos = []
        banderatituloInsertado = False
        for i in notasOrdenadasPorGrupo:
            for d in i:
                for j in d:
                    print(j, d[0])
                    if j == d[0]:
                        notasOrdenadasParaelHtmltitulos.append("nombre")
                        # notasOrdenadasParaelHtml.append(j.username)
                        notasOrdenadasParaelHtml.append(j)
                    else:
                        notasOrdenadasParaelHtmltitulos.append(j['quiz'].name)
                        notasOrdenadasParaelHtml.append(j['nota'])
                        # print()
                        # print(d)
                if banderatituloInsertado == False:
                    # notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtmltitulos)
                    notasOrdenadasParaelHtmltitulos=[]
                    banderatituloInsertado = True
                notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtml)
                notasOrdenadasParaelHtml= []
                notasOrdenadasParaelHtmltitulos=[]
            notasOrdenadasParaelHtmlFull.append(notasOrdenadasParaelHtml2)
            notasOrdenadasParaelHtml2 = []
            banderatituloInsertado = False
            
        for i in notasOrdenadasParaelHtmlFull:
            
            print(i)
            print()
        # df = pd.DataFrame(notasOrdenadasPorGrupo)
        # print(df)
        
        # df2 = df.groupby('nombre')['Fee'].apply(list)
        # print(df2)
        uu1 = []
        uu2 = []
        
        #primero se guardo los grupos, ahora se den guardar estudiantes
        nombresNotasOrd = []
        nombresNotasParaOrdenal = []
        llevaNombre = ""
        llevaNombreArray = []
        for a in aa2:
            print(a)
            # llevaNombre == ""
            llevaNombreArray = []
            for i in a:
                
                # print(i)
                if llevaNombre == "":
                    llevaNombre = i["nombre"]
                    llevaNombreArray.append(llevaNombre)
                    llevaNombreArray.append(i)
                    
                elif llevaNombre == i["nombre"] and a[-1] == i:
                    llevaNombreArray.append(i)
                    nombresNotasParaOrdenal.append(llevaNombreArray)
                    # llevaNombreArray = []
                    
                elif llevaNombre != i["nombre"] and a[-1] == i:
                    nombresNotasParaOrdenal.append(llevaNombreArray)
                    llevaNombreArray = []
                    llevaNombre = i["nombre"]
                    llevaNombreArray.append(i["nombre"])
                    llevaNombreArray.append(i)
                    nombresNotasParaOrdenal.append(llevaNombreArray)
                elif llevaNombre != i["nombre"] and a[0] == i:
                    # nombresNotasParaOrdenal.append(llevaNombreArray)
                    llevaNombreArray = []
                    llevaNombre = i["nombre"]
                    llevaNombreArray.append(i["nombre"])
                    llevaNombreArray.append(i)
                elif llevaNombre == i["nombre"]:
                    # print(i.nota.user)
                    # print(i["nombre"], "               ", i["nota"], "            ", i["quiz"])
                    llevaNombre = i["nombre"]
                    llevaNombreArray.append(i)
                elif llevaNombre != i["nombre"]:
                    nombresNotasParaOrdenal.append(llevaNombreArray)
                    llevaNombreArray = []
                    llevaNombre = i["nombre"]
                    llevaNombreArray.append(i["nombre"])
                    llevaNombreArray.append(i)
                else:
                    print("elsee"*29)
                    #antes estaba abajo y parecia funcionar 
                    # nombresNotasParaOrdenal.append(llevaNombreArray)
                    # llevaNombreArray = []
                # elif listaOrdenadaDeNotasArrayCon0[-1] == i:
                #     llevaNombreArray.append(i)
                #     nombresNotasParaOrdenal.append(llevaNombreArray)
                # else:
                #     llevaNombreArray.append(i)
                #     nombresNotasParaOrdenal.append(llevaNombreArray)
            nombresNotasOrd.append(nombresNotasParaOrdenal)
            nombresNotasParaOrdenal = []
            
            
            
        
            
        notasOrdenadasParaelHtmlDictionary = []
        notasOrdenadasParaelHtml = []
        notasOrdenadasParaelHtml2 = []
        notasOrdenadasParaelHtmlFull = []
        notasOrdenadasParaelHtmltitulos = []
        banderatituloInsertado = False
        for i in nombresNotasOrd:
            for d in i:
                for j in d:
                    # print(j, d[0])
                    if j == d[0]:
                        notasOrdenadasParaelHtmltitulos.append("nombre")
                        # notasOrdenadasParaelHtml.append(j.username)
                        notasOrdenadasParaelHtml.append(j)
                    else:
                        notasOrdenadasParaelHtmltitulos.append(j['quiz'].name)
                        notasOrdenadasParaelHtml.append(round(j['nota'],2))
                        # print()
                        # print(d)
                if banderatituloInsertado == False:
                    notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtmltitulos)
                    notasOrdenadasParaelHtmltitulos=[]
                    banderatituloInsertado = True
                notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtml)
                notasOrdenadasParaelHtml= []
                notasOrdenadasParaelHtmltitulos=[]
            
            
            print("d[1]",i[0][1]["grupo"] )            
            notasOrdenadasParaelHtmlFull.append(notasOrdenadasParaelHtml2)        
            notasOrdenadasParaelHtmlDictionary.append(
                {
                    "grupo": i[0][1]["grupo"],
                    'listaEstNot':  notasOrdenadasParaelHtml2
                }
            )
            notasOrdenadasParaelHtml2 = []
            banderatituloInsertado = False
            
        # print("nombresNotasOrd")
        # for i in nombresNotasOrd:
        #     print()
        #     print(i)
        # for i in aa2:
        #     uu1.append(
                    
        #             list(filter( lambda x: x['nombre'] == i["nombre"], aa2 ))
        #         )
        #     print(i)
            
        # print(uu1)
            
        # for i in aa4:
        #     print(i)
            
        # for estudi in ListEstudiantesAsOneArray:
        
        # for i in notasOrdenadasPorGrupo:
        #     print(i)
        #     print("--"*22)
        
        
        
            
        for i in notasOrdenadasParaelHtmlDictionary:
            print(i["grupo"])
            print(i["listaEstNot"])
            
        
        for i in claseEstudiante:
            print(i)
            
        for i in zz:
            print(i)
            print()
            
        
        
        
        
        listaNombresEstudiantes = []
        listaNombresEstudiantesfull = []
        promedioEstudiantes = []
        
        # notasOrdenadasParaelHtmlFullpop = notasOrdenadasParaelHtmlFull.copy()
        notasOrdenadasParaelHtmlFullpop = deepcopy(notasOrdenadasParaelHtmlFull)
        
        # def popstr(elemento):
        #     newpersona = elemento.copy()
        #     newpersona.pop(0)
        #     # persona["altura"] = persona["edad"] / 2
        #     # return persona
        #     return newpersona


        # notasOrdenadasParaelHtmlFullpop = list(map(popstr, notasOrdenadasParaelHtmlFull))
    
        
        
        for i in notasOrdenadasParaelHtmlFullpop:
            print()
            # newi = i.copy()
            i.pop(0)
        
        # def poplist(elem, listaNombresEstudiantes):
        #     newelem = elem.copy()
        #     for j in newelem:
        #         listaNombresEstudiantes.append(j.pop(0))
        #     listaNombresEstudiantesfull.append(listaNombresEstudiantes)
        #     return(listaNombresEstudiantesfull)
        
        # notasOrdenadasParaelHtmlFullpop2 = list(map(poplist, notasOrdenadasParaelHtmlFullpop, listaNombresEstudiantes))
        
        print("se van a imprimir los pop ordenadas")
        for i in notasOrdenadasParaelHtmlFullpop:
            print()
            print(i)
        for i in notasOrdenadasParaelHtmlFullpop:
            listaNombresEstudiantes = []
            for j in i:
                listaNombresEstudiantes.append(j.pop(0))
            listaNombresEstudiantesfull.append(listaNombresEstudiantes)
        
        print(listaNombresEstudiantesfull)
        
        
        promedionotas = []
        promedionotasFull = []
        for i in notasOrdenadasParaelHtmlFullpop:
            promedionotas = []
            for j in i:
                mean = statistics.mean(j)
                promedionotas.append(mean)
            promedionotasFull.append(promedionotas)

            
        
        print(listaNombresEstudiantesfull)
        print(promedionotasFull)
        
        promedioNotasMerge = []
        for k,i in enumerate(listaNombresEstudiantesfull):
            x = []
            x = [i]
            x.append(promedionotasFull[k])
            promedioNotasMerge.append(x)
        
        print(promedioNotasMerge)
        print(claseEstudiante)
        # notasOrdenadasParaelHtmlDictionary2 = []
        # notasOrdenadasParaelHtml = []
        # notasOrdenadasParaelHtml2 = []
        # notasOrdenadasParaelHtmlFull2 = []
        # notasOrdenadasParaelHtmltitulos = []
        # banderatituloInsertado = False
        # for i in nombresNotasOrd:
        #     for d in i:
        #         for j in d:
        #             # print(j, d[0])
        #             if j != d[0]:
        #                 notasOrdenadasParaelHtmltitulos.append("nombre")
        #                 notasOrdenadasParaelHtml.append(j.username)
        #                 notasOrdenadasParaelHtmltitulos.append(j['quiz'].name)
        #                 notasOrdenadasParaelHtml.append(round(j['nota'],2))
        #             else:
        #                 # print()
        #                 # print(d)
        #         if banderatituloInsertado == False:
        #             notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtmltitulos)
        #             notasOrdenadasParaelHtmltitulos=[]
        #             banderatituloInsertado = True
        #         notasOrdenadasParaelHtml2.append(notasOrdenadasParaelHtml)
        #         notasOrdenadasParaelHtml= []
        #         notasOrdenadasParaelHtmltitulos=[]
            
        #     print("d[1]",i[0][1]["grupo"] )            
        #     notasOrdenadasParaelHtmlFull2.append(notasOrdenadasParaelHtml2)        
        #     notasOrdenadasParaelHtmlDictionary2.append(
        #         {
        #             "grupo": i[0][1]["grupo"],
        #             'listaEstNot':  notasOrdenadasParaelHtml2
        #         }
        #     )
        #     notasOrdenadasParaelHtml2 = []
        #     banderatituloInsertado = False
        
        
        print(notasOrdenadasParaelHtmlDictionary)
        context = {
            'profGrupo': profGrupo,
            'profNotasGrupo': profNotasGrupo,
            'datosChart' : datosChart,
            'estudiante': estudiante,
            'clases': clases,
            'listaCursos': listcourse,
            'claseEstudiante': claseEstudiante,
            'TodosLosDatos': ob,
            'listaLecciones': n2,
            'listaQuices2': LQuiz2,
            'listaQuices': n3,
            'listaEstudiantes': n4,
            'C': Cu1,
            'Lcurse2': Lcurse2,
            'Llesson2': Llesson2,
            'LQuiz2': LQuiz2,
            'mediaDENotas': mediaDENotas,
            'ListResultados': allll,
            'zz': zz,
            'listclases': listclases,
            'notasOrdenadasParaelHtmlFull': notasOrdenadasParaelHtmlFull,
            'notasOrdenadasParaelHtmlDictionary': notasOrdenadasParaelHtmlDictionary,
            'promedioNotasMerge':promedioNotasMerge,
            'listaNombresEstudiantesfull':listaNombresEstudiantesfull


        }


        return context


    def all(self):
        p = self.request.user
        n = []
        for i in range(0,5):
            n.append(i)
        print(p,"++++++++++++++++++++++++++++++++++++++")
        return n

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def get_context_data(self ,**kwargs):
        context = super().get_context_data(**kwargs)
        context["all"] = self.all()
        context["p"] = self.p()
        return context


