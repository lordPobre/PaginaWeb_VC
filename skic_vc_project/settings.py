import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-inseguro-cambiar')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skic_vc_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skic_vc_project.wsgi.application'

# ---------------------------------------------------------------------------
# Base de datos
# Vercel no conserva archivos entre despliegues: SQLite se pierde. En producción
# usar Postgres (Neon, Supabase o Vercel Postgres) mediante DATABASE_URL.
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get('DATABASE_URL', '')
EN_VERCEL = bool(os.environ.get('VERCEL'))
_es_local = any(h in DATABASE_URL for h in ('@localhost', '@127.0.0.1', '@db:'))

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        # En Vercel cada request puede ser una función nueva: no reutilizar conexiones
        # y usar el endpoint "pooled" del proveedor (Neon: host con "-pooler").
        conn_max_age=0 if EN_VERCEL else 60,
        conn_health_checks=True,
        ssl_require=not _es_local,
    ) if DATABASE_URL.startswith(('postgres://', 'postgresql://')) else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if DATABASES['default']['ENGINE'].endswith('postgresql'):
    DATABASES['default'].setdefault('OPTIONS', {})['connect_timeout'] = 10
    if EN_VERCEL:
        # Requerido con PgBouncer en modo transacción (pooler de Neon/Supabase).
        DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

if EN_VERCEL and not DATABASE_URL:
    raise RuntimeError('Falta DATABASE_URL en Vercel: SQLite no persiste en producción.')

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
# En Vercel no corre collectstatic: WhiteNoise sirve directo desde core/static.
WHITENOISE_USE_FINDERS = True

# ---------------------------------------------------------------------------
# Archivos subidos (imágenes de proyectos, hero, etc.) → Cloudflare R2
# R2 es compatible con S3, por eso se usa django-storages con boto3.
# Si no hay credenciales R2 (desarrollo local), se guardan en /media.
# ---------------------------------------------------------------------------
R2_ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
R2_BUCKET = os.environ.get('R2_BUCKET')                      # público, ej: vc-media
R2_BUCKET_PRIVADO = os.environ.get('R2_BUCKET_PRIVADO')      # privado, ej: vc-privado (evidencia de denuncias)
R2_PUBLIC_DOMAIN = (os.environ.get('R2_PUBLIC_DOMAIN') or '').strip()  # ej: media.vcchile.cl o pub-xxxx.r2.dev
# Acepta el valor con o sin "https://" y sin "/" final (django-storages espera solo el dominio).
R2_PUBLIC_DOMAIN = R2_PUBLIC_DOMAIN.removeprefix('https://').removeprefix('http://').rstrip('/') or None

USAR_R2 = all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET])

STATICFILES_BACKEND = {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'}

if USAR_R2:
    _r2_base = {
        'access_key': R2_ACCESS_KEY_ID,
        'secret_key': R2_SECRET_ACCESS_KEY,
        'endpoint_url': f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        'region_name': 'auto',
        'signature_version': 's3v4',
        'default_acl': None,
        'file_overwrite': False,
        'object_parameters': {'CacheControl': 'public, max-age=31536000, immutable'},
    }
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                **_r2_base,
                'bucket_name': R2_BUCKET,
                'custom_domain': R2_PUBLIC_DOMAIN,   # URLs públicas sin firma
                'querystring_auth': False,
            },
        },
        'privado': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                **_r2_base,
                'bucket_name': R2_BUCKET_PRIVADO or R2_BUCKET,
                'location': '' if R2_BUCKET_PRIVADO else 'privado',
                'querystring_auth': True,            # URL firmada, expira
                'querystring_expire': 600,
                'object_parameters': {'CacheControl': 'private, no-store'},
            },
        },
        'staticfiles': STATICFILES_BACKEND,
    }
    MEDIA_URL = f'https://{R2_PUBLIC_DOMAIN}/' if R2_PUBLIC_DOMAIN else '/media/'
else:
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'privado': {'BACKEND': 'django.core.files.storage.FileSystemStorage',
                    'OPTIONS': {'location': BASE_DIR / 'privado'}},
        'staticfiles': STATICFILES_BACKEND,
    }
    MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Correo (Outlook / Microsoft 365) para avisos del formulario de contacto.
# Ver CORREO_OUTLOOK.md. CORREO_MODO: "smtp", "graph" o vacío (no envía).
# ---------------------------------------------------------------------------
CORREO_MODO = os.environ.get('CORREO_MODO', '').strip().lower()
CORREO_REMITENTE = os.environ.get('CORREO_REMITENTE', '').strip()
CORREO_DESTINO = [d.strip() for d in os.environ.get('CORREO_DESTINO', CORREO_REMITENTE).split(',') if d.strip()]

# Modo smtp
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.office365.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = CORREO_REMITENTE
EMAIL_HOST_PASSWORD = os.environ.get('CORREO_CLAVE', '')
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = CORREO_REMITENTE or 'webmaster@localhost'

# Modo graph (app registrada en Entra ID con permiso Mail.Send de aplicación)
MS_TENANT_ID = os.environ.get('MS_TENANT_ID', '')
MS_CLIENT_ID = os.environ.get('MS_CLIENT_ID', '')
MS_CLIENT_SECRET = os.environ.get('MS_CLIENT_SECRET', '')

# Imprime el traceback de cualquier error 500 en la terminal (local) y en los logs de Vercel,
# aunque DEBUG esté en False.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
        'core': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
