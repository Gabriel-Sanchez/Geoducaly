
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static
from .views import calendar_view

urlpatterns = [
    path('',views.calendario, name="calendar"),
    path('calendar/', calendar_view, name='calendario'),
]

