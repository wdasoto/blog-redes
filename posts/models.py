
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Categoria(models.Model):
    """Categorías para organizar los artículos de redes"""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(
        max_length=20,
        choices=[
            ('blue', 'Azul - Cisco'),
            ('green', 'Verde - Seguridad'),
            ('orange', 'Naranja - Wireless'),
            ('purple', 'Púrpura - Cloud'),
            ('red', 'Rojo - Troubleshooting'),
            ('gray', 'Gris - General'),
        ],
        default='blue'
    )
    icono = models.CharField(max_length=50, blank=True, help_text="Emoji o clase de icono")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['orden', 'nombre']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('categoria_detalle', kwargs={'slug': self.slug})


class Post(models.Model):
    """Artículos del blog de redes de datos"""
    
    # Niveles de dificultad para redes
    NIVEL_CHOICES = [
        ('principiante', '🟢 Principiante (CCNA)'),
        ('intermedio', '🟡 Intermedio (CCNP)'),
        ('avanzado', '🟠 Avanzado (CCIE)'),
        ('experto', '🔴 Experto / Arquitectura'),
    ]
    
    # Estado del post
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    ]
    
    # Campos principales
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    subtitulo = models.CharField(max_length=300, blank=True)
    contenido = models.TextField()
    resumen = models.TextField(
        max_length=500, 
        blank=True,
        help_text="Breve descripción para la lista de artículos"
    )
    
    # Relaciones
    autor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    
    # Metadatos del contenido
    nivel_dificultad = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='principiante'
    )
    etiquetas = models.CharField(
        max_length=300,
        blank=True,
        help_text="Separadas por comas: Cisco, Packet Tracer, VLAN, etc."
    )
    
    # Multimedia
    imagen_destacada = models.ImageField(
        upload_to='posts/featured/%Y/%m/',
        blank=True,
        null=True,
        help_text="Imagen principal del artículo"
    )
    imagen_banner = models.ImageField(
        upload_to='posts/banners/%Y/%m/',
        blank=True,
        null=True,
        help_text="Imagen grande para el encabezado"
    )
    
    # Configuración y estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='borrador'
    )
    destacado = models.BooleanField(
        default=False,
        help_text="Aparecerá en la sección de destacados"
    )
    
    # Contadores (se actualizarán manualmente o con señales)
    vistas = models.PositiveIntegerField(default=0)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    
    # SEO
    meta_descripcion = models.CharField(
        max_length=160,
        blank=True,
        help_text="Descripción para Google (SEO)"
    )
    palabras_clave = models.CharField(
        max_length=200,
        blank=True,
        help_text="Palabras clave para SEO"
    )
    
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_publicacion', '-fecha_creacion']
        indexes = [
            models.Index(fields=['-fecha_publicacion']),
            models.Index(fields=['estado', '-fecha_creacion']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generar slug si no existe
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Actualizar fecha de publicación si cambia a publicado
        if self.estado == 'publicado' and not self.fecha_publicacion:
            from django.utils import timezone
            self.fecha_publicacion = timezone.now()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('post_detalle', kwargs={'slug': self.slug})
    
    @property
    def get_nivel_color(self):
        """Devuelve el color asociado al nivel"""
        colores = {
            'principiante': 'success',
            'intermedio': 'warning',
            'avanzado': 'orange',
            'experto': 'danger',
        }
        return colores.get(self.nivel_dificultad, 'secondary')
    
    @property
    def lista_etiquetas(self):
        """Devuelve las etiquetas como lista"""
        if self.etiquetas:
            return [tag.strip() for tag in self.etiquetas.split(',')]
        return []


class Comentario(models.Model):
    """Comentarios en los artículos"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'Comentario de {self.autor} en {self.post}'


class ArchivoAdjunto(models.Model):
    """Archivos descargables (labs, configs, etc.)"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='adjuntos'
    )
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='posts/adjuntos/%Y/%m/')
    descripcion = models.TextField(blank=True)
    descargas = models.PositiveIntegerField(default=0)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Archivo Adjunto"
        verbose_name_plural = "Archivos Adjuntos"
    
    def __str__(self):
        return self.nombre
