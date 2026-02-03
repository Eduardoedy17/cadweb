from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # Categorias
    path('categoria/', views.categoria, name='categoria'),
    path('form_categoria/', views.form_categoria, name='form_categoria'),
    path('exibir_categoria/<int:id>/', views.exibir_categoria, name='exibir_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('excluir_categoria/<int:id>/', views.excluir_categoria, name='excluir_categoria'),

    # Clientes
    path('cliente/', views.cliente, name='cliente'),
    path('form_cliente/', views.form_cliente, name='form_cliente'),
    path('detalhes_cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir_cliente/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    # Produtos
    path('produto/', views.produto, name='produto'),
    path('form_produto/', views.form_produto, name='form_produto'),
    path('detalhes_produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('excluir_produto/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('estoque/<int:id>/', views.estoque, name='estoque'),

    # Pedidos
    path('pedido/', views.pedido, name='pedido'),
    path('form_pedido/', views.form_pedido, name='form_pedido'),
    path('detalhes_pedido/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('editar_pedido/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('excluir_pedido/<int:id>/', views.excluir_pedido, name='excluir_pedido'),
    
    # Itens do Pedido
    path('form_item_pedido/<int:id>/', views.form_item_pedido, name='form_item_pedido'),
    path('excluir_item_pedido/<int:id>/', views.excluir_item_pedido, name='excluir_item_pedido'),

    # Pagamentos e Nota Fiscal
    path('pedido/pagamento/<int:id>/', views.form_pagamento, name='form_pagamento'),
    path('pedido/excluir_pagamento/<int:id>/', views.excluir_pagamento, name='excluir_pagamento'),
    path('pedido/nota_fiscal/<int:id>/', views.nota_fiscal, name='nota_fiscal'),
]