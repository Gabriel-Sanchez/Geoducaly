from django.shortcuts import render
from defapp.models import datos
from random import sample

from django.contrib.auth.decorators import login_required

from usersapp.models import Estudiante

from juegosapp.models import ListQuiz, Pregunta, ijuegos, QuizUsuario, PreguntasRespondidas, UserNumQuiz

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import layout

from cursosLeccionesapp.models import course

from gamesUnityapp.views import tabla_puntuacion_list

#@login_required
def home(request):
    winlist=datos.objects.all().order_by('?')[:2]
    # datosi=datos.objects.all()
    # win = []
    # winlist = []

    # for i in range(1, len(datosi)+1):
    #     win.append(i)
    
    # wins = sample(win,2)

    # for n in wins:
    #     d = datos.objects.filter(id=n)
    #     d2 = d.first()
    #     winlist.append(d2)
    
    #cads
    

    
    iju = ijuegos.objects.all()

    #trivias
    # listaTrivias = ListQuiz.objects.all()

    # usernumquiz = UserNumQuiz.objects.filter(usuario=request.user)

    # listNumero = []
    

    # for trivia in listaTrivias:
    #     for usertrivia in usernumquiz:
    #         if trivia == usertrivia.listquiz:
    #             print(trivia,"  ",usertrivia)
    #             l = [trivia, usertrivia.Num_veces_jugadas]
    #             break
    #             # listNumero.append(l)
    #         else:
    #             l = [trivia, 0]
    #             # listNumero.append(l)
    #     if  usernumquiz.exists():
    #         listNumero.append(l)

    #     if not usernumquiz.exists():
    #         l = [trivia, 0]
    #         listNumero.append(l)
    
    
    
    # listNumeronoRepet = []

    # noRepet = set(listNumero)
    # listNumeronoRepet = list(noRepet)
    

    # print(listNumero)

    cardsCollors = ['text-white bg-primary', 'text-white bg-secondary','text-white bg-success', 'text-white bg-danger', 'bg-warning', 'text-body bg-info', 'bg-light','text-white bg-dark']

    object_cursos = course.objects.all()[:3] 
    
    clasificacion = tabla_puntuacion_list()[:3] 
    
    context = {
        "datos":winlist,
        "cardsCollors":cardsCollors,
        'juegos': iju,
        'object_list': object_cursos,
        'clasificacion': clasificacion
        # 'listaTrivias': listaTrivias,
        # 'listNumero': listNumero

    }

    return render(request,"home/home.html" , context)


from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import pandas as pd
import random


def aboutUs(request):
    plot = figure(sizing_mode='stretch_width', height=400,  toolbar_location=None)
    plot.line([1, 2, 3, 4, 5], [2, 5, 3, 7, 1], line_width=2)

    
    # genera el HTML y el JavaScript necesarios para mostrar la figura
    script, div = components(plot)
    
    
    # context = {'script': script, 'div': div}
    
    
    




    df = pd.DataFrame(dict(
        fruits = ['Apple', 'Orange', 'Pineapple', 'Pear', 'Kiwi', 'aa'],
        sales = random.sample(range(1, 11), 6),
    ))
    
    source = ColumnDataSource(data=df)
    p = figure(width=400, height=400, x_range=source.data['fruits'],  toolbar_location=None , tools="")

    p.vbar(x='fruits', top='sales', source=source, width=0.5, bottom=0, color='lightgreen')




 
    


    
    script, div = components(p)
    
    
    context = {'script': script, 'div': div}

    
    # print(div)
    # print(script)
#     x = [1, 2, 3, 4, 5]
#     y = [6, 7, 2, 3, 6]
    
#     plot = figure(title="Gráfico de dispersión")
#     plot.scatter(x, y)
    
  
# # Agrega tus datos y configuraciones al gráfico aquí
#     script, div = components(plot)
    
#     context = {'script': script, 'div': div}

    # Crea dos figuras de Bokeh
    plot1 = figure(sizing_mode='stretch_width', height=400)
    plot1.line([1, 2, 3, 4, 5], [2, 5, 3, 7, 1], line_width=2)

    plot2 = figure(sizing_mode='stretch_width', height=400)
    plot2.line([1, 2, 3, 4, 5], [1, 3, 2, 6, 4], line_width=2)

    # Combina las dos figuras en un diseño
    layout1 = layout([[plot1], [plot2]])

    # Genera los componentes de la gráfica para incrustarla en la plantilla
    script, div = components(layout1)
    
    return render(request,"AcercaDe/Acercade.html", context)





def alljuegos(request):
    iju = ijuegos.objects.all()

    #trivias
    listaTrivias = ListQuiz.objects.all()
    
    #revisar este funcionamiento
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

