from django.db import models
from decimal import Decimal
import random

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="E-mail")

    def __str__(self):
        return self.nome
    
    @property
    def data_nascimento_formatada(self):
        if self.datanasc:
            return self.datanasc.strftime("%d/%m/%Y") 
        return None

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    @property
    def estoque(self):
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'

class Pedido(models.Model):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome}"

    @property
    def data_pedidof(self):
        return self.data_pedido.strftime('%d/%m/%Y %H:%M') if self.data_pedido else None 

    @property
    def total(self):
        # Soma todos os itens do pedido usando Decimal para precisão financeira (aceita centavos)
        return sum((item.qtde * item.preco for item in self.itempedido_set.all()), Decimal('0.00'))

    @property
    def qtdeItens(self):
        return self.itempedido_set.count()

    # --- PROPRIEDADES DE PAGAMENTO ---
    @property
    def pagamentos(self):
        # Retorna a lista de pagamentos salvos para este pedido
        return self.pagamento_set.all().order_by('-data_pgto')

    @property
    def total_pago(self):
        # Soma dinâmica dos valores registrados na tabela Pagamento para este pedido
        # Essencial para que a Nota Fiscal mostre os valores recebidos
        return sum((pgto.valor for pgto in self.pagamento_set.all()), Decimal('0.00'))

    @property
    def debito(self):
        # Calcula o saldo devedor subtraindo o total pago do total do pedido em tempo real
        return self.total - self.total_pago

    # --- CÁLCULO DE IMPOSTOS (Utilizando Decimal para evitar erros de arredondamento) ---
    @property
    def icms(self): 
        return (self.total * Decimal('0.18')).quantize(Decimal('0.01'))
    
    @property
    def ipi(self): 
        return (self.total * Decimal('0.04')).quantize(Decimal('0.01'))
    
    @property
    def pis(self): 
        return (self.total * Decimal('0.0165')).quantize(Decimal('0.01'))
    
    @property
    def cofins(self): 
        return (self.total * Decimal('0.076')).quantize(Decimal('0.01'))
    
    @property
    def total_impostos(self):
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def valor_final_nota(self):
        # Valor total considerando os impostos conforme o desafio
        return self.total + self.total_impostos

    @property
    def chave_acesso(self):
        # Geração da chave de acesso única baseada no ID e data
        random.seed(self.id)
        aleatorio = random.randint(100000, 999999)
        data_str = self.data_pedido.strftime('%Y%m%d') if self.data_pedido else "00000000"
        return f"{data_str}{self.id:06d}{aleatorio}300156134409126"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.qtde * self.preco

class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pgto = models.DateTimeField(auto_now_add=True)

    @property
    def data_pgtof(self):
        return self.data_pgto.strftime('%d/%m/%Y %H:%M')