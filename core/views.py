
from django.shortcuts import render, redirect
from .models import Proyecto, Contacto, Denuncia
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html')

def nosotros(request):
    return render(request, 'core/nosotros.html')

def organismo_corporativo_view(request):
    administracion = [
        {'nombre': 'Sebastian Vegas', 'cargo': 'Gerente General', 'foto': 'core/img/sebastian.png'},
        {'nombre': 'Mauricio Campos', 'cargo': 'Gerente Técnico', 'foto': 'core/img/luis.jpg'},
        {'nombre': 'Carlos Lopez', 'cargo': 'Jefe Supremo TI', 'foto': 'core/img/TI.png'},
    ]

    directorio = [
        {'nombre': 'Juan Soto', 'cargo': 'Presidente', 'foto': 'core/img/juan.jpg'},
        {'nombre': 'Marta Leiva', 'cargo': 'Directora', 'foto': 'core/img/marta.jpg'},
    ]

    return render(request, 'core/organismo_corporativo.html', {
        'administracion': administracion,
        'directorio': directorio
    })


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        Contacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
        messages.success(request, 'Tu mensaje ha sido enviado correctamente.')
        return redirect('contacto')
    return render(request, 'core/contacto.html')

def proyectos(request):
    try:
        proyectos = Proyecto.objects.all()
    except:
        proyectos = [] 
    return render(request, 'core/proyectos.html', {'proyectos': proyectos})

def sostenibilidad(request):
    return render(request, 'core/sostenibilidad.html')

def denuncias(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        contacto = request.POST.get('contacto', '')
        categoria = request.POST.get('categoria')
        relacion = request.POST.get('relacion')
        descripcion = request.POST.get('descripcion')
        evidencia = request.FILES.get('evidencia') 

        Denuncia.objects.create(
            nombre=nombre,
            contacto=contacto,
            categoria=categoria,
            relacion=relacion,
            descripcion=descripcion,
            evidencia=evidencia
        )
        
        return render(request, 'core/denuncias.html', {'exito': True})
    return render(request, 'core/denuncias.html')

def blog(request):
    return render(request, 'core/blog.html')

def articulo(request):
    return render(request, 'core/articulo.html')

def articulo_seguridad(request):
    return render(request, 'core/articulo_seguridad.html')

def articulo_soldadura(request):
    return render(request, 'core/articulo_soldadura.html')