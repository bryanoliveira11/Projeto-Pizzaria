from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib import messages
from Clientes.models import Cliente
from . import models

class ListaPizzas(ListView): # criando classe das pizzas e linkando o html
    model = models.Pizza
    template_name = 'Cardapio/cardapio.html'
    context_object_name = 'cardapio'
    paginate_by = 6
    
    
class DetalhesPizzas(DetailView): # criando classe dos detalhes e linkando o html
    model = models.Pizza
    template_name = 'Cardapio/detalhes.html'
    context_object_name = 'pizza'
    slug_url_kwarg = 'slug' # slug do banco de dados que vai na barra de pesquisa
    
    
class Pesquisa(ListaPizzas): # class para o queryset da barra de pesquisa
    def get_queryset(self, *args, **kwargs):
        pesquisa = self.request.GET.get('pesquisa') or self.request.session['pesquisa']
        qs = super().get_queryset(*args, **kwargs)
        
        if not pesquisa:
            return qs
        
        self.request.session['pesquisa'] = pesquisa     
        
        qs = qs.filter( # query set para filtrar por nome ou sabor da descrição
            Q(nome__icontains= pesquisa) |
            Q(descricao__icontains= pesquisa))       
        
        self.request.session.save()
        return qs
    
    
class AdicionarAoCarrinho(View):
    def get(self,*args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('cardapio:pizzas'))
        id_tamanho = self.request.GET.get('tid')
        
        if not id_tamanho:
            messages.error(self.request, 'Pizza não Existe !')
            return redirect(http_referer)
        
        pizza_tamanhos = get_object_or_404(models.PizzaTamanhos, id=id_tamanho)
        pizza = pizza_tamanhos.pizza
        pizza_id = pizza.pk
        pizza_nome = pizza.nome
        tamanho_nome = pizza_tamanhos.tamanho
        preco_unitario = pizza_tamanhos.preco
        quantidade = 1
        slug = pizza.slug
        imagem = pizza.imagem
        
        if imagem: # salvando o nome da imagem na var, caso contrário não salva na sessão.
            imagem = imagem.name
        else:
            imagem = ''
        
        if not self.request.session.get('carrinho'): # caso não exista nenhum carrinho na sessão do usuário
            self.request.session['carrinho'] = {} # criando dicionario que será o carrinho e salvando na sessão
            self.request.session.save() 
            
        carrinho = self.request.session['carrinho']
        
        # caso o id da pizza já existir no carrinho, vai adicionar + 1 na quantidade
        
        if id_tamanho in carrinho:
            quantidade_carrinho = carrinho[id_tamanho]['quantidade'] # pega a chave quantidade do dicionario carrinho
            quantidade_carrinho += 1 # adicionando + 1
            
            carrinho[id_tamanho]['quantidade'] = quantidade_carrinho # atribuindo a quantidade no dicionario
            carrinho[id_tamanho]['preco_quantitativo'] = preco_unitario * quantidade_carrinho # calculando total para o produto
        
        else:
            carrinho[id_tamanho] = {
                'pizza_id': pizza_id,
                'pizza_nome': pizza_nome,
                'tamanho_nome': tamanho_nome,
                'tamanho_id': id_tamanho,
                'preco_unitario': preco_unitario,
                'preco_quantitativo': preco_unitario, # preco unitario * quantidade,
                'quantidade': quantidade, # quantidade 1 por padrão
                'slug': slug,
                'imagem': imagem,
            }
            
        self.request.session.save() # salvando carrinho na sessão
        
        messages.success(self.request, f'Pizza de {tamanho_nome.title()} Adicionado ao Carrinho {carrinho[id_tamanho]["quantidade"]}x')
        
        return redirect(http_referer)
    
    
class RemoverDoCarrinho(View):
    def get(self,*args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('cardapio:pizzas'))
        id_tamanho = self.request.GET.get('tid')
        
        if not id_tamanho: # se não existir o id da url
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'): # se o carrinho não existir
            return redirect(http_referer)

        if id_tamanho not in self.request.session['carrinho']: # se o produto id não existir no carrinho
            return redirect(http_referer)
        
        
        carrinho = self.request.session['carrinho'][id_tamanho]
        
        messages.success(self.request, f'O Produto {carrinho["tamanho_nome"].title()} Foi Removido do Carrinho ! ')
        
        del self.request.session['carrinho'][id_tamanho]
        self.request.session.save()
        return redirect(http_referer)

            
class Carrinho(View):
    def get(self,*args, **kwargs):
        context = {'carrinho': self.request.session.get('carrinho', {})}
        return render(self.request, 'Cardapio/carrinho.html', context)
    
    
class ResumoDoPedido(View):
    def get(self, *args, **kwargs):
        
        try:
            
            if not self.request.user.is_authenticated:
                messages.error(self.request, 'Faça o Login Antes de Acessar Esta Tela ! ')
                return redirect('cliente:login')
        
            cliente = Cliente.objects.filter(usuario=self.request.user).exists()

            if not cliente:
                messages.error(self.request, 'Cliente Não Cadastrado')
                return redirect('cliente:cadastro')

            context = {
                'usuario': self.request.user,
                'carrinho': self.request.session['carrinho'],
            }

            return render(self.request, 'Cardapio/resumodopedido.html', context)
        
        except Exception:
            messages.error(self.request, 'Um Erro Ocorreu, Certifique-se de Adicionar Algo no Carrinho !')
            return redirect('cardapio:pizzas')