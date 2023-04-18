from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .models import Pedido, ItemPedido
from utils import utils

class DispatchLoginRequiredMixin(View): # garantir que o usuário esteja logado
    def dispatch(self,*args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('cliente:login')
        
        return super().dispatch(*args, **kwargs)
        
    def get_queryset(self,*args, **kwargs):
        qs =  super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        return qs
    
class Pagar(DispatchLoginRequiredMixin,DetailView):
    template_name = 'Pedidos/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    
class SalvarPedido(View):
    template_name = 'Pedidos/pagar.html'
    
    def get(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você Precisa Fazer o Login ! ')
            
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho Vázio ! ')
            return redirect('cardapio:pizzas')
        
        
        carrinho = self.request.session.get('carrinho')
        qtd_total_carrinho = utils.cart_quantidade_total(carrinho)
        valor_total = utils.cart_total(carrinho)
        
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total,
            qtd_total=qtd_total_carrinho,
            status='C'
        )
        
        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    pizza=t['pizza_nome'],
                    pizza_id=t['pizza_id'],
                    tamanho=t['tamanho_nome'],
                    tamanho_id=t['tamanho_id'],
                    preco=t['preco_quantitativo'],
                    quantidade=t['quantidade'],
                    imagem=t['imagem'],
                    
                ) for t in carrinho.values()
            ]
        )
        
        del self.request.session['carrinho']
        
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )
    
class ListarPedidos(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'Pedidos/lista.html'
    paginate_by = 10
    ordering = ['-id']
    
class Detalhes(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'Pedidos/detalhe.html'
    pk_url_kwarg = 'pk'
