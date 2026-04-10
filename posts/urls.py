from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaPostsView.as_view(), name='lista_posts'),
    path('post/<slug:slug>/', views.DetallePostView.as_view(), name='detalle_post'),
    path('categoria/<slug:slug>/', views.CategoriaView.as_view(), name='categoria_detalle'),
]
