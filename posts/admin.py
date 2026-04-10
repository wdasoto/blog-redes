from django.contrib import admin
from .models import Categoria, Post, Comentario, ArchivoAdjunto

# Personalizar cómo se ve Categoria en el admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'color', 'activa', 'orden']
    list_filter = ['activa', 'color']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['orden', 'nombre']


# Personalizar cómo se ve Post en el admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 
        'categoria', 
        'autor', 
        'nivel_dificultad', 
        'estado', 
        'destacado',
        'fecha_publicacion',
        'vistas'
    ]
    list_filter = [
        'estado', 
        'categoria', 
        'nivel_dificultad', 
        'destacado',
        'fecha_creacion'
    ]
    search_fields = ['titulo', 'contenido', 'etiquetas', 'resumen']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ['-fecha_creacion']
    
    # Organizar campos en grupos
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('titulo', 'slug', 'subtitulo', 'contenido', 'resumen')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'nivel_dificultad', 'etiquetas')
        }),
        ('Multimedia', {
            'fields': ('imagen_destacada', 'imagen_banner')
        }),
        ('Configuración', {
            'fields': ('autor', 'estado', 'destacado')
        }),
        ('SEO', {
            'fields': ('meta_descripcion', 'palabras_clave'),
            'classes': ('collapse',)  # Sección colapsada
        }),
    )
    
    # Acciones rápidas
    actions = ['publicar_posts', 'destacar_posts']
    
    def publicar_posts(self, request, queryset):
        queryset.update(estado='publicado')
    publicar_posts.short_description = "Publicar posts seleccionados"
    
    def destacar_posts(self, request, queryset):
        queryset.update(destacado=True)
    destacar_posts.short_description = "Marcar como destacados"


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['post', 'autor', 'texto_truncado', 'fecha_creacion', 'aprobado']
    list_filter = ['aprobado', 'fecha_creacion']
    actions = ['aprobar_comentarios']
    
    def texto_truncado(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_truncado.short_description = 'Comentario'
    
    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"


@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'post', 'descargas', 'fecha_subida']
    list_filter = ['fecha_subida']
    search_fields = ['nombre', 'descripcion']

