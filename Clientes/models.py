from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validacpf import valida_cpf
import re

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Nome')
    idade = models.IntegerField()
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    bairro = models.CharField(max_length=30,default=None)
    numero = models.CharField(max_length=5, verbose_name='Número')
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2, default='SP', choices=(
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ))
    
    def __str__(self) -> str:
        return f'{self.usuario}'
    
    def clean(self):
        erros = {}
        
        if len(self.cep ) < 8 or not self.cep or re.search(r'[^0-9]', self.cep):
            erros['cep'] = 'CEP Inválido. Digite os 8 Dígitos do CEP ! '
            
        if not valida_cpf(self.cpf):
            erros['cpf'] = ' Digite Um CPF Válido ! '
            
        if self.idade < 1 or self.idade > 105 or not type(self.idade) == int:
            erros['idade'] = ' Digite Uma Idade Válida ! '
            
        cpf_enviado = self.cpf or None
        cpf_salvo = None
        cliente = Cliente.objects.filter(cpf=cpf_enviado).first()
        
        if cliente:
            cpf_salvo = cliente.cpf
            
            if cpf_salvo is not None and self.pk != cliente.pk:
                erros['cpf'] = ' Este CPF Já Está Em Uso ! '
            
        if erros:
            raise ValidationError(erros)
        