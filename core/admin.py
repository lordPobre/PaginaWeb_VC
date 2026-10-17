from django.contrib import admin
from django.utils.html import format_html

from .models import Proyecto, ProyectoImagen, SlideInicio, ImagenSitio, Contacto, Denuncia

admin.site.site_header = 'VC Ingeniería y Construcción · Administración'
admin.site.site_title = 'VC Admin'
admin.site.index_title = 'Contenido del sitio'


def miniatura(obj, campo='imagen', alto=56):
    f = getattr(obj, campo, None) if obj else None
    if not f:
        return '—'
    try:
        url = f.url
    except Exception:
        return '—'
    return format_html('<img src="{}" style="height:{}px;width:auto;object-fit:cover;">', url, alto)


class ProyectoImagenInline(admin.TabularInline):
    model = ProyectoImagen
    extra = 1
    fields = ('vista', 'imagen', 'pie', 'pie_en', 'orden')
    readonly_fields = ('vista',)

    @admin.display(description='Vista')
    def vista(self, obj):
        return miniatura(obj, alto=48)


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('vista', 'titulo', 'categoria', 'ubicacion', 'anio', 'destacado', 'publicado', 'orden')
    list_display_links = ('vista', 'titulo')
    list_editable = ('destacado', 'publicado', 'orden')
    list_filter = ('categoria', 'publicado', 'destacado')
    search_fields = ('titulo', 'resumen', 'ubicacion')
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ('vista_grande',)
    inlines = [ProyectoImagenInline]
    fieldsets = (
        ('Proyecto', {'fields': ('titulo', 'slug', 'categoria', ('etiqueta', 'etiqueta_en'))}),
        ('Imagen principal', {'fields': ('vista_grande', 'imagen', 'imagen_alt')}),
        ('Textos', {'fields': (('resumen', 'resumen_en'), ('descripcion', 'descripcion_en'))}),
        ('Ficha técnica', {'fields': (('ubicacion', 'ubicacion_en'), 'anio', ('especialidad', 'especialidad_en'), ('alcance', 'alcance_en'))}),
        ('Publicación', {'fields': (('publicado', 'destacado', 'orden'),)}),
    )

    @admin.display(description='')
    def vista(self, obj):
        return miniatura(obj)

    @admin.display(description='Vista previa')
    def vista_grande(self, obj):
        return miniatura(obj, alto=180)


@admin.register(SlideInicio)
class SlideInicioAdmin(admin.ModelAdmin):
    list_display = ('vista', 'etiqueta', 'etiqueta_en', 'activo', 'orden')
    list_display_links = ('vista', 'etiqueta')
    list_editable = ('activo', 'orden')

    @admin.display(description='')
    def vista(self, obj):
        return miniatura(obj, alto=64)


@admin.register(ImagenSitio)
class ImagenSitioAdmin(admin.ModelAdmin):
    list_display = ('vista', 'espacio', 'alt', 'actualizado')
    list_display_links = ('vista', 'espacio')

    @admin.display(description='')
    def vista(self, obj):
        return miniatura(obj, alto=64)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha')
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('nombre', 'email', 'mensaje', 'fecha')


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'relacion', 'remitente', 'fecha_creacion', 'tiene_evidencia')
    list_filter = ('categoria', 'relacion')
    readonly_fields = ('nombre', 'contacto', 'categoria', 'relacion', 'descripcion', 'evidencia_link', 'fecha_creacion')
    exclude = ('evidencia',)

    @admin.display(description='Remitente')
    def remitente(self, obj):
        return obj.nombre or 'Anónima'

    @admin.display(boolean=True, description='Evidencia')
    def tiene_evidencia(self, obj):
        return bool(obj.evidencia)

    @admin.display(description='Evidencia')
    def evidencia_link(self, obj):
        if not obj.evidencia:
            return '—'
        # URL firmada del bucket privado, expira en 10 minutos.
        return format_html('<a href="{}" target="_blank" rel="noopener">Descargar evidencia (enlace temporal)</a>', obj.evidencia.url)
