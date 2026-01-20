from django.db import models

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

    # Slide 30: Atributo estoque em Produto (relacionamento)
    @property
    def estoque(self):
        # Tenta buscar o estoque, se não existir, cria um novo com qtde 0
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('E', 'Entregue'),
        ('C', 'Cancelado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    produtos = models.ManyToManyField(Produto)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"

# Slide 22: Model Estoque
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'