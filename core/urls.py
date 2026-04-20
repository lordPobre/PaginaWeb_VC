from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    #path('noticias/', views.noticias, name='noticias'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('sostenibilidad/', views.sostenibilidad, name='sostenibilidad'),
    path('organismo-corporativo/', views.organismo_corporativo_view, name='organismo_corporativo'),
    path('denuncias/', views.denuncias, name='denuncias'),
]
