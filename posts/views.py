from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Categoria

# Vista para la página principal - Lista de artículos
class ListaPostsView(ListView):
    model = Post
    template_name = 'posts/lista.html'
    context_object_name = 'posts'
    paginate_by = 5  # 5 artículos por página
    
    def get_queryset(self):
        # Solo mostrar posts publicados, ordenados por fecha
        return Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activa=True)
        context['posts_destacados'] = Post.objects.filter(
            estado='publicado', 
            destacado=True
        )[:3]
        return context

# Vista para ver un artículo completo
class DetallePostView(DetailView):
    model = Post
    template_name = 'posts/detalle.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(estado='publicado')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Incrementar contador de vistas
        post = self.get_object()
        post.vistas += 1
        post.save()
        
        # Posts relacionados (misma categoría)
        context['relacionados'] = Post.objects.filter(
            categoria=post.categoria,
            estado='publicado'
        ).exclude(id=post.id)[:3]
        
        context['categorias'] = Categoria.objects.filter(activa=True)
        return context

# Vista para filtrar por categoría
class CategoriaView(ListView):
    model = Post
    template_name = 'posts/categoria.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Post.objects.filter(
            categoria=self.categoria,
            estado='publicado'
        ).order_by('-fecha_publicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        context['categorias'] = Categoria.objects.filter(activa=True)
        return context

# Vista para la página de inicio (opcional, puede redirigir a lista)
def inicio(request):
    return render(request, 'posts/inicio.html')

