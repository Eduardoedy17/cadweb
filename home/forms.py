from django import forms
from .models import *
from decimal import Decimal

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '000.000.000-00'}),
            'datanasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'img_base64': forms.HiddenInput(),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'status']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:        
        model = ItemPedido
        fields = ['produto', 'qtde', 'preco']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'qtde': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido', 'forma', 'valor']
        widgets = {
            'pedido': forms.HiddenInput(),
            'forma': forms.Select(attrs={'class': 'form-control'}),
            # Campo de texto para suportar a máscara jQuery
            'valor': forms.TextInput(attrs={'class': 'money form-control', 'placeholder': '0,00'}),
        }

    def clean_valor(self):
        valor_raw = self.cleaned_data.get('valor')
        
        # Converte para string para garantir a limpeza dos caracteres da máscara
        valor_str = str(valor_raw)
        
        try:
            # 1. Remove o ponto separador de milhar (ex: 1.250,50 -> 1250,50)
            # 2. Substitui a vírgula decimal por ponto (ex: 1250,50 -> 1250.50)
            valor_limpo = valor_str.replace('.', '').replace(',', '.')
            valor_decimal = Decimal(valor_limpo)
        except (ValueError, TypeError, Exception):
            raise forms.ValidationError("Informe um valor numérico válido (ex: 1.250,50).")

        if valor_decimal <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
            
        return valor_decimal

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['qtde']
        widgets = {
            'qtde': forms.NumberInput(attrs={'class': 'form-control'}),
        }