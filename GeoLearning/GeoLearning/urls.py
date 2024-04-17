"""GeoLearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from usersapp import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homeapp.urls')),
    path('users/', include('usersapp.urls')),

    # path('listcursos/', include('cursosapp.urls')),
    path('vistacurso/', include('cursosLeccionesapp.urls')),
    path('', include('baseapp.urls')),

    # nuevas del gabo
    path('datos/', include('defapp.urls')),
    path('juegos/', include('juegosapp.urls')),
    
    
   
    path('truefalse/', include('ciertoFalsoapp.urls')),
    
    
    path('gamesUnity/', include('gamesUnityapp.urls')),
    
    
]

