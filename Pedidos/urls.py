from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('listapedido/', views.ListarPedidos.as_view(), name='listapedido'),    
    path('detalhes/<int:pk>', views.Detalhes.as_view(), name='detalhes'),
] 