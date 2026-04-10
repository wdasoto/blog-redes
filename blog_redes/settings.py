"""
Django settings for blog_redes project.
"""

from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-0b5_-otn28n&9bfyoh4c$6vxau#wrw0j+x@kh+$vj*xg6#l1$^'
DEBUG = False  # Cambiar a False en producción

# Hosts permitidos (añadir dominios en producción)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de terceros (opcional, para el futuro)
    # 'ckeditor',  # Editor de texto enriquecido (instalar luego con pip)
    
    # Tu app
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_redes.urls'

# Configuración de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta global de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Contexto personalizado para el blog
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_redes.wsgi.application'

# Base de datos SQLite (perfecta para empezar)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización - ESPAÑOL
LANGUAGE_CODE = 'es-es'  # Español de España
TIME_ZONE = 'America/Bogota'  # Cambia a tu zona horaria (America/Mexico_City, America/Argentina/Buenos_Aires, etc.)
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JavaScript, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Carpeta global de archivos estáticos
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para producción (collectstatic)

# Archivos de media (imágenes subidas por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de login
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Tipo de campo auto por defecto (Django 3.2+)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de seguridad básica (para producción activar estas)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
