from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('organismo-corporativo/', views.organismo_corporativo_view, name='organismo_corporativo'),
    path('contacto/', views.contacto, name='contacto'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('sostenibilidad/', views.sostenibilidad, name='sostenibilidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)