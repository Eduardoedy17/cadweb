from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    # --- Categoria ---
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form/', views.form_categoria, name="form_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name="detalhes_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name="excluir_categoria"),

    # --- Produto ---
    path('produto/', views.produto, name="produto"),
    path('produto/form/', views.form_produto, name="form_produto"),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name="detalhes_produto"),
    path('produto/editar/<int:id>/', views.editar_produto, name="editar_produto"),
    path('produto/excluir/<int:id>/', views.excluir_produto, name="excluir_produto"),

    # --- Cliente ---
    path('cliente/', views.cliente, name="cliente"),
    path('cliente/form/', views.form_cliente, name="form_cliente"),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name="detalhes_cliente"),
    path('cliente/editar/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name="excluir_cliente"),

    # --- Pedido ---
    path('pedido/', views.pedido, name="pedido"),
    path('pedido/form/', views.form_pedido, name="form_pedido"),
    path('pedido/detalhes/<int:id>/', views.detalhes_pedido, name="detalhes_pedido"),
    path('pedido/editar/<int:id>/', views.editar_pedido, name="editar_pedido"),
    path('pedido/excluir/<int:id>/', views.excluir_pedido, name="excluir_pedido"),
]