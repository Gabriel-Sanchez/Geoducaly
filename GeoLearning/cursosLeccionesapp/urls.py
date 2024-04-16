
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

from .views import courseListView, courseDetailView

app_name = "courses"


from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view
)


urlpatterns = [
    path('a',views.v, name="v"),
    path('vistasc/<curso>/<les>',views.vistasc, name="vistasc"),
    path('filter_anio/<anio>',views.filter_anio, name="f_anio"),
    
    path('create/<grupo>',views.create_quiz, name="create_quiz"),
    path('edit/<quiz>',views.edit_quiz, name="edit_quiz"),
    path('list_quices/<grupo>',views.list_quices, name="list_quices"),
    path('delete_quiz/<grupo>',views.delete_quiz, name="delete_quiz"),


    path('',courseListView.as_view(), name="list"),
    path('<slug>',courseDetailView.as_view(), name="detail"),
    path('<course_slug>/<lesson_slug>/',views.LessonDetailView, name="lesson-detail"),

    path('vistas',views.vistas, name="vistas"),

    path('mainv/mainv/', QuizListView.as_view(), name='main-view'),
    path('<course_slug>/<lesson_slug>/<pk>/', quiz_view, name='quiz-view'),
    # path('mainv/mainv/<pk>/', quiz_view, name='quiz-view'),
    path('<course_slug>/<lesson_slug>/<pk>/save/', save_quiz_view, name='save-view'),
    # path('mainv/mainv/<pk>/save/', save_quiz_view, name='save-view'),
    path('<course_slug>/<lesson_slug>/<pk>/data/', quiz_data_view, name='quiz-data-view'),
    # path('mainv/mainv/<pk>/data/', quiz_data_view, name='quiz-data-view'),
    
    path('crea_grupo/',views.crea_grupo, name="crea_grupo"),
    path('edita_grupo/<grupo_id>',views.edit_grupo, name="edita_grupo"),
    path('delete_grupo/',views.delete_grupo, name="delete_grupo"),
    path('detalles_grupo/<grupo_id>',views.detalles_grupo, name="detalles_grupo"),
    path('unirse_grupo/<grupo_id>',views.unirse_grupo, name="unirse_grupo"),
    path('lista_grupo/',views.lista_grupo, name="lista_grupo"),
    path('set_comment_lesson/',views.set_comment_lesson, name="set_comment_lesson"),
    
    path('salirse_grupo_estudiante/',views.salirse_grupo_estudiante, name="salirse_grupo_estudiante"),
    
    path('grupo/mis_grupos',views.mis_grupos, name="mis_grupos"),
    
    path('grupo/eliminar_juego_carta/<id_juego>',views.eliminar_juego_carta, name="eliminar_juego_carta"),
    path('grupo/eliminar_juego_cf/<id_juego>',views.eliminar_juego_cf, name="eliminar_juego_cf"),

]


