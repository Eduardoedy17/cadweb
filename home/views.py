from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def index(request): 
    return render(request, 'index.html')

# --- VIEWS DE PAGAMENTO ---
@login_required
def form_pagamento(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            if pagamento.valor > pedido.debito:
                messages.error(request, f"Erro: Valor excede o débito de R$ {pedido.debito}")
            else:
                pagamento.save()
                messages.success(request, "Pagamento registrado!")
                return redirect('form_pagamento', id=id)
    else:
        form = PagamentoForm(initial={'pedido': pedido})
    return render(request, 'pedido/pagamento.html', {'pedido': pedido, 'form': form})

@login_required
def excluir_pagamento(request, id):
    pg = get_object_or_404(Pagamento, pk=id)
    pedido_id = pg.pedido.id
    pg.delete()
    messages.success(request, "Pagamento removido.")
    return redirect('form_pagamento', id=pedido_id)

# --- VIEW NOTA FISCAL ---
@login_required
def nota_fiscal(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    return render(request, 'pedido/nota_fiscal.html', {'pedido': pedido})
