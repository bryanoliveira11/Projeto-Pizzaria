from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Usuário')
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField(default=0)
    status = models.CharField(
        default='C', max_length=1, choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )
    
    def __str__(self):
        return f'Pedido N. {self.pk}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pizza = models.CharField(max_length=255)
    pizza_id = models.PositiveIntegerField()
    tamanho = models.CharField(max_length=255)
    tamanho_id = models.PositiveIntegerField()
    preco = models.FloatField()
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)
    
    def __str__(self):
        return f'Item do {self.pedido}'
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'