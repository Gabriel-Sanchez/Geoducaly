
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

# antes de modificar
urlpatterns = [
    path('',views.alljuegos, name="alljuegos"),
    path('<eljuego>',views.juegos, name="juegos"),
    path('juegos2',views.juegos2, name="juegos2"),
    path('listaTrivias',views.listaTrivias, name="listaTrivias"),
    path('Juegotrivia/<n_jugada>/<Lquiz>',views.Juegotrivia, name="Juegotrivia"),
    path('tablero/',views.tablero, name="tablero"),
    path('resultado/<n_jugada>/<int:pregunta_respondida_pk>/',views.resultado_pregunta, name="resultado"),
    
           path('homeCards/', views.home, name='homecards'),
    path('get_countries/', views.get_countries, name='get_countries'),
    
      path('get_cards/', views.game_view, name='get_cards'),
      path('card_difuculty/', views.card_difuculty, name='card_difuculty'),
      path('get_card_pair/', views.get_card_pair, name='get_card_pair'),
      
      path('cardsPareo/', views.cardsPareo, name='cardsPareo'),
      path('jugarTrivialeccion/<leccion_id>', views.jugar_trivia, name='jugar_trivia'),
      path('jugarTrivialeccion/terminar/', views.terminar_trivia, name='terminarTrivialeccion'),
      path('llenarJuegosRapido/', views.llenarJuegosRapido, name='llenarJuegosRapido'),
      
      
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


