from django.db import models
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
        return sum(item.qtde * item.preco for item in self.itempedido_set.all())

    @property
    def qtdeItens(self):
        return self.itempedido_set.count()

    # --- PROPRIEDADES DE PAGAMENTO (Slide 19) ---
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self)

    @property
    def total_pago(self):
        return sum(pgto.valor for pgto in self.pagamentos)

    @property
    def debito(self):
        return self.total - self.total_pago

    # --- DESAFIO: IMPOSTOS E CHAVE DE ACESSO ---
    @property
    def icms(self): return self.total * 0.18
    @property
    def ipi(self): return self.total * 0.04
    @property
    def pis(self): return self.total * 0.0165
    @property
    def cofins(self): return self.total * 0.076
    
    @property
    def total_impostos(self):
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def chave_acesso(self):
        random.seed(self.id)
        aleatorio = random.randint(100000, 999999)
        return f"{self.data_pedido.strftime('%Y%m%d')}{self.id:06d}{aleatorio}"

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