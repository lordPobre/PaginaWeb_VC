"""Utilidades de imágenes: optimización a WebP y storage privado para denuncias."""
import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import storages

MAX_LADO = 2400      # px, lado mayor
CALIDAD_WEBP = 82


def optimizar_imagen(field):
    """Si el archivo es nuevo (aún no guardado), lo redimensiona y convierte a WebP.
    Reduce PNG de 2–3 MB a ~200–400 KB sin pérdida visible."""
    if not field or getattr(field, '_committed', True):
        return
    try:
        from PIL import Image, ImageOps
        archivo = field.file
        archivo.seek(0)
        img = Image.open(archivo)
        img = ImageOps.exif_transpose(img)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')
        img.thumbnail((MAX_LADO, MAX_LADO), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format='WEBP', quality=CALIDAD_WEBP, method=6)
        nombre = os.path.splitext(os.path.basename(field.name))[0] + '.webp'
        field.save(nombre, ContentFile(buf.getvalue()), save=False)
    except Exception:
        # Si Pillow no puede procesarla (SVG, archivo raro), se sube tal cual.
        pass


def storage_privado():
    """Callable usado en FileField(storage=...). Django lo serializa por referencia en las migraciones."""
    try:
        return storages['privado']
    except Exception:
        return storages['default']
