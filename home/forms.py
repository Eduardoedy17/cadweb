from django import forms
from datetime import date
from .models import *

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'categoria': forms.HiddenInput(), 
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'img_base64': forms.HiddenInput(),
        }

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto','qtde']
        widgets = {
            'produto': forms.HiddenInput(),
            'qtde':forms.TextInput(attrs={'class': 'inteiro form-control'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'qtde']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control'}),
        }

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido', 'forma', 'valor']
        widgets = {
            'pedido': forms.HiddenInput(),
            'forma': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'money form-control', 'placeholder': '0,00'}),
        }

    def clean_valor(self):
        valor_str = self.cleaned_data.get('valor')
        try:
            # Converte formato brasileiro 1.234,56 para decimal
            valor_limpo = valor_str.replace('.', '').replace(',', '.')
            valor = float(valor_limpo)
        except:
            valor = 0
            
        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor