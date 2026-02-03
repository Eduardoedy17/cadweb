from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    # Autocomplete / Testes
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),

    # Categoria
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form/', views.form_categoria, name="form_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name="detalhes_categoria"),
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name="excluir_categoria"),

    # Produto
    path('produto/', views.produto, name="produto"),
    path('produto/form/', views.form_produto, name="form_produto"),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name="detalhes_produto"),
    path('produto/editar/<int:id>/', views.editar_produto, name="editar_produto"),
    path('produto/excluir/<int:id>/', views.excluir_produto, name="excluir_produto"),
    path('produto/ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),

    # Cliente
    path('cliente/', views.cliente, name="cliente"),
    path('cliente/form/', views.form_cliente, name="form_cliente"),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name="detalhes_cliente"),
    path('cliente/editar/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name="excluir_cliente"),

    # --- PEDIDO ---
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/form/<int:id>', views.novo_pedido, name='novo_pedido'),
    path('pedido/detalhes/<int:id>', views.detalhes_pedido, name='detalhes_pedido'),
    path('pedido/excluir/<int:id>', views.excluir_pedido, name='excluir_pedido'),
    
    # --- ITENS PEDIDO ---
    path('pedido/remover_item/<int:id>', views.remover_item_pedido, name='remover_item_pedido'),
    path('pedido/editar_item/<int:id>', views.editar_item_pedido, name='editar_item_pedido'),

    # --- PAGAMENTOS E NOTA FISCAL ---
    path('pedido/pagamento/<int:id>/', views.form_pagamento, name='form_pagamento'),
    path('pedido/excluir_pagamento/<int:id>/', views.excluir_pagamento, name='excluir_pagamento'),
    path('pedido/nota_fiscal/<int:id>/', views.nota_fiscal, name='nota_fiscal'),
]