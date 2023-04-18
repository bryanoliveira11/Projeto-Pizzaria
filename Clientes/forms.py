from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from . import models

class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ('cpf', 'idade', 'cep','cidade','estado','endereco', 'bairro', 'numero',)
                
        
class FormCadastro(forms.ModelForm):
    senha = forms.CharField(required=True, widget=forms.PasswordInput, label='Senha', help_text='Mínimo de 6 Caracteres')
    senha_confirmar = forms.CharField(required=True, widget=forms.PasswordInput, label='Confirme Sua Senha')
    
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email' , 'senha', 'senha_confirmar')
        
    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        erro_mensagens = {}
        erro_emailExiste = ' Esse Email Já Está Em Uso ! '
        erro_senhaTamanho = ' A Senha Precisa Ter 6 Caracteres ! '
        erro_senhaDiferente = ' As Senhas Não Batem ! '
        erro_campoObrigatorio = ' Este Campo é Obrigatório '
        erro_usuarioExiste = 'Nome De Usuário Já Está Em Uso '
        erro_alterarUser = f' Não Podemos Alterar Seu Usuário. Por Favor Use " {self.usuario} " '
        
        usuario = cleaned.get('username')
        email = cleaned.get('email')
        senha = cleaned.get('senha')
        senha_confirmar = cleaned.get('senha_confirmar')
        
        usuario_database = User.objects.filter(username=usuario).first()
        email_database = User.objects.filter(email=email).first()
        
        # Validações Para o Cadastro - Usuário JÁ logado, alteração de dados.
        
        if not senha:
            erro_mensagens['senha'] = erro_campoObrigatorio
            erro_mensagens['senha_confirmar'] = erro_campoObrigatorio
        else:
            pass
        
        if self.usuario:
            
            if str(self.usuario) != str(usuario_database): # não deixar alterar usuário
                erro_mensagens['username'] = erro_alterarUser
            
            if usuario_database: # usuário já existente
                if usuario != usuario_database.username:
                    erro_mensagens['username'] = erro_usuarioExiste
                    
            if email_database and usuario_database: # email já existente no banco = erro
                if email != usuario_database.email:
                   erro_mensagens['email'] = erro_emailExiste
                else: # email não mudou ou mudou e não existe ainda = fazer nada, apenas o update que vem da view
                    pass
               
            if senha: # senhas divergentes
                if senha != senha_confirmar:
                   erro_mensagens['senha'] = erro_senhaDiferente
                   erro_mensagens['senha_confirmar'] = erro_senhaDiferente
                       
                if len(senha) < 6: # senha curta 
                   erro_mensagens['senha'] = erro_senhaTamanho  

    
        else: # usuário não logado, cadastro
            
            if usuario_database: # usuário já existe
                erro_mensagens['username'] = erro_usuarioExiste

            if email_database: # email já existe
                erro_mensagens['email'] = erro_emailExiste

            if not senha: # senha não preenchida
                erro_mensagens['senha'] = erro_campoObrigatorio
            
            if not senha_confirmar:
                erro_mensagens['senha_confirmar'] = erro_campoObrigatorio

            if senha != senha_confirmar: # senhas diferentes
                erro_mensagens['senha'] = erro_senhaDiferente
                erro_mensagens['senha_confirmar'] = erro_senhaDiferente
                
            if len(senha) < 6: # senha curta 
                erro_mensagens['senha'] = erro_senhaTamanho  
            
        if erro_mensagens:
            raise forms.ValidationError(erro_mensagens)
        