from django.urls import path
from . import views

app_name = 'cardapio'

urlpatterns = [
    path('', views.ListaPizzas.as_view(), name='pizzas'),
    path('<slug>', views.DetalhesPizzas.as_view(), name='detalhes'),
    path('pesquisa/', views.Pesquisa.as_view(), name='pesquisa'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('resumodopedido/', views.ResumoDoPedido.as_view(), name='resumodopedido'),
] 