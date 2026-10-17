
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Proyecto, Contacto, Denuncia, SlideInicio
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html', {
        'slides': SlideInicio.objects.filter(activo=True)[:5],
        'destacados': Proyecto.objects.filter(publicado=True, destacado=True)[:6],
    })

# Equipo directivo mostrado en Nosotros (#equipo). Reemplaza la antigua página
# "Organismo corporativo", que tenía nombres y fotos de ejemplo.
EQUIPO = [
    {'nombre': 'Sebastián Vega', 'iniciales': 'SV', 'cargo': 'Gerente General', 'cargo_key': 'roleGG', 'email': 'svega@vcchile.cl'},
    {'nombre': 'Mauricio Campos', 'iniciales': 'MC', 'cargo': 'Gerente Técnico', 'cargo_key': 'roleGT', 'email': 'mcampos@vcchile.cl'},
]

def nosotros(request):
    return render(request, 'core/nosotros.html', {'equipo': EQUIPO})

def organismo_corporativo_view(request):
    # Se mantiene la URL antigua para no romper enlaces externos.
    return redirect('/nosotros/#equipo', permanent=True)


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        # Campos nuevos del formulario de inicio. Se anexan al mensaje para no
        # requerir una migración del modelo Contacto.
        empresa = request.POST.get('empresa', '').strip()
        servicio = request.POST.get('servicio', '').strip()
        extras = []
        if empresa:
            extras.append(f'Empresa: {empresa}')
        if servicio:
            extras.append(f'Servicio: {servicio}')
        if extras:
            mensaje = ' | '.join(extras) + '\n\n' + mensaje

        Contacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
        messages.success(request, 'Tu mensaje ha sido enviado correctamente. Te contactaremos a la brevedad.')

        destino = request.POST.get('next', '')
        if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
            return redirect(destino)
        return redirect('contacto')
    return render(request, 'core/contacto.html')

def proyectos(request):
    lista = Proyecto.objects.filter(publicado=True)
    presentes = set(lista.values_list('categoria', flat=True))
    categorias = [
        {'valor': k, 'es': es, 'en': Proyecto.CATEGORIAS_EN.get(k, es)}
        for k, es in Proyecto.CATEGORIAS if k in presentes
    ]
    return render(request, 'core/proyectos.html', {'proyectos': lista, 'categorias': categorias})

def proyecto_detalle(request, slug):
    proyecto = get_object_or_404(Proyecto, slug=slug, publicado=True)
    otros = Proyecto.objects.filter(publicado=True).exclude(pk=proyecto.pk)[:3]
    return render(request, 'core/proyecto_detalle.html', {'p': proyecto, 'otros': otros})

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
