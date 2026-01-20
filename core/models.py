from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='noticias/')

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clientes/')

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class PersonaOrganismo(models.Model):
    SECCION_CHOICES = [
        ('administracion', 'Administración'),
        ('directorio', 'Directorio'),
    ]
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='organismo_corporativo/')
    seccion = models.CharField(max_length=20, choices=SECCION_CHOICES)

    def __str__(self):
        return f"{self.nombre} - {self.seccion}"

class Sostenibilidad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.ImageField(upload_to='sostenibilidad/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"

class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='proyectos/')

    def __str__(self):
        return self.titulo