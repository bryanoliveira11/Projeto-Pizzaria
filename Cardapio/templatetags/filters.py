from django.template import Library
from utils import utils

register = Library()

@register.filter
def formata_preco(preco):
    return utils.formata_preco(preco)

@register.filter
def limit_length(text):
    return utils.limit_length(text)

@register.filter
def cart_quantidade_total(carrinho):
    return utils.cart_quantidade_total(carrinho)

@register.filter
def cart_total(carrinho):
    return utils.cart_total(carrinho)

@register.filter
def formata_quantidade(carrinho):
    return utils.formata_quantidade(carrinho)

@register.filter
def formata_unidades(quantidade):
    return utils.formata_unidades(quantidade)

@register.filter
def formata_unidades(quantidade):
    return utils.formata_itens(quantidade)