# Generated by Django 4.1.7 on 2023-04-17 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itempedido',
            old_name='produto',
            new_name='pizza',
        ),
        migrations.RenameField(
            model_name='itempedido',
            old_name='produto_id',
            new_name='pizza_id',
        ),
        migrations.RenameField(
            model_name='itempedido',
            old_name='variacao',
            new_name='tamanho',
        ),
        migrations.RenameField(
            model_name='itempedido',
            old_name='variacao_id',
            new_name='tamanho_id',
        ),
        migrations.RemoveField(
            model_name='itempedido',
            name='preco_promocional',
        ),
    ]