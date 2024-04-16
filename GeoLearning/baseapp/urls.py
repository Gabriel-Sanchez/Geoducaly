from django.urls import path

from baseapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('foros',views.foros, name="foros"),
]


urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)