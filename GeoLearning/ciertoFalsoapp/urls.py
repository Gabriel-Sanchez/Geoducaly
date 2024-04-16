from django.urls import path
from .views import jugar, terminar, guardar_score_Post

# app_name = "juegos_cf"

urlpatterns = [
    path('jugar/<leccion_id>', jugar, name='jugar_cf'),
    path('jugar/terminar/', terminar, name='terminar'),
    path('guardar_score_Post/', guardar_score_Post, name='guardar_score_Post'),
]
