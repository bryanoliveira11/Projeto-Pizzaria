from django.utils.text import Truncator

def formata_preco(preco):
    return f'R$ {preco:.2f}'.replace('.', ',')

def limit_length(text):
    return Truncator(text).chars(33)

def cart_quantidade_total(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_total(carrinho):
    return sum(
        [
            item.get('preco_quantitativo')
            if item.get('preco_quantitativo')
            else item.get('preco_unitario')
            for item in carrinho.values()
        ]
        
    )

def formata_quantidade(carrinho):
    quantidade = sum([item['quantidade'] for item in carrinho.values()])
    
    if quantidade == 1:
        return f'{quantidade} Item'
    else:
        return f'{quantidade} Itens'
    
def formata_unidades(quantidade):
    
    if quantidade == 1:
        return f'{quantidade} Unidade'
    else:
        return f'{quantidade} Unidades'
    
def formata_itens(quantidade):
    
    if quantidade == 1:
        return f'{quantidade} Item'
    else:
        return f'{quantidade} Itens'