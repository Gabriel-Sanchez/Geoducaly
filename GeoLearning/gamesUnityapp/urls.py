
from django.urls import path

from . import views

from django.conf.urls.static import static

urlpatterns = [
    path('score_table/',views.score_table, name="score_table"),
    path('api/get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('api/post-data-token/', views.post_data, name='post-data-token'),
    path('audio/', views.serve_audio_file, name='audio_fondo'),
    
    path('grupo/<id_grupo>', views.view_grupo_general, name='view_grupo_general'),
]

