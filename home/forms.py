from django import forms
from datetime import date
from .models import *

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome  

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': '000.000.000-00'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'dd/mm/aaaa'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > date.today():
            raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            # Alteração Slide 220: Categoria vira HiddenInput
            'categoria': forms.HiddenInput(), 
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control', 'maxlength': '500', 'placeholder': '0.000,00'}),
            'img_base64': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'produtos', 'status']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'produtos': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: 150px;'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto','qtde']
        widgets = {
            'produto': forms.HiddenInput(),
            'qtde':forms.TextInput(attrs={'class': 'inteiro form-control',}),
        }