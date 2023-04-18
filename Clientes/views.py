from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from . import models
import copy

class BaseForms(View):    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {})) # copiando o carrinho da sessão
        
        self.perfil = None
        
        if self.request.user.is_authenticated:
            
            self.perfil = models.Cliente.objects.filter(usuario = self.request.user).first()
        
            self.contexto = {
                'userForm' : forms.FormCadastro(data = self.request.POST or None, usuario=self.request.user, instance=self.request.user),
                'clienteForm' : forms.ClienteForm(data = self.request.POST or None, instance=self.perfil)
            }
            
        else:
            
            self.contexto = {
                'userForm' : forms.FormCadastro(data = self.request.POST or None),
                'clienteForm' : forms.ClienteForm(data = self.request.POST or None)
            }
            
        self.userForm = self.contexto['userForm']
        self.clienteForm = self.contexto['clienteForm']
        
        self.renderizar = render(self.request, self.template_name, self.contexto)
        
    def get(self,*args, **kwargs):
        return self.renderizar

class Cadastrar(BaseForms):
    template_name = 'Clientes/cadastro.html'
    
    def post(self, *args, **kwargs):
        
        if not self.userForm.is_valid() or not self.clienteForm.is_valid():
            messages.error(self.request, 'Existem Erros no Seu Cadastro ! ')
            return self.renderizar
        
        username = self.userForm.cleaned_data.get('username')
        senha = self.userForm.cleaned_data.get('senha')
        email = self.userForm.cleaned_data.get('email')
        primeiro_nome = self.userForm.cleaned_data.get('first_name')
        ultimo_nome = self.userForm.cleaned_data.get('last_name')
        
        # validações para o usuário já logado, ou seja, alteração de dados da conta
        
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = str(username)
            
            if senha:
                usuario.set_password(senha)
                
            usuario.email = email
            usuario.first_name = primeiro_nome
            usuario.last_name = ultimo_nome
            usuario.save()
            
            if not self.perfil:
                self.clienteForm.cleaned_data['usuario'] = usuario
                perfil = models.Cliente(**self.clienteForm.cleaned_data)
                perfil.save()
                
            else:
                perfil = self.clienteForm.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
                messages.success(self.request, 'Dados Alterados Com Sucesso. Refaça Seu Login ! ')
                return redirect('cliente:login')
                
        # usuário que não está logado, ou seja, um cadastro novo no banco de dados
                
        else:
            usuario = self.userForm.save(commit=False)
            usuario.set_password(senha)
            usuario.save()
            
            perfil = self.clienteForm.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            messages.success(self.request, 'Cadastro Realizado com Sucesso. Faça o Login por Aqui ou Através da Aba Conta > Login ! ')
        
        if senha:
            autentica = authenticate(self.request, user=usuario, password=senha)
            
            if autentica:
                login(self.request, user=usuario)
        
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        return redirect('cliente:login')
    
    
class Login(BaseForms):
    template_name = 'Clientes/login.html'

    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')
        
        if not usuario or not senha:  # se não estiver preenchido
            messages.error(self.request, 'Endereço de Email ou Senha Inválidos ! ')
            return redirect('cliente:login')
        
        cliente = authenticate(self.request, username=usuario, password=senha)
        
        if not cliente: # se não autenticar no banco de dados
            messages.error(self.request, 'Endereço de Email ou Senha Inválidos ! ')
            return redirect('cliente:login')
        
        login(self.request, user=cliente)
        messages.success(self.request, f'Login na Conta {usuario} Feito Com Sucesso ! ')
        return redirect('cardapio:pizzas')
    
    
class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho')) # copiando carrinho para não perder no logout
        logout(self.request) # logout
        
        self.request.session['carrinho'] = carrinho # passando o carrinho copiado para a nova sessão
        self.request.session.save() # salvando sessão
        
        messages.success(self.request, 'Logout Efetuado. Até a Próxima ! ')
        return redirect('cardapio:pizzas')
