from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def index(request):
    """Renderiza a página inicial do dashboard."""
    return render(request, 'index.html')

# --- AUTOCOMPLETE / TESTES ---

@login_required
def buscar_dados(request, app_modelo):
    """Gera dados JSON para campos de autocomplete."""
    termo = request.GET.get('q', '')
    try:
        app, modelo_nome = app_modelo.split('.')
        modelo = apps.get_model(app, modelo_nome)
    except:
        return JsonResponse({'error': 'Erro no modelo'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

@login_required
def teste1(request):
    """Página de teste de autocomplete estático."""
    return render(request, 'testes/teste1.html')

@login_required
def teste2(request):
    """Página de teste de autocomplete Ajax genérico."""
    return render(request, 'testes/teste2.html')

# --- CATEGORIA ---

@login_required
def categoria(request):
    """Lista todas as categorias ordenadas por ID decrescente."""
    contexto = {'lista': Categoria.objects.all().order_by('-id')}
    return render(request, 'categoria/lista.html', contexto)

@login_required
def form_categoria(request):
    """Gera o formulário de criação de nova categoria."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro salvo com sucesso!')
            return redirect('categoria')
    else:
        form = CategoriaForm()
    contexto = {'form': form}
    return render(request, 'categoria/formulario.html', contexto)

@login_required
def detalhes_categoria(request, id):
    """Exibe os detalhes de uma categoria em modo de leitura."""
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(instance=categoria)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    contexto = {'form': form, 'titulo': 'Detalhes da Categoria', 'apenas_leitura': True}
    return render(request, 'categoria/formulario.html', contexto)

@login_required
def editar_categoria(request, id):
    """Permite a edição de uma categoria existente."""
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
def excluir_categoria(request, id):
    """Elimina uma categoria do sistema."""
    categoria = get_object_or_404(Categoria, pk=id)
    categoria.delete()
    messages.success(request, 'Registro excluído com sucesso!')
    return redirect('categoria')

# --- PRODUTO & ESTOQUE ---

@login_required
def produto(request):
    """Lista todos os produtos cadastrados."""
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)

@login_required
def form_produto(request):
    """Gera o cadastro de novos produtos."""
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/formulario.html', {'form': form, 'titulo': 'Cadastro de Produto'})

@login_required
def detalhes_produto(request, id):
    """Exibe informações detalhadas de um produto."""
    item = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(instance=item)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    return render(request, 'produto/formulario.html', {'form': form, 'titulo': 'Detalhes do Produto', 'apenas_leitura': True})

@login_required
def editar_produto(request, id):
    """Permite alterar dados de um produto."""
    item = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado!')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=item)
    return render(request, 'produto/formulario.html', {'form': form, 'titulo': 'Editar Produto'})

@login_required
def excluir_produto(request, id):
    """Remove um produto do catálogo."""
    item = get_object_or_404(Produto, pk=id)
    item.delete()
    messages.success(request, 'Produto excluído!')
    return redirect('produto')

@login_required
def ajustar_estoque(request, id):
    """Gera o ajuste manual da quantidade em estoque."""
    produto = get_object_or_404(Produto, pk=id)
    estoque = produto.estoque 
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect('produto')
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})

# --- CLIENTE ---

@login_required
def cliente(request):
    """Lista os clientes por ordem alfabética."""
    contexto = {'lista': Cliente.objects.all().order_by('nome')}
    return render(request, 'cliente/lista.html', contexto)

@login_required
def form_cliente(request):
    """Cadastra um novo cliente no sistema."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente salvo com sucesso!')
            return redirect('cliente')
    else:
        form = ClienteForm()
    return render(request, 'cliente/formulario.html', {'form': form, 'titulo': 'Cadastro de Cliente'})

@login_required
def detalhes_cliente(request, id):
    """Visualiza os dados cadastrais de um cliente."""
    item = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(instance=item)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    return render(request, 'cliente/formulario.html', {'form': form, 'titulo': 'Detalhes do Cliente', 'apenas_leitura': True})

@login_required
def editar_cliente(request, id):
    """Atualiza as informações de um cliente."""
    item = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado!')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=item)
    return render(request, 'cliente/formulario.html', {'form': form, 'titulo': 'Editar Cliente'})

@login_required
def excluir_cliente(request, id):
    """Remove um cliente do sistema."""
    item = get_object_or_404(Cliente, pk=id)
    item.delete()
    messages.success(request, 'Cliente excluído!')
    return redirect('cliente')

# --- PEDIDO ---

@login_required
def pedido(request):
    """Lista todos os pedidos realizados."""
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

@login_required
def novo_pedido(request, id):
    """Inicia um novo pedido para um cliente específico."""
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'GET':
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/formulario.html', {'form': form})
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            pedido.save()
            return redirect('detalhes_pedido', id=pedido.id) 

@login_required
def detalhes_pedido(request, id):
    """Gera a adição de itens e visualização do pedido."""
    pedido = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.preco = item.produto.preco 
            
            estoque_atual = item.produto.estoque
            if estoque_atual.qtde >= item.qtde:
                estoque_atual.qtde -= item.qtde 
                estoque_atual.save()
                item.save() 
                messages.success(request, 'Item adicionado com sucesso!')
            else:
                messages.error(request, 'Estoque insuficiente para este produto!')
            return redirect('detalhes_pedido', id=id)
    else:
        form = ItemPedidoForm()
    
    contexto = {'pedido': pedido, 'form': form}
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def editar_item_pedido(request, id):
    """Ajusta a quantidade de um item já inserido no pedido."""
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    estoque = item.produto.estoque 

    if request.method == 'POST':
        qtde_anterior = item.qtde 
        form = ItemPedidoForm(request.POST, instance=item)
        if form.is_valid():
            item_obj = form.save(commit=False)
            diferenca = item_obj.qtde - qtde_anterior 
            
            if diferenca > 0: 
                if estoque.qtde >= diferenca:
                    estoque.qtde -= diferenca
                    estoque.save()
                    item_obj.save()
                    messages.success(request, 'Item atualizado!')
                else:
                    messages.error(request, 'Estoque insuficiente!')
            else: 
                estoque.qtde += abs(diferenca) 
                estoque.save()
                item_obj.save()
                messages.success(request, 'Item atualizado!')
            return redirect('detalhes_pedido', id=pedido_id)
    else:
        form = ItemPedidoForm(instance=item)
    return render(request, 'pedido/formulario_item.html', {'form': form, 'pedido': item.pedido})

@login_required
def remover_item_pedido(request, id):
    """Remove um item do pedido e devolve a quantidade ao estoque."""
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    estoque = item.produto.estoque
    estoque.qtde += item.qtde
    estoque.save()
    item.delete()
    messages.success(request, 'Item removido e estoque restaurado!')
    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def excluir_pedido(request, id):
    """Elimina um pedido do sistema."""
    item = get_object_or_404(Pedido, pk=id)
    item.delete()
    messages.success(request, 'Pedido excluído!')
    return redirect('pedido')

# --- PAGAMENTO (Slide 19) ---

@login_required
def form_pagamento(request, id):
    """Gera o registro de pagamentos do pedido."""
    pedido = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.pedido = pedido
            
            # CORREÇÃO: Usando objetos Decimal consistentes para comparação 
            # (evita o TypeError e garante precisão financeira)
            if pagamento.valor > pedido.debito:
                messages.error(request, f"Valor superior ao débito de R$ {pedido.debito}")
            else:
                pagamento.save()
                messages.success(request, 'Pagamento registrado!')
                return redirect('form_pagamento', id=id)
    else:
        # Sugere o valor do débito restante no formulário inicial
        form = PagamentoForm(initial={'pedido': pedido, 'valor': pedido.debito})
        
    return render(request, 'pedido/pagamento.html', {'pedido': pedido, 'form': form})

@login_required
def excluir_pagamento(request, id):
    """Remove um registro de pagamento."""
    pg = get_object_or_404(Pagamento, pk=id)
    pedido_id = pg.pedido.id
    pg.delete()
    messages.success(request, 'Pagamento removido.')
    return redirect('form_pagamento', id=pedido_id)

# --- NOTA FISCAL (Slide 19) ---

@login_required
def nota_fiscal(request, id):
    """Exibe a nota fiscal detalhada com cálculos de impostos."""
    pedido = get_object_or_404(Pedido, pk=id)
    return render(request, 'pedido/nota_fiscal.html', {'pedido': pedido})