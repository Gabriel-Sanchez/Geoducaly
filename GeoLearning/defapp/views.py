from django.shortcuts import render
from .models import datos
from django.core.paginator import Paginator
from cursosLeccionesapp.models import Lesson
import re


import random
import colorsys
# Create your views here.


def datosview(request,search):
    
    mensaje = ""
    tipoMensaje = ''
    selected_lesson = None
    print(search)
    
    if search == "1":
        semilla = request.session.get('semilla', random.randint(1, 100))

        # Almacena la semilla en la sesión
        request.session['semilla'] = semilla

        # Usa la semilla para obtener un orden aleatorio constante
        random.seed(semilla)
        print(semilla)
        alldata=datos.objects.all().order_by('?')

    else:
        resultado = re.split(r'(\d+)$', search)
        if len(resultado) >= 2:
            parte_anterior = resultado[0]
            numero = resultado[1]
        else:
            parte_anterior = search
            numero = None
        
        leccion_id = request.GET.get('leccion', '')
        if leccion_id:
            try:
                lesson = Lesson.objects.get(id=leccion_id)
                alldata = datos.objects.filter(leccion=lesson)
                search = 'filtro'+leccion_id
                selected_lesson = int(leccion_id) 
                
                mensaje = f"Resultados para la lección '{lesson.title}'"
                tipoMensaje = 'alert-info'
            except Lesson.DoesNotExist:
                mensaje = "Ups.. La lección seleccionada no existe."
                tipoMensaje = 'alert-danger'
        elif parte_anterior == 'filtro':
            alldata = datos.objects.filter(leccion_id = numero)
            selected_lesson = int(numero) 
            mensaje = f"Resultados para la lección '{alldata.first().leccion.title}'"
            tipoMensaje = 'alert-info'
            #search = palabrab

        else:
            palabrab = request.GET.get("prd")
            print('se busca en bbb-')
            
            
            if palabrab == None:
                palabrab = search
            # else:
            
            
            alldata=datos.objects.filter(title__icontains=palabrab)
            search = palabrab
            
                
            if len(alldata) == 0:
                mensaje = "Ups.. no encontramos nungun dato relacionado con '"+palabrab+"'"
                tipoMensaje = 'alert-danger'
            else:
                mensaje = "Resultados para la busqueda '" + palabrab + "'" 
                tipoMensaje = 'alert-info'

        # context= {
        #     'alldata': alldata,
        #     'mensaje': mensaje
        # }

        # return render(request,"definiciones/datos.html", context )
    # elif request.method == "GET":
    #     alldata = request.GET
    
    
    
    # else:
    

    
    # print(alldata)
        
        
    paginator = Paginator(alldata, 5) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # return render(request, 'list.html', {'page_obj': page_obj})
    
    
    print(search)
    


    lessons = Lesson.objects.filter(mostrar=True)
    
        # Generar un color aleatorio para cada lección
    lesson_colors = {}
    for lesson in lessons:
        hue = random.random()
        saturation = random.uniform(0.5, 1.0)
        lightness = random.uniform(0.4, 0.8)
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb)
        lesson_colors[lesson.id] = color

    context= {
        'alldatos': page_obj,
        'search': search,
        'mensaje': mensaje,
        'tipoMensaje': tipoMensaje,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        # 'dddd': page_obj,
        # 'NumPag': int(NumPag),
        # 'disabled': disabled,
        # 'arrayNumBoton': arrayNumBoton,
        

    }

    return render(request,"definiciones/datos.html", context)

