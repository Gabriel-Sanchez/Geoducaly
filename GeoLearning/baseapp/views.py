from django.shortcuts import render, HttpResponse
from usersapp.models import Estudiante, Profesor
from django.contrib.auth.models import User



# Create your views here.



def foros(request):

    p = request.user
    user = User.objects.get(username=p.username)

    try:
        p2 = p
        estudiante =Estudiante.objects.get(user = p2) 
    except Exception as error:
        estudiante = request.user.profesor
    
    context={
    'Uprofile': estudiante
    }

    return render(request,"baseapp/foros.html", context)

