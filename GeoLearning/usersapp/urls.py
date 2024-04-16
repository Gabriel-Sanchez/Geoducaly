
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from django.contrib.auth.views import  PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


from .views import (
    prof
)

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('me/profile/', views.update_profile, name="update_profile"),
    path('me/details_profile/', views.details_profile, name="details_profile"),
    path('me/prof_charts/', prof.as_view(), name="prof_charts"),
    
    path('me/editar_juego_CF/<id_juego>', views.editar_cf, name="prof_edit_CF"),
    path('me/crear_cf/<id_grupo>', views.crear_cf, name="prof_crear_cf"),
    
    path('me/editar_juego_carta/<id_juego>', views.editar_carta, name="editar_carta"),
    path('me/crear_juego_carta/<id_grupo>', views.crear_carta, name="crear_carta"),
    

   path('reset/password_reset/', PasswordResetView.as_view(
        template_name='users/registration/password_reset_form.html',
        email_template_name='users/registration/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='users/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users/registration/password_reset_complete.html'), name='password_reset_complete'),

   ]