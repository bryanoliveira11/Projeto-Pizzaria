# Generated by Django 4.1.7 on 2023-04-13 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0003_rename_nome_cliente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='endereco',
            field=models.CharField(max_length=50, verbose_name='Endereço'),
        ),
    ]