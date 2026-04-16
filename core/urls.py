from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    #path('noticias/', views.noticias, name='noticias'),
    path('sostenibilidad/', views.noticias, name='sostenibilidad'),
    #path('organismo-corporativo/', views.organismo_corporativo_view, name='organismo_corporativo'),
]
