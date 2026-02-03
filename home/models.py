from django.db import models
import random

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()
    def __str__(self): return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="E-mail")
    def __str__(self): return self.nome
    @property
    def data_nascimento_formatada(self):
        return self.datanasc.strftime("%d/%m/%Y") if self.datanasc else None

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)
    def __str__(self): return self.nome
    @property
    def estoque(self):
        obj, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return obj

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

class Pedido(models.Model):
    STATUS_CHOICES = [(1, 'Novo'), (2, 'Em Andamento'), (3, 'Concluído'), (4, 'Cancelado')]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    @property
    def data_pedidof(self): return self.data_pedido.strftime('%d/%m/%Y %H:%M')
    
    @property
    def total(self):
        return sum(item.qtde * item.preco for item in self.itempedido_set.all())

    # --- REQUISITOS PAGAMENTO ---
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)

    @property
    def total_pago(self):
        return sum(p.valor for p in self.pagamentos)

    @property
    def debito(self):
        return self.total - self.total_pago

    # --- DESAFIO IMPOSTOS E CHAVE ---
    @property
    def icms(self): return self.total * 0.18
    @property
    def ipi(self): return self.total * 0.04
    @property
    def pis(self): return self.total * 0.0165
    @property
    def cofins(self): return self.total * 0.076
    @property
    def total_impostos(self): return self.icms + self.ipi + self.pis + self.cofins

    @property
    def chave_acesso(self):
        random.seed(self.id)
        return f"{self.data_pedido.strftime('%Y%m%d')}{self.id:06d}{random.randint(100000, 999999)}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class Pagamento(models.Model):
    FORMA_CHOICES = [(1, 'Dinheiro'), (2, 'Cartão'), (3, 'Pix'), (4, 'Outra')]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pgto = models.DateTimeField(auto_now_add=True)