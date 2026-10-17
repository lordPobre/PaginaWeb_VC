from django import template
from django.templatetags.static import static

register = template.Library()


def _imagenes(context):
    """Carga todas las ImagenSitio una sola vez por request."""
    request = context.get('request')
    cache = getattr(request, '_vc_imgs', None) if request else None
    if cache is None:
        from core.models import ImagenSitio
        try:
            cache = {i.espacio: i for i in ImagenSitio.objects.all()}
        except Exception:
            cache = {}
        if request is not None:
            request._vc_imgs = cache
    return cache


@register.simple_tag(takes_context=True)
def img_sitio(context, espacio, respaldo):
    """URL de la imagen cargada en el admin para `espacio`; si no hay, usa la estática `respaldo`.
    Uso: <img src="{% img_sitio 'hero_nosotros' 'core/img/nosotros.jpg' %}">"""
    obj = _imagenes(context).get(espacio)
    if obj and obj.imagen:
        return obj.imagen.url
    return static(respaldo)


@register.simple_tag(takes_context=True)
def img_alt(context, espacio, respaldo=''):
    obj = _imagenes(context).get(espacio)
    return (obj.alt if obj and obj.alt else respaldo)
