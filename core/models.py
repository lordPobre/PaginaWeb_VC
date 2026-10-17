from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .imagenes import optimizar_imagen, storage_privado


# ---------------------------------------------------------------------------
# Contenido administrable (imágenes y proyectos). Los archivos se guardan en
# Cloudflare R2 a través de STORAGES["default"] (ver settings.py).
# ---------------------------------------------------------------------------

class Proyecto(models.Model):
    CATEGORIAS = [
        ('energia', 'Energía'),
        ('montaje', 'Montaje industrial'),
        ('hidraulica', 'Hidráulica'),
        ('obras', 'Obras civiles'),
        ('mineria', 'Minería'),
        ('mantencion', 'Mantención'),
    ]
    CATEGORIAS_EN = {
        'energia': 'Energy', 'montaje': 'Industrial installation', 'hidraulica': 'Hydraulics',
        'obras': 'Civil works', 'mineria': 'Mining', 'mantencion': 'Maintenance',
    }

    titulo = models.CharField('Título', max_length=150)
    slug = models.SlugField(unique=True, max_length=160, help_text='Se usa en la URL: /proyectos/<slug>/')
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIAS)
    etiqueta = models.CharField('Etiqueta visible', max_length=60, blank=True, help_text='Ej: "Mantención e hidráulica". Si se deja vacío se usa la categoría.')
    etiqueta_en = models.CharField('Etiqueta (EN)', max_length=60, blank=True)

    resumen = models.TextField('Resumen', help_text='Texto corto para Inicio y el listado.')
    resumen_en = models.TextField('Resumen (EN)', blank=True)
    descripcion = models.TextField('Descripción completa', blank=True)
    descripcion_en = models.TextField('Descripción completa (EN)', blank=True)

    ubicacion = models.CharField('Ubicación', max_length=120, blank=True)
    ubicacion_en = models.CharField('Ubicación (EN)', max_length=120, blank=True)
    anio = models.PositiveIntegerField('Año', blank=True, null=True)
    especialidad = models.CharField('Especialidad', max_length=120, blank=True)
    especialidad_en = models.CharField('Especialidad (EN)', max_length=120, blank=True)
    alcance = models.CharField('Alcance', max_length=160, blank=True)
    alcance_en = models.CharField('Alcance (EN)', max_length=160, blank=True)

    imagen = models.ImageField('Imagen principal', upload_to='proyectos/')
    imagen_alt = models.CharField('Texto alternativo', max_length=160, blank=True)

    destacado = models.BooleanField('Mostrar en Inicio', default=True)
    publicado = models.BooleanField('Publicado', default=True)
    orden = models.PositiveIntegerField('Orden', default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', '-anio', 'titulo']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)[:160]
        optimizar_imagen(self.imagen)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('proyecto_detalle', args=[self.slug])

    @property
    def etiqueta_es(self):
        return self.etiqueta or self.get_categoria_display()

    @property
    def etiqueta_en_final(self):
        return self.etiqueta_en or self.CATEGORIAS_EN.get(self.categoria, self.etiqueta_es)


class ProyectoImagen(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='proyectos/galeria/')
    pie = models.CharField('Pie de foto', max_length=160, blank=True)
    pie_en = models.CharField('Pie de foto (EN)', max_length=160, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Imagen de galería'
        verbose_name_plural = 'Galería'

    def save(self, *args, **kwargs):
        optimizar_imagen(self.imagen)
        super().save(*args, **kwargs)


class SlideInicio(models.Model):
    """Fotos rotativas del hero de Inicio."""
    imagen = models.ImageField(upload_to='inicio/')
    etiqueta = models.CharField('Etiqueta', max_length=60, help_text='Texto bajo la barra de progreso. Ej: "Obras civiles"')
    etiqueta_en = models.CharField('Etiqueta (EN)', max_length=60, blank=True)
    alt = models.CharField('Texto alternativo', max_length=160, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Foto del hero (Inicio)'
        verbose_name_plural = 'Fotos del hero (Inicio)'

    def __str__(self):
        return self.etiqueta

    def save(self, *args, **kwargs):
        optimizar_imagen(self.imagen)
        super().save(*args, **kwargs)


class ImagenSitio(models.Model):
    """Imágenes fijas del sitio (portadas de cada página, paneles, fondos).
    Si un espacio no tiene imagen cargada, la plantilla usa la imagen estática actual."""
    ESPACIOS = [
        ('area_montaje', 'Inicio · Panel Montaje Industrial'),
        ('area_obras', 'Inicio · Panel Obras Civiles'),
        ('area_mantencion', 'Inicio · Panel Mantención Programada'),
        ('inicio_esg', 'Inicio · Fondo Sostenibilidad'),
        ('inicio_contacto', 'Inicio · Foto Contacto'),
        ('hero_nosotros', 'Nosotros · Portada'),
        ('nosotros_bloque', 'Nosotros · Imagen "Sobre nosotros"'),
        ('hero_proyectos', 'Proyectos · Portada'),
        ('hero_sostenibilidad', 'Sostenibilidad · Portada'),
        ('hero_contacto', 'Contacto · Portada'),
        ('hero_denuncias', 'Canal de denuncias · Portada'),
        ('hero_blog', 'Blog · Portada'),
    ]
    espacio = models.CharField(max_length=40, choices=ESPACIOS, unique=True)
    imagen = models.ImageField(upload_to='sitio/')
    alt = models.CharField('Texto alternativo', max_length=160, blank=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['espacio']
        verbose_name = 'Imagen del sitio'
        verbose_name_plural = 'Imágenes del sitio'

    def __str__(self):
        return self.get_espacio_display()

    def save(self, *args, **kwargs):
        optimizar_imagen(self.imagen)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Formularios
# ---------------------------------------------------------------------------

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = 'Mensajes de contacto'

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class Denuncia(models.Model):
    CATEGORIAS = [
        ('etica', 'Faltas a la Ética o Fraude'),
        ('acoso', 'Acoso Laboral / Sexual'),
        ('seguridad', 'Infracción HSEQ (Seguridad y Medio Ambiente)'),
        ('otro', 'Otras irregularidades'),
    ]
    RELACIONES = [
        ('trabajador', 'Trabajador Directo'),
        ('subcontratista', 'Subcontratista / Proveedor'),
        ('comunidad', 'Comunidad / Tercero Externo'),
        ('cliente', 'Cliente / Mandante'),
    ]

    nombre = models.CharField(max_length=200, blank=True, null=True, help_text="Dejar en blanco si es anónima")
    contacto = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    relacion = models.CharField(max_length=50, choices=RELACIONES, blank=True, null=True)
    descripcion = models.TextField()
    # La evidencia va a un bucket PRIVADO (nunca público): solo se accede con URL firmada desde el admin.
    evidencia = models.FileField(upload_to='denuncias/', blank=True, null=True, storage=storage_privado)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        remitente = "Anónima" if not self.nombre else self.nombre
        return f"Denuncia: {self.get_categoria_display()} - {remitente}"
