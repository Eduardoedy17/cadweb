from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from .models import *
from .forms import *

def index(request):
    return render(request, 'index.html')

# --- AUTOCOMPLETE / TESTES (Slide 15) ---
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '')
    try:
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

def teste1(request):
    return render(request, 'testes/teste1.html')

def teste2(request):
    return render(request, 'testes/teste2.html')

# --- CATEGORIA ---
def categoria(request):
    contexto = {'lista': Categoria.objects.all().order_by('-id')}
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
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

def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(instance=categoria)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    contexto = {'form': form, 'titulo': 'Detalhes da Categoria', 'apenas_leitura': True}
    return render(request, 'categoria/formulario.html', contexto)

def editar_categoria(request, id):
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

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    categoria.delete()
    messages.success(request, 'Registro excluído com sucesso!')
    return redirect('categoria')

# --- PRODUTO & ESTOQUE ---
def produto(request):
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)

def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/formulario.html', {'form': form, 'titulo': 'Cadastro de Produto'})

def detalhes_produto(request, id):
    item = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(instance=item)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    return render(request, 'produto/formulario.html', {'form': form, 'titulo': 'Detalhes do Produto', 'apenas_leitura': True})

def editar_produto(request, id):
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

def excluir_produto(request, id):
    item = get_object_or_404(Produto, pk=id)
    item.delete()
    messages.success(request, 'Produto excluído!')
    return redirect('produto')

def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    estoque = produto.estoque 
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto)
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
         form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form,})

# --- CLIENTE ---
def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('nome')}
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente salvo com sucesso!')
            return redirect('cliente')
    else:
        form = ClienteForm()
    return render(request, 'cliente/formulario.html', {'form': form, 'titulo': 'Cadastro de Cliente'})

def detalhes_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(instance=item)
    for field in form.fields.values():
        field.widget.attrs['disabled'] = 'disabled'
    return render(request, 'cliente/formulario.html', {'form': form, 'titulo': 'Detalhes do Cliente', 'apenas_leitura': True})

def editar_cliente(request, id):
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

def excluir_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    item.delete()
    messages.success(request, 'Cliente excluído!')
    return redirect('cliente')

# --- PEDIDO (Novas Views - Slide 16) ---

def pedido(request):
    """Lista todos os pedidos (Slide 188)"""
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

# ... imports ...

def novo_pedido(request, id):
    """
    Recebe o ID do cliente vindo da lista de clientes.
    Cria um formulário de pedido já vinculado a este cliente.
    """
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado')
            return redirect('cliente')

        # Cria instância com o cliente
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        
        return render(request, 'pedido/formulario.html', {'form': form})
        
    else: # POST
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido')

def editar_pedido(request, id):
    item = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('pedido')
    else:
        form = PedidoForm(instance=item)
    return render(request, 'pedido/form.html', {'form': form})

def excluir_pedido(request, id):
    item = get_object_or_404(Pedido, pk=id)
    item.delete()
    messages.success(request, 'Pedido excluído!')
    return redirect('pedido')