"""Sube a Cloudflare R2 las imágenes y proyectos que hoy están fijos en el código.

Uso:  python manage.py cargar_contenido_inicial
Es seguro ejecutarlo varias veces: no duplica lo que ya existe.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Proyecto, SlideInicio, ImagenSitio

IMG = Path(settings.BASE_DIR) / 'core' / 'static' / 'core' / 'img'

PROYECTOS = [
    dict(titulo='Central Quintero Energía', slug='central-quintero-energia', categoria='energia',
         resumen='Mejoramiento de mobiliario en sala de control U-3. Ejecución bajo estrictos protocolos de continuidad operacional y seguridad eléctrica.',
         resumen_en='Furniture upgrade in the U-3 control room, carried out under strict operational-continuity and electrical-safety protocols.',
         ubicacion='Quintero, V Región', ubicacion_en='Quintero, Valparaíso Region', anio=2023,
         especialidad='Obras civiles', especialidad_en='Civil works', alcance='Sala de control U-3', alcance_en='U-3 control room',
         archivo='quintero-energia.jpg', orden=1),
    dict(titulo='Alfalfal II', slug='alfalfal-ii', categoria='montaje',
         resumen='Fabricación y montaje especializado de línea de succión para bomba dragadora en proyecto Foreway. Alta precisión en soldadura y ajuste mecánico.',
         resumen_en='Fabrication and installation of a dredge-pump suction line for the Foreway project, with high-precision welding and mechanical fitting.',
         ubicacion='Cajón del Maipo, RM', ubicacion_en='Cajón del Maipo, Santiago Metropolitan Region',
         especialidad='Montaje mecánico', especialidad_en='Mechanical installation', alcance='Línea de succión de bomba dragadora', alcance_en='Dredge-pump suction line',
         archivo='alfalfal2.png', orden=2),
    dict(titulo='Central Las Lajas', slug='central-las-lajas', categoria='hidraulica',
         etiqueta='Mantención e hidráulica', etiqueta_en='Maintenance & hydraulics',
         resumen='Reparación de filtros de retrolavado y fabricación de líneas de acero inoxidable para circuitos abiertos y cerrados de las unidades 1 y 2.',
         resumen_en='Repair of backwash filters and fabrication of stainless-steel lines for the open and closed circuits of units 1 and 2.',
         ubicacion='Central Las Lajas / Alfalfal II',
         especialidad='Fabricación en acero inoxidable', especialidad_en='Stainless-steel fabrication', alcance='Filtros de retrolavado', alcance_en='Backwash filters',
         archivo='Laja.jpg', orden=3),
]

SLIDES = [
    ('banner_vc.png', 'Obras civiles', 'Civil works', 'Supervisor frente a obra en construcción'),
    ('planta.png', 'Montaje industrial', 'Industrial installation', 'Planta industrial con correas transportadoras'),
    ('puente.png', 'Infraestructura', 'Infrastructure', 'Puente de hormigón sobre río'),
]

ESPACIOS = {
    'area_montaje': 'servicio1.png', 'area_obras': 'servicio2.png', 'area_mantencion': 'servicio3.png',
    'inicio_esg': 'sostenibilidad.png', 'inicio_contacto': 'contacto.png',
    'hero_nosotros': 'nosotros.jpg', 'nosotros_bloque': 'servicio2.png', 'hero_proyectos': 'banner_pro.jpg',
    'hero_sostenibilidad': 'sostenibilidad.png', 'hero_contacto': 'contacto.png',
    'hero_denuncias': 'banner.png', 'hero_blog': 'planta.png',
}


class Command(BaseCommand):
    help = 'Carga proyectos, fotos del hero e imágenes del sitio en el storage configurado (Cloudflare R2).'

    def _archivo(self, nombre):
        ruta = IMG / nombre
        if not ruta.exists():
            self.stdout.write(self.style.WARNING(f'  No existe {ruta}, se omite.'))
            return None
        return File(open(ruta, 'rb'), name=nombre)

    def handle(self, *args, **opts):
        destino = 'Cloudflare R2' if getattr(settings, 'USAR_R2', False) else 'disco local (/media) — faltan variables R2_*'
        self.stdout.write(f'Destino de archivos: {destino}')

        for i, datos in enumerate(PROYECTOS):
            datos = dict(datos)
            archivo = datos.pop('archivo')
            if Proyecto.objects.filter(slug=datos['slug']).exists():
                self.stdout.write(f'· Proyecto "{datos["titulo"]}" ya existe')
                continue
            f = self._archivo(archivo)
            if not f:
                continue
            p = Proyecto(**datos)
            p.imagen = f  # sin guardar aún: así se optimiza a WebP al hacer save()
            p.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Proyecto "{p.titulo}"'))

        if not SlideInicio.objects.exists():
            for orden, (archivo, et, et_en, alt) in enumerate(SLIDES):
                f = self._archivo(archivo)
                if not f:
                    continue
                s = SlideInicio(etiqueta=et, etiqueta_en=et_en, alt=alt, orden=orden)
                s.imagen = f
                s.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Foto del hero "{et}"'))
        else:
            self.stdout.write('· Fotos del hero ya cargadas')

        for espacio, archivo in ESPACIOS.items():
            if ImagenSitio.objects.filter(espacio=espacio).exists():
                continue
            f = self._archivo(archivo)
            if not f:
                continue
            obj = ImagenSitio(espacio=espacio)
            obj.imagen = f
            obj.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Imagen del sitio "{obj.get_espacio_display()}"'))

        self.stdout.write(self.style.SUCCESS('Listo. Administra todo desde /admin/'))
