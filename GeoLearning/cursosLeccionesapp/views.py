# Create your views here.
from gamesUnityapp.models import Score_juegos_Group
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from .models import course, Lesson, Comment, parrafoLeccion, GrupoNotas, GrupoEstudiante, Grupo

from django.contrib.auth.models import User

from usersapp.models import Profesor
from .models import Quiz

from .forms import MiFormSet, MiFormulario

# Create your views here.
from django.forms import formsets

from .forms import BaseExtraFormSet, ExtraForm
from usersapp.forms import ProfileForm

from .forms import NameForm, formset_factory, QuizForm, AnswerForm,QuestionForm

from .forms import GrupoForm, GrupoForm_CRUD
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def tabla_por_grupo(id_grupo):
    estudiantesPorGrupo = GrupoEstudiante.objects.filter(grupo = id_grupo)
    estudiantes_Score_juegos_lesson = Score_juegos_Group.objects.filter(juego_group=id_grupo, estudiante__in = [estu.estudiante for estu in estudiantesPorGrupo])
    print(estudiantesPorGrupo)
    print(estudiantes_Score_juegos_lesson)
    try:
        
        estudiantes_con_suma = estudiantes_Score_juegos_lesson.values('estudiante').annotate(total_score=Sum('score'))
        # estudiantes_con_suma = Score_juegos_lesson.objects.values('estudiante').annotate(total_score=Sum('score'))

        estudiantes = Estudiante.objects.filter(pk__in=[item['estudiante'] for item in estudiantes_con_suma])

        clasificacion = []
        for estudiante_con_suma in estudiantes_con_suma:
            estudiante = estudiantes.filter(pk=estudiante_con_suma['estudiante']).first()
            if estudiante:
                estudiante_con_suma['estudiante_obj'] = estudiante
                clasificacion.append(estudiante_con_suma)

        clasificacion = sorted(clasificacion, key=lambda x: x['total_score'], reverse=True)
        return clasificacion

        # clasificacion = Score_juegos_lesson.objects.all()
        # clasificacion = Score_juegos_lesson.objects.values(estudiante_obj=F('estudiante')).annotate(total_score=Sum('score')).order_by('-total_score')
    except Exception as error:
        clasificacion = []
        return clasificacion

def eliminar_juego_cf(request, id_juego):
    objeto = get_object_or_404(test_True_false, id=id_juego)
    grupo = objeto.grupofk
    nombre = objeto.name
    objeto.delete()
    mensaje = "¡El juego " + nombre + " se eliminó !"
    tipo_alerta = "success"
    messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
    return redirect('courses:detalles_grupo', grupo_id=grupo.id)

def eliminar_juego_carta(request, id_juego):
    objeto = get_object_or_404(Lesson_cards, id=id_juego)
    grupo = objeto.grupofk
    nombre = objeto.name
    objeto.delete()
    mensaje = "¡El juego " + nombre + " se eliminó !"
    tipo_alerta = "success"
    messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
    return redirect('courses:detalles_grupo', grupo_id=grupo.id)

@login_required
def mis_grupos(request):
    
    usuario_sesion = request.user 

    if hasattr(usuario_sesion, 'estudiante'):

        return redirect('view_grupo_general', id_grupo="general")
    else:
        return redirect('courses:detalles_grupo', grupo_id="general")
 
@login_required
def detalles_grupo(request, grupo_id):
    mensajeVacio = ''
    if grupo_id == 'general':
        #grupoEstudiante = GrupoEstudiante.objects.filter(estudiante=request.user).order_by('?').first()
        #grupo = grupoEstudiante.grupo
        grupo = Grupo.objects.filter(profesor__user=request.user).order_by('?').first()
        juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
        test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
    else:
        grupo = Grupo.objects.get(pk=grupo_id)
        
        juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
        test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
    
    #agregar una comparacion del profesor que accede sea el mismo que tiene control del grupo

    profesor_id = request.user  # Aquí puedes cambiar el ID del profesor
    if request.method == 'POST':
        form = GrupoForm(request.POST, profesor_id=profesor_id)
        if form.is_valid():
            # ...
            print('valid')
            grupo = form.cleaned_data['grupo']
            
            print(form.cleaned_data['grupo'])
            print(type(form.cleaned_data['grupo']  ))
            juegos_carta_por_grupo = Lesson_cards.objects.filter(grupofk = grupo)
            test_True_false_por_grupo = test_True_false.objects.filter(grupofk = grupo)
    else:
        form = GrupoForm(profesor_id=profesor_id)
    #return render(request, 'mi_vista.html', {'form': form})
    if grupo:
        clasificacion = tabla_por_grupo(grupo.id)
        mensajeVacio = ''
    else:
        grupo = []
        clasificacion = []
        mensajeVacio = 'No ha creado ningún grupo'
    
    context = { 
               'grupo': grupo,
               'juegos_cartas': juegos_carta_por_grupo,
               'juegoTF': test_True_false_por_grupo,
               'form': form,
               'clasificacion': clasificacion,
               'mensajeVacio': mensajeVacio
               }
    

    return render(request, 'cursosLeccionesapp/detalles_grupo.html', context)
    
@login_required
def crea_grupo(request):
    boton_del = 0
    profesor = request.user.profesor
    
    if request.method == 'POST':
        form = GrupoForm_CRUD(request.POST,  request.FILES)
        print("entro en el post")
        print(form.errors)
        if form.is_valid():

            grupo = form.cleaned_data
            
            id = grupo['id']
            name = grupo['name']
            #course = grupo['course']
            description = grupo['description'] 
            privado = grupo['privado'] 
            imagen = grupo['imagen_grupo']
            
            if id:
                guarda_grupo = Grupo.objects.get(id= id)
                guarda_grupo.name = name
                guarda_grupo.description = description
                guarda_grupo.privado = privado
                if imagen:
                    guarda_grupo.imagen_grupo = imagen
                guarda_grupo.save()
            else:
                grupo_save = Grupo(name= name, description= description, privado= privado, profesor= profesor, imagen_grupo = imagen)
                grupo_save.save()
            
            
            
            mensaje = "¡El grupo " + name + " se guardó correctamente !"
            tipo_alerta = "success"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return redirect('details_profile')  
    else:
        # mensaje = form.errors
        # tipo_alerta = "warning"
        # messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
        form = GrupoForm_CRUD(initial={'profesor': profesor})
        # boton_del = 1
        
    errors = None
    if request.method == 'POST':
        errors = form.errors
    
    context = {'form': form,'boton_del': boton_del, 'errors': errors}
    return render(request, 'cursosLeccionesapp/crea_grupo.html', context )

@login_required
def edit_grupo(request, grupo_id):
    grupo = Grupo.objects.get(pk=grupo_id)
    form = GrupoForm_CRUD(instance=grupo)
    context = {'form': form,
               'boton_del': 1,
               'id':grupo.id}
    return render(request, 'cursosLeccionesapp/crea_grupo.html', context )
    
@login_required
def delete_grupo(request):
    print('no entro')
    if request.method == 'POST':
        el_id = request.POST.get('texto', '')
        el_grupo = get_object_or_404(Grupo, pk=el_id)
        name = el_grupo.name
        el_grupo.delete()
        
        mensaje = "¡El grupo  " + name + " se eliminó correctamente !"
        tipo_alerta = "success"
        messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
        
        return redirect('details_profile')  
    return render(request, 'cursosLeccionesapp/crea_grupo.html' )
    
    
    
@login_required
def salirse_grupo_estudiante(request):

    if request.method == 'POST':
        estudiante = request.user.estudiante 
        el_id = request.POST.get('texto', '')
        el_grupo = get_object_or_404(GrupoEstudiante,grupo_id=el_id, estudiante=estudiante)
        name = el_grupo.grupo.name
        el_grupo.delete()
        
        mensaje = "¡Te has salido del grupo " + name + " correctamente."
        tipo_alerta = "success"
        messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
        
        
    return redirect('details_profile') 
    
    
    
    
@login_required
def unirse_grupo(request, grupo_id):
    
    
    
    if request.method == 'POST':
        
        el_codigo = request.POST.get('texto', '')
        estudiante = request.user.estudiante 
        el_grupo = Grupo.objects.filter(codigo_unico = el_codigo )
        
        if el_grupo.exists():
            el_grupo = el_grupo.first()
            if GrupoEstudiante.objects.filter(grupo=el_grupo , estudiante=estudiante).exists():
                mensaje = "Usted ya está en el grupo seleccionado"
                tipo_alerta = "warning"
                messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
                return redirect('courses:lista_grupo')
            else:
                estudianteGrupo = GrupoEstudiante(grupo=el_grupo , estudiante=estudiante)
                estudianteGrupo.save()
                mensaje = "¡Usted Ahora es parte del grupo " + el_grupo.name + " !"
                tipo_alerta = "success"
                messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
        else:
            mensaje = "El código introducido no pertenece a ningún grupo"
            tipo_alerta = "warning"
            messages.add_message(request, getattr(messages, tipo_alerta.upper()), mensaje)
            return redirect('courses:lista_grupo')
            
          
        
    return redirect('details_profile') 

@login_required
def lista_grupo(request):
    
    usuario_sesion = request.user 

    
    if hasattr(usuario_sesion, 'estudiante'):
        estudiante = usuario_sesion.estudiante
   
        grupos_estudiantes_esta = GrupoEstudiante.objects.filter(estudiante=estudiante)
        
        grupos_estudiantes_esta = [ grupo.grupo_id for grupo in grupos_estudiantes_esta  ]
    else:
        grupos_estudiantes_esta = None
        

    list_grupos = Grupo.objects.filter(privado=False)

    context = {
        'list_grupos': list_grupos,
        'grupos_estudiantes_esta': grupos_estudiantes_esta,
        
        }
    
    return render(request, 'cursosLeccionesapp/lista_grupo.html', context)

def list_quices(request, grupo):
    print(grupo)
    id_grupo = grupo
    list_Q = Quiz.objects.filter(fk_grupo=grupo)
    grupo = ''
    
    if list_Q.exists():
        grupo = list_Q.first().fk_grupo.course
    context = {
        'grupo': grupo,
        'list_Q': list_Q,
        'id_grupo': id_grupo
    }
    return render(request, 'cursosLeccionesapp/list_quices.html', context)

def delete_quiz(request, grupo):
    
    quiz_n = Quiz.objects.get(id=grupo)
    id_grupo = quiz_n.fk_grupo.id
    quiz_n.delete()
    print(id_grupo)
    
    return redirect("courses:list_quices",grupo=id_grupo)

def edit_quiz2(request, quiz):
    NameFormSet = formset_factory(AnswerForm, extra=0)
    print('')
    
    if request.method == 'POST':
        formset = NameFormSet(request.POST)
        if formset.is_valid():
            names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
            
            print(names)
            for i in formset:
                print(i)
            initial_data = names
                
            formset = NameFormSet(initial=initial_data)

            return render(request, 'cursosLeccionesapp/form_edit_quiz.html', {'formset': formset, 'names':names, 'quiz':quiz})        
            # return redirect('success')
    
        names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
        initial_data = names
        
        # for i in formset:
        #     print(i)
        
        # LosAs_p = list( filter( lambda x: x != {} , [form.as_p for form in formset ])) 
        # print(LosAs_p)
        
        formset = NameFormSet(initial=initial_data)
        print('post no valido')
        

    else:
        formset = NameFormSet(prefix='form')
        print('no')

    return render(request, 'cursosLeccionesapp/form_edit_quiz.html', {'formset': formset, 'quiz':quiz})

def delete_questions(id_quiz,lista):
    
    all_question_quiz = Question.objects.filter(quiz=id_quiz)
    print(all_question_quiz)
    print("!"*10)
    
    preguntas = all_question_quiz.exclude(pk__in=lista)
    print(preguntas)
    preguntas.delete()
    
    

def create_quiz(request, grupo):
    # NameFormSet = formset_factory(AnswerForm, extra=0)
    questForm =  formset_factory(QuestionForm, extra=0)
    
    # quizForm = QuizForm()
    
    datos_grupo = Grupo.objects.get(id=grupo)
    list_lesson = Lesson.objects.filter(course=datos_grupo.course)
    print(list_lesson)    
    producto_choices = [(producto.id, producto.title) for producto in list_lesson]
    quizForm = QuizForm(lessson_choices = producto_choices)
    print('')
    print(quizForm)
    
    
    if request.method == 'POST':
        questFormset = questForm(request.POST, prefix='formb')
        quizForm = QuizForm(request.POST)
        
        print(quizForm.is_valid())
        print(quizForm.cleaned_data)
        
  
        if quizForm.is_valid() and questFormset.is_valid() :

            names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
            initial_data = names

            questFormset = questForm(initial=initial_data, prefix='formb')
            
            F_quiz = quizForm.cleaned_data
            
            fk_grupo_ = Grupo.objects.get(id=grupo)
       
            quiz_name = F_quiz['name']
            quiz_difficult = F_quiz['difficluty'] 
            quiz_lesson = F_quiz['lessson']
            quiz_required_score_to_pass = F_quiz['required_score_to_pass']
            quiz_time = F_quiz['time']
            
            quiz_fk_grupo = fk_grupo_ 
            # quiz_fk_grupo = F_quiz['fk_grupo'] 
            
            objetoQuizForm = Quiz(
                name=quiz_name,
                topic='a',
                number_of_questions=len(names ),
                time=quiz_time,
                difficluty=quiz_difficult,
                required_score_to_pass=quiz_required_score_to_pass,
                lessson=quiz_lesson,
                fk_grupo=quiz_fk_grupo
            )

            objetoQuizForm.save()
            

            for formulario in names:
                
                quest_text=formulario['text']
                quest_text_n =formulario['text_n']
                
                objetoQuestion = get_or_create_question(quest_text_n, quest_text, objetoQuizForm)
                
                answer_id_1 = formulario['opcion_1_n']
                answer_text1 = formulario['opcion_1']
                answer_correct1 = formulario['opcion_1_check']
                
                
                get_or_create_data(objetoQuestion, answer_id_1, answer_text1, answer_correct1)

                answer_id_2 = formulario['opcion_2_n']
                answer_text2 = formulario['opcion_2']
                answer_correct2 = formulario['opcion_2_check']
                

                get_or_create_data(objetoQuestion, answer_id_2, answer_text2, answer_correct2)

                answer_id_3 = formulario['opcion_3_n']
                answer_text3 = formulario['opcion_3']
                answer_correct3 = formulario['opcion_3_check']
                get_or_create_data(objetoQuestion, answer_id_3, answer_text3, answer_correct3)

                answer_id_4 = formulario['opcion_4_n']
                answer_text4 = formulario['opcion_4']
                answer_correct4 = formulario['opcion_4_check']
                get_or_create_data(objetoQuestion, answer_id_4, answer_text4, answer_correct4)
                
            
            questFormset, quizForm = get_forms(objetoQuizForm,questForm, quizForm, producto_choices)
            
            # print(questFormset)
            # print(quizForm) 
        
            context = {
                # 'formset': formset, 
                'names':names,
                'quizForm': quizForm,
                'questForm':questFormset,
                'quiz': objetoQuizForm.id,
                'grupo':objetoQuizForm.fk_grupo.id,
                "Name_quiz":objetoQuizForm.name
                # 'sublistas': sublistas
                }

            return render(request, 'cursosLeccionesapp/form_edit_quiz.html', context)
            #return redirect("courses:list_quices",grupo=id_grupo)
            # return redirect('success')

        # formset.is_valid()
        # names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
        # pp = list( filter( lambda x: x != {} , [form.as_p for form in formset ])) 
        # initial_data = names
        
        # for i in pp:
        #     print(i)
        # print(names)

        # formset = NameFormSet(initial=initial_data, prefix='forma')
        
        questFormset.is_valid()
        names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
  
        initial_data = names
        print(names)

        questFormset = questForm(initial=initial_data, prefix='formb')
        print('post no valido')
        

    else:
        # formset = NameFormSet(prefix='forma')
        questFormset =  questForm(prefix='formb')
        print('no')
        
    context = {
        # 'formset': formset,
        'quizForm':quizForm,
        'questForm': questFormset
        }

    return render(request, 'cursosLeccionesapp/form_create_quiz.html', context)


def comprobar_respuesta(respuesta):
    if Answer.objects.filter(id=respuesta['id']).exists():
        return(respuesta)
    else:
        return False
        
        
def saveForm(iteracion, answer):
    pass


def get_forms(datos_Quiz,questForm, quizForm,producto_choices):

    setattr(quizForm, datos_Quiz.name, 1)
    setattr(quizForm, datos_Quiz.difficluty, 2)
    setattr(quizForm, str (datos_Quiz.lessson) , 3)
    setattr(quizForm, str(datos_Quiz.fk_grupo) , 4)
    # setattr(quizForm, str(datos_Quiz.id) , 5)
    setattr(quizForm, str(datos_Quiz.id) , 5)
    
    initial_data = [{'name':datos_Quiz.name}]
    
    quizForm = QuizForm(instance=datos_Quiz,lessson_choices = producto_choices)
    

    
    preguntas = Question.objects.filter(quiz=datos_Quiz)
    
    lista_preguntas = []
    for n_pregunta in preguntas:
        respuestas = Answer.objects.filter(question=n_pregunta)
        lista_preguntas.append(respuestas)
    
    
    print(lista_preguntas)
    
    dict_preguntas = []
    for l_respuestas in lista_preguntas:
        pregunta = {
            'text':l_respuestas[0].question.text , 
            'text_n':l_respuestas[0].question.id , 
            'opcion_1': l_respuestas[0].text,
            'opcion_1_n': l_respuestas[0].id,
            'opcion_1_check':l_respuestas[0].correct,
            'opcion_2':l_respuestas[1].text, 
            'opcion_2_n':l_respuestas[1].id, 
            'opcion_2_check': l_respuestas[1].correct,
            'opcion_3':l_respuestas[2].text,
            'opcion_3_n':l_respuestas[2].id,
            'opcion_3_check': l_respuestas[2].correct,
            'opcion_4':l_respuestas[3].text,
            'opcion_4_n':l_respuestas[3].id,
            'opcion_4_check': l_respuestas[3].correct,

        }
        
        dict_preguntas.append(pregunta)
    

        
        
    initial_data = dict_preguntas
  
    
    questFormset =  questForm(prefix='formb', initial=initial_data)
    
    return questFormset, quizForm
    

def get_or_create_data(question, id, answertext, answerCorrect):
    
    respuesta = Answer.objects.filter(id=id, question=question)
    
    if respuesta.exists():
        respuesta = respuesta.first()
        
        respuesta.text = answertext
        respuesta.correct=answerCorrect
        respuesta.save() 
        return respuesta
    else:
        respuesta = Answer(question=question, text=answertext, correct=answerCorrect)
        respuesta.save()
        return respuesta
    
def get_or_create_question(id, questionText, questionQuiz):
    
    
    
    respuesta = Question.objects.filter(id=id, quiz=questionQuiz)
    
    if respuesta.exists():
        respuesta = respuesta.first()
        
        respuesta.text = questionText
        respuesta.save() 
        return respuesta
    else:
        respuesta = Question(quiz=questionQuiz, text=questionText)
        respuesta.save()
        return respuesta
    
    
def get_or_create_Quiz(id, questionText, questionQuiz):
    
    respuesta = Question.objects.filter(id=id, quiz=questionQuiz)
    
    if respuesta.exists():
        respuesta = respuesta.first()
        
        respuesta.text = questionText
        respuesta.save() 
        return respuesta
    else:
        respuesta = Question(quiz=questionQuiz, text=questionText)
        respuesta.save()
        return respuesta
        

def edit_quiz(request,quiz):
    datos_Quiz = Quiz.objects.get(id=quiz)
    # NameFormSet = formset_factory(AnswerForm, extra=0)
    questForm =  formset_factory(QuestionForm, extra=0)
    
    list_lesson = Lesson.objects.filter(course=datos_Quiz.lessson.course)
    print(list_lesson)    
    producto_choices = [(producto.id, producto.title) for producto in list_lesson]
    quizForm = QuizForm(lessson_choices = producto_choices)
    # quizForm = QuizForm()
    
    
    print('')
    if request.method == 'POST':
        # formset = NameFormSet(request.POST, prefix='forma')
        questFormset = questForm(request.POST, prefix='formb')
        quizForm = QuizForm(request.POST)
        
        print(quizForm.is_valid())
        print(quizForm.cleaned_data)
        
        
        
        
        # sublistas = []
        # numero_quest = 0
        # for i in range(0, len(formset), 4):
        #     # Get the sublist
        #     sublista = []
        #     print(questFormset[numero_quest])
        #     sublista.append(questFormset[numero_quest])
        #     sublista.extend(formset[i:i+4]) 
        #     # sublista = formset[i:i+4]
        #     # Append the sublist to the list of sublists
        #     sublistas.append(sublista)
        #     print(numero_quest)
        #     numero_quest += 1
        #     # print(sublistas)
            
        
        
        # if quizForm.is_valid() and formset.is_valid() and questFormset.is_valid() :
        if quizForm.is_valid() and questFormset.is_valid() :

            # names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
            # initial_data = names
            # print(names)
            
                
            # formset = NameFormSet(initial=initial_data, prefix='forma')
            
            names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
            initial_data = names

            questFormset = questForm(initial=initial_data, prefix='formb')
            
            # print(names)
            # print(quizForm.cleaned_data)
            
            # print(quizForm)
            F_quiz = quizForm.cleaned_data
       
            
            # print(F_quiz['name'] )
            # print(F_quiz['difficluty'] )
            # print(type(F_quiz['lessson'])   )
            # print(F_quiz['fk_grupo'] )
            
            
            # quiz_id = F_quiz['id']
            quiz_name = F_quiz['name']
            quiz_difficult = F_quiz['difficluty'] 
            quiz_lesson = F_quiz['lessson']
            # quiz_fk_grupo = F_quiz['fk_grupo'] 
            
            quiz_required_score_to_pass = F_quiz['required_score_to_pass']
            quiz_time = F_quiz['time']
            
            
            
            objetoQuizForm = datos_Quiz
            objetoQuizForm.name = quiz_name
            objetoQuizForm.difficluty = quiz_difficult
            objetoQuizForm.time = quiz_time
            objetoQuizForm.required_score_to_pass = quiz_required_score_to_pass
            objetoQuizForm.number_of_questions = len(names)
            
            objetoQuizForm.save()
            
            # objetoQuizForm =  Quiz.objects.get(
            #      id=datos_Quiz.id,
            #                         name=quiz_name,
            #                        topic='a',
            #                        number_of_questions=4,
            #                        time=20,
            #                     difficluty=quiz_difficult,
            #                            required_score_to_pass=4,
            #                            lessson=quiz_lesson,
            #                            fk_grupo=datos_Quiz.fk_grupo
            #                            )
            # objetoQuizForm =  Quiz(name=quiz_name,
            #                        topic='a',
            #                        number_of_questions=4,
            #                        time=20,
            #                     difficluty=quiz_difficult,
            #                            required_score_to_pass=4,
            #                            lessson=quiz_lesson,
            #                            fk_grupo=quiz_fk_grupo
            #                            )
            
            # print('objetonquiz  ',objetoQuizForm)
            objetoQuizForm.save()
            
            # itera_n_orden = 1
            lista_id_contiene = []
            for formulario in names:
                
                # print(formulario['text'])
                quest_text=formulario['text']
                quest_text_n =formulario['text_n']
                
                objetoQuestion = get_or_create_question(quest_text_n, quest_text, objetoQuizForm)
                
                lista_id_contiene.append(objetoQuestion.id)
                
                
                # objetoQuestion , created = Question.objects.get_or_create(
                #     id = quest_text_n,
                #     # text=quest_text,
                #     quiz=objetoQuizForm
                #     )
                # # objetoQuestion = Question(text=quest_text,quiz=objetoQuizForm)
                # # print('objeto', objetoQuestion)
                
                # objetoQuestion.text = quest_text
                # objetoQuestion.save()
                
                # print(formulario['opcion_1'])
                # print(formulario['opcion_1_check'])
                
                
                answer_id_1 = formulario['opcion_1_n']
                answer_text1 = formulario['opcion_1']
                answer_correct1 = formulario['opcion_1_check']
                
                
                get_or_create_data(objetoQuestion, answer_id_1, answer_text1, answer_correct1)
                
                # answer1 , created = Answer.objects.get_or_create(
                #     # text=answer_text1,
                #                 #  correct=answer_correct1,
                #                  question=objetoQuestion,
                #                  id=answer_id_1
                #                  )
                # # answer1 = Answer(text=answer_text1,
                # #                  correct=answer_correct1,
                # #                  question=objetoQuestion
                # #                  )
                
                # # print(answer1)
                # # itera_n_orden+=itera_n_orden
                # answer1.text = formulario['opcion_1']
                # answer1.correct = formulario['opcion_1_check']
                # answer1.save()
                
                answer_id_2 = formulario['opcion_2_n']
                answer_text2 = formulario['opcion_2']
                answer_correct2 = formulario['opcion_2_check']
                
                
                
                get_or_create_data(objetoQuestion, answer_id_2, answer_text2, answer_correct2)
                # answer2 , created = Answer.objects.get_or_create(
                #     # text=answer_text2,
                #                 #  correct=answer_correct2,
                #                  question=objetoQuestion,
                #                 #  n_orden=itera_n_orden,
                #                  id = answer_id_2
                                 
                #                  )
                # # answer2 = Answer(text=answer_text2,
                # #                  correct=answer_correct2,
                # #                  question=objetoQuestion
                # #                  )
                
                # # print(answer2)
                # # itera_n_orden+=itera_n_orden
                # answer2.text = formulario['opcion_2']
                # answer2.correct = formulario['opcion_2_check']
                # answer2.save()
                
                answer_id_3 = formulario['opcion_3_n']
                answer_text3 = formulario['opcion_3']
                answer_correct3 = formulario['opcion_3_check']
                get_or_create_data(objetoQuestion, answer_id_3, answer_text3, answer_correct3)
                
                # answer3 , created = Answer.objects.get_or_create(
                #     # text=answer_text3,
                #                 #  correct=answer_correct3,
                #                  question=objetoQuestion,
                #                 #  n_orden=itera_n_orden,
                #                  id= answer_id_3
                                 
                #                  )
                # # answer3 = Answer(text=answer_text3,
                # #                  correct=answer_correct3,
                # #                  question=objetoQuestion
                # #                  )
                
                # # print(answer3)
                # # itera_n_orden+=itera_n_orden
                # answer3.text = formulario['opcion_3']
                # answer3.correct = formulario['opcion_3_check']
                # answer3.save()
                
                answer_id_4 = formulario['opcion_4_n']
                answer_text4 = formulario['opcion_4']
                answer_correct4 = formulario['opcion_4_check']
                get_or_create_data(objetoQuestion, answer_id_4, answer_text4, answer_correct4)
                # answer4 , created = Answer.objects.get_or_create(
                #     # text=answer_text4,
                #                 #  correct=answer_correct4,
                #                  question=objetoQuestion,
                #                 #  n_orden=itera_n_orden,
                #                 id=answer_id_4
                                 
                #                  )
                # # answer4 = Answer(text=answer_text4,
                # #                  correct=answer_correct4,
                # #                  question=objetoQuestion
                # #                  )
                
                # # print(answer4)
                # # itera_n_orden+=itera_n_orden
                # answer4.text = formulario['opcion_4']
                # answer4.correct = answer_correct4
                # answer4.save()
                
                # itera_n_orden = 1
                
                # print(formulario['opcion_2'])
                # print(formulario['opcion_2_check'])
                
                # print(formulario['opcion_3'])
                # print(formulario['opcion_3_check'])
                
                # print(formulario['opcion_4'])
                # print(formulario['opcion_4_check'])
                # print('*'*24)
            
            
            delete_questions(quiz,lista_id_contiene)
            questFormset, quizForm = get_forms(datos_Quiz,questForm, quizForm, producto_choices)
            
            # print(questFormset)
            # print(quizForm) 
        
            context = {
                # 'formset': formset, 
                'names':names,
                'quizForm': quizForm,
                'questForm':questFormset,
                'quiz': quiz,
                'grupo':datos_Quiz.fk_grupo.id,
                "Name_quiz":datos_Quiz.name
                # 'sublistas': sublistas
                }

            return render(request, 'cursosLeccionesapp/form_edit_quiz.html', context)        
            # return redirect('success')

        # formset.is_valid()
        # names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
        # pp = list( filter( lambda x: x != {} , [form.as_p for form in formset ])) 
        # initial_data = names
        
        # for i in pp:
        #     print(i)
        # print(names)

        # formset = NameFormSet(initial=initial_data, prefix='forma')
        
        questFormset.is_valid()
        names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
  
        initial_data = names
        print(names)
        

        questFormset = questForm(initial=initial_data, prefix='formb')
        print('post no valido')
        

    else:

        
        # quizForm = QuizForm(datos_Quiz.first())
        
        print(quizForm)
        
        
        setattr(quizForm, datos_Quiz.name, 1)
        setattr(quizForm, datos_Quiz.difficluty, 2)
        setattr(quizForm, str (datos_Quiz.lessson) , 3)
        setattr(quizForm, str(datos_Quiz.fk_grupo) , 4)
        setattr(quizForm, str(datos_Quiz.id) , 5)
        
        initial_data = [{'name':datos_Quiz.name}]
        
        # quizForm = QuizForm(initial_data)
        
        
        # print(quizForm.is_valid())
        
        # print(quizForm['name']) 
        
         
        # quizForm['name'] = datos_Quiz.name
        # quizForm['difficluty'] = datos_Quiz.difficluty
        # quizForm['lessson'] = datos_Quiz.lessson
        # quizForm['fk_grupo'] = datos_Quiz.fk_grupo

           
        # formset = NameFormSet(prefix='forma')
        print(quizForm)
        
        quizForm = QuizForm(instance=datos_Quiz,lessson_choices = producto_choices )
        print(quizForm)
        
        # print(quizForm['id']) 
        
        preguntas = Question.objects.filter(quiz=datos_Quiz)
        # print(preguntas)
        
        lista_preguntas = []
        for n_pregunta in preguntas:
            respuestas = Answer.objects.filter(question=n_pregunta)
            lista_preguntas.append(respuestas)
        
        
        print(lista_preguntas)
        
        dict_preguntas = []
        for l_respuestas in lista_preguntas:
            pregunta = {
            'text':l_respuestas[0].question.text , 
            'text_n':l_respuestas[0].question.id , 
            
            'opcion_1': l_respuestas[0].text,
            'opcion_1_n': l_respuestas[0].id,
            'opcion_1_check':l_respuestas[0].correct,
            'opcion_2':l_respuestas[1].text, 
            'opcion_2_n':l_respuestas[1].id, 
            'opcion_2_check': l_respuestas[1].correct,
            'opcion_3':l_respuestas[2].text,
            'opcion_3_n':l_respuestas[2].id,
            'opcion_3_check': l_respuestas[2].correct,
            'opcion_4':l_respuestas[3].text,
            'opcion_4_n':l_respuestas[3].id,
            'opcion_4_check': l_respuestas[3].correct,

            }
            
            dict_preguntas.append(pregunta)
        
        #print(dict_preguntas)
            
            
        initial_data = dict_preguntas
        
        print(quizForm)
        
        
        
        
        # initial_data=[{
        #     'text':'aaaaaaaa', 
        #     'opcion_1':'hala',
        #     'opcion_1_check':True,
        #     'opcion_2':'o', 
        #   'opcion_2_check': False,
        #   'opcion_3':'h',
        #   'opcion_3_check': False,
        #   'opcion_4':'hh',
        #   'opcion_4_check': False,
        #                },{
        #     'text':'aaaaaaaa2', 
        #     'opcion_1':'hala',
        #     'opcion_1_check':True,
        #     'opcion_2':'o', 
        #   'opcion_2_check': False,
        #   'opcion_3':'h',
        #   'opcion_3_check': False,
        #   'opcion_4':'hh',
        #   'opcion_4_check': False,
        #                }]
        
        questFormset =  questForm(prefix='formb', initial=initial_data)
        
        
        # questFormset['opcion_1'].value = 'hola1'
        # questFormset['text'].value = 'h'
        
        #   
          
          
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # questFormset =  questForm(initial=initial_data,prefix='formb')
        
        print('no')
        
    context = {
        # 'formset': formset,
        'quizForm':quizForm,
        'questForm': questFormset,
        'quiz':quiz,
        'grupo':datos_Quiz.fk_grupo.id,
        "Name_quiz":datos_Quiz.name
        }

    return render(request, 'cursosLeccionesapp/form_edit_quiz.html', context)


# def create_quiz(request):
#     NameFormSet = formset_factory(AnswerForm, extra=0)
#     questForm =  formset_factory(QuestionForm, extra=0)
#     quizForm = QuizForm()
#     print('')
    
#     if request.method == 'POST':
#         formset = NameFormSet(request.POST, prefix='forma')
#         questFormset = questForm(request.POST, prefix='formb')
#         quizForm = QuizForm(request.POST)
        
        
#         sublistas = []
#         numero_quest = 0
#         for i in range(0, len(formset), 4):
#             # Get the sublist
#             sublista = []
#             print(questFormset[numero_quest])
#             sublista.append(questFormset[numero_quest])
#             sublista.extend(formset[i:i+4]) 
#             # sublista = formset[i:i+4]
#             # Append the sublist to the list of sublists
#             sublistas.append(sublista)
#             print(numero_quest)
#             numero_quest += 1
#             # print(sublistas)
            
        
        
#         if quizForm.is_valid() and formset.is_valid() and questFormset.is_valid() :

#             names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
#             initial_data = names
#             print(names)
            
                
#             formset = NameFormSet(initial=initial_data, prefix='forma')
            
#             names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
#             initial_data = names

#             questFormset = questForm(initial=initial_data, prefix='formb')
            
#             print(names)
#             print(quizForm.cleaned_data)
            
#             context = {
#                 'formset': formset, 
#                 'names':names,
#                 'quizForm': quizForm,
#                 'questForm':questFormset,
#                 'sublistas': sublistas
#                 }

#             return render(request, 'cursosLeccionesapp/form_create_quiz.html', context)        
#             # return redirect('success')

#         formset.is_valid()
#         names = list( filter( lambda x: x != {} , [form.cleaned_data for form in formset ])) 
#         pp = list( filter( lambda x: x != {} , [form.as_p for form in formset ])) 
#         initial_data = names
        
#         for i in pp:
#             print(i)
#         print(names)

#         formset = NameFormSet(initial=initial_data, prefix='forma')
        
#         questFormset.is_valid()
#         names = list( filter( lambda x: x != {} , [form.cleaned_data for form in questFormset ])) 
  
#         initial_data = names
#         print(names)

#         questFormset = questForm(initial=initial_data, prefix='formb')
#         print('post no valido')
        

#     else:
#         formset = NameFormSet(prefix='forma')
#         questFormset =  questForm(prefix='formb')
#         print('no')
        
#     context = {
#         'formset': formset,
#         'quizForm':quizForm,
#         'questForm': questFormset
#         }

#     return render(request, 'cursosLeccionesapp/form_create_quiz.html', context)




def create_quiz2(request):
    NameFormSet = formset_factory(AnswerForm)
    questForm =  formset_factory(QuestionForm)
    # questForm =  QuestionForm()
    quizForm = QuizForm()
    
    print('')
    
    if request.method == 'POST':
        formset = NameFormSet(request.POST, prefix='form1')
        questFormset = questForm(request.POST, prefix='form2')
        quizForm = QuizForm(request.POST)
        
        # form = QuizForm(request.POST)
        # if form.is_valid():
        #     data = form.cleaned_data
        #     # person = QuizForm(name=data['name'], email=data['email'], age=data['age'])
        #     # person.save()
        #     print(data)
        #     return render(request, 'cursosLeccionesapp/form_edit_quiz.html', {'form': form})        
        #     # return redirect('success')
        
        
        
        if  quizForm.is_valid() and formset.is_valid() :
        # if questFormset.is_valid() and quizForm.is_valid() and formset.is_valid() :
        # if formset.is_valid():
            # procesar datos del formulario aquí
            names = [form.cleaned_data for form in formset]
            # names2 = [form.cleaned_data for form in quizForm]
            # names3 = [form.cleaned_data for form in questFormset]
            # names2 = quizForm.cleaned_data
            # names3 = questForm.cleaned_data
            print(names)
            # print(names2)
            # print(names3)
            print(quizForm.cleaned_data)
            # print(questForm.cleaned_data)
            context = {
                'formset': formset, 
                'questForm':questFormset,
                'quizForm': quizForm,
                # 'names': names,
                # 'names2': names2,
                # 'names2': names3,
                
        }
            return render(request, 'cursosLeccionesapp/formulario_create_quiz.html', context)
    else:
        # initial_data = [{'name': 'Name 1'}, {'name': 'Name 2'}]
        # initial_data = [{'difficluty': p.difficluty} for p in choose]

        # formset = NameFormSet(initial=initial_data)
        formset = NameFormSet(prefix='form1')
        

    # print(formset)
    questFormset =  questForm(prefix='form2')
    formset = NameFormSet(prefix='form1')
 
    context = {
        'formset': formset, 
        'questForm':questFormset,
        'quizForm': quizForm
        }
    
    return render(request, 'cursosLeccionesapp/formulario_create_quiz.html', context )



# def create_quiz(request):
#     ExtraFormSet = formsets.formset_factory(ExtraForm, formset=BaseExtraFormSet, can_delete=True, extra=3)
#     if request.method == 'POST':
#         extra_formset = ExtraFormSet(request.POST)
#         if extra_formset.is_valid():
#             # Aquí puedes procesar los datos del formset y guardarlos en la base de datos
#             pass
#     else:
#         extra_formset = ExtraFormSet()
#     return render(request, 'cursosLeccionesapp/formulario_create_quiz.html', {'answer_set_formset': extra_formset,
#                                                                               'ExtraForm':ExtraForm })




def create_quiz2(request):
    form = MiFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # procesa el formulario
        nombre = form.cleaned_data[1]['nombre']
        apellido = form.cleaned_data[1]['apellido']
        print(f'Nombre: {nombre}')
        print(f'Apellido: {apellido}')
        
    return render(request, 'cursosLeccionesapp/formulario_create_quiz.html', {'mi_formset': form})



def filter_anio(request,anio):
    filtro = course.objects.filter(anio=anio)

    context = {
            'object_list': filtro
        }

    return render(request,"cursosLeccionesapp/course_list.html", context)


from django.contrib.auth.decorators import login_required
from ciertoFalsoapp.models import test_True_false

def obtener_lecciones_con_score_perfecto(estudiante_id):
    # Filtrar los puntajes del estudiante con score perfecto
    puntajes_estudiante = Score_juegos_lesson.objects.filter(estudiante=estudiante_id, score_perfecto=True)
    print(puntajes_estudiante)
    
    # Crear una lista de nombres de lecciones con score perfecto
    lecciones_con_score_perfecto = [
        puntaje.juego_lesson.lesson for puntaje in puntajes_estudiante
    ]

    return lecciones_con_score_perfecto
#@login_required
class courseListView(ListView):
    model = course

class courseDetailView(DetailView):
    model = course
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user = self.request.user
            if hasattr(user, 'estudiante'):
                context['UserJuegoPerfecto'] = obtener_lecciones_con_score_perfecto(user.estudiante)
        else:
            context['UserJuegoPerfecto'] = []
        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     course = context['object']  # Obtenemos el objeto Course
        
    #     # Filtramos las lecciones basadas en el atributo booleano deseado
    #     filtered_lessons = Lesson.objects.filter(course=course, mostrar=True)
        
    #     context['lessons'] = filtered_lessons
    #     return context

# @csrf_exempt

#requisito login para ver
from gamesUnityapp.models import Juegos_lesson, Score_juegos_lesson
from juegosapp.models import Lesson_cards, ListQuiz

from gamesUnityapp.views import grafico_EXP

def LessonDetailView(request, course_slug, lesson_slug):
    

    try:
        grupo_del_estudiante = GrupoEstudiante.objects.filter(estudiante=request.user.estudiante)
    except Exception as error:
        grupo_del_estudiante = []


    course_qs = course.objects.filter(slug=course_slug)
    

    if request.method == "POST":
        postcoment = request.POST["prd"]
        print("funciona  "+ postcoment)

        course_qs = course.objects.filter(slug=course_slug)
        if course_qs.exists():
            coursea = course_qs.first()
        
        lesson_qs = coursea.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        usuario = request.user
        comentario = Comment(content=postcoment)
        comentario.lessson = lesson
        comentario.user = usuario
        comentario.save()



    if course_qs.exists():
        coursea = course_qs.first()
    
    lesson_qs = coursea.lessons.filter(slug=lesson_slug)
    if lesson_qs.exists():
        lesson = lesson_qs.first()
        l = coursea.lessons.all()

        comentarios = Comment.objects.filter(lessson_id=lesson.id).order_by('-timestamp')

        
        #obtener los quices
        print(grupo_del_estudiante)
        try:
            quices = Quiz.objects.filter(lessson_id=lesson.id, fk_grupo__in=[ x['grupo_id'] for x in grupo_del_estudiante.values()])
            
        except Exception as error:
            quices = []
        

        parrafos = parrafoLeccion.objects.filter(leccion_id=lesson.id)
        
        rutajuego = Juegos_lesson.objects.filter(lesson=lesson.id)
        rutajuego = rutajuego.first()
        
        
        #obtener puntuacion
        try:
            clasificacion = Score_juegos_lesson.objects.filter(juego_lesson__lesson=lesson.id).order_by('-score')[:5]
            
        except Exception as error:
            clasificacion = []
        
        testTF = test_True_false.objects.filter(leccion=lesson).first()
        testCards = Lesson_cards.objects.filter(leccion=lesson).first()
        testTrivia = ListQuiz.objects.filter(leccion=lesson).first()
        
        if hasattr(request.user, 'estudiante'):
            score_perfecto = Score_juegos_lesson.objects.filter(juego_lesson__lesson=lesson.id, estudiante = request.user.estudiante ).first()
        else:
            score_perfecto = False
        
    script, div =  grafico_EXP(clasificacion)

    context = {  
        'object': lesson, 
        'a': l,
        'ruta_c' : course_slug,
        'ruta_l': lesson_slug,
        'coment': comentarios,
        'quices': quices,
        'parrafos': parrafos,
        'name_path_game': rutajuego,
        'tabla_clasificacion': clasificacion,
        'testTF': testTF,
        'testCards': testCards,
        'testTrivia': testTrivia,
        'script': script, 
        'div': div,
        'score_perfecto': score_perfecto
    }

    return render(request, "cursosLeccionesapp/lesson_detail.html",context)

def vistas(request):
    return render(request,"a/v.html")

def v(request):
    listaCursos = []

    clases = Grupo.objects.filter(profesor__user__username="maria")
    for i in clases:
        listaCursos.append(i.course)
    setlistaCursos = set(listaCursos)
    listlistaCursos = list(setlistaCursos)
    context = {  
            'clases': clases,
            'listaCursos': listlistaCursos

        }
    return render(request,"a/v.html",context)

def vistasc(request,curso,les):

    if request.method == "POST":
        postcoment = request.POST["prd"]
        print("funciona  "+ postcoment)

        course_qs = course.objects.filter(slug=curso)
        if course_qs.exists():
            coursea = course_qs.first()
        
        lesson_qs = coursea.lessons.filter(slug=les)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        usuario = request.user
        comentario = Comment(content=postcoment)
        comentario.lessson = lesson
        comentario.user = usuario
        comentario.save()

        return LessonDetailView().get(request,curso,les)
    else:
        return LessonDetailView().get(request,curso,les)




from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Question, Answer
from .models import Result

from usersapp.models import Estudiante

class QuizListView(ListView):
    model = Quiz 
    template_name = 'cursosLeccionesapp/quizmain.html'

def quiz_view(request,course_slug,lesson_slug, pk):
    print("-------------------",pk)
    quiz = Quiz.objects.get(pk=pk)
    print("-------------------",quiz)
    context = {
        'obj': quiz,
        'course_slug': course_slug,
        'lesson_slug': lesson_slug
    }
    return render(request, 'cursosLeccionesapp/quiz.html', context)

def quiz_data_view(request,course_slug,lesson_slug,  pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def save_quiz_view(request,course_slug,lesson_slug, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')
        

        print('aqui'*20)
        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            print(question)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        estudiant = Estudiante.objects.get(user= user)
        #se realizaron cambios al modificar la base de datos
        # saveNota = Result.objects.create(quiz=quiz, user=user, score=score_)
        saveNota = Result.objects.create(quiz=quiz, user=estudiant, score=score_)
        print(saveNota)
        
        # grupoEst =  GrupoEstudiante.objects.get(estudiante=request.user.estudiante)
        getGrupo = Grupo.objects.get(course=quiz.lessson.course)
        
        # grupoNotas = GrupoNotas.objects.create(nota=saveNota, grupo=grupoEst.grupo)
        grupoNotas = GrupoNotas.objects.create(nota=saveNota, grupo=getGrupo)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


from django.http import JsonResponse
from django.core import serializers

def set_comment_lesson(request):
    if request.method == "POST":
        postcoment = request.POST["content"]
        id_lesson = request.POST["id_lesson"]
        print("funciona ajax "+ postcoment)
        
        try:
            lesson = Lesson.objects.get(id=id_lesson)
            usuario = request.user
            comentario = Comment(content=postcoment)
            comentario.lessson = lesson
            comentario.user = usuario
            comentario.save()
            
        except Exception as error:
            lesson = []

        # course_qs = course.objects.filter(slug=course_slug)
        # if course_qs.exists():
        #     coursea = course_qs.first()
        
        # lesson_qs = coursea.lessons.filter(slug=lesson_slug)
        # if lesson_qs.exists():
        #     lesson = lesson_qs.first()
    comments = Comment.objects.filter(lessson_id=id_lesson).order_by('-timestamp')
    comments_data = []
    for comment in comments:
        if hasattr(comment.user, 'estudiante') and comment.user.estudiante.picture:
            picture_url = comment.user.estudiante.picture.url
        elif hasattr(comment.user, 'profesor') and comment.user.profesor.picture:
            picture_url = comment.user.profesor.picture.url
        else:
            picture_url = '/media/default/user.png'
        comments_data.append({
            'content': comment.content,
            'picture_url': picture_url
        })



    return JsonResponse({'comments': comments_data})


    comments_json = serializers.serialize('json', comments)
    return JsonResponse({'comments': comments_json})



