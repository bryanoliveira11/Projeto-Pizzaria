# Generated by Django 4.1.7 on 2023-04-17 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0002_rename_produto_itempedido_pizza_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='qtd_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]