from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from .models import *
from .util import *
from django.contrib.auth import authenticate, login, logout
from rolepermissions.checkers import has_role
from django.contrib import messages
# has_role_decorator --> verifica o grupo
# has_permissions_decorator --> verifica a permissão
# Create your views here.

def redirecionar_home(request):
    if request.user.is_authenticated:
        if has_role(request.user, 'artista') and has_role(request.user, 'comprador'):
            return redirect('index')
        
        elif has_role(request.user, 'comprador') or has_role(request.user, 'artista'):
            return redirect('index')
    return redirect('index')


def index (request):
    return render(request, 'index.html',)

def criar_usuario(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        conf_senha = request.POST.get('conf_senha')
        tipo = request.POST.get('tipo')
        
        #verificar campos obrigatorios
        if not all([nome_completo, usuario, email, senha, conf_senha, tipo]):
            messages.error(request, "Todos os campos são obrigratorios!")
            return redirect('criar_usuario')
        
        #verificar senhas
        if senha != conf_senha:
            messages.error(request, "As senhas não coincidem!")
            return redirect('criar_usuario')
           
        #verificar email e username
        if Usuarios.objects.filter(username=usuario, email=email).exists():
            return HttpResponse("o nome de usuario ja esta em uso")
        
        #criar usuario
        user = Usuarios.objects.create_user(username = usuario, email= email, password = conf_senha)
        user.nome_completo = nome_completo
        user.tipo = tipo
        user.save()
        
        if tipo == 'oferecer':
            assign_role(user, 'artista')
            messages.success(request, 'Usuário salvo como artista!')
        
        if tipo == 'contratar':
            assign_role(user, 'comprador')
            messages.success(request, 'Usuário salvo como artista!')
            
        if tipo == 'hibrido':
            assign_role(user, 'comprador')
            assign_role(user, 'artista')
            
        return redirect('login_view')
    return render(request, 'cadastro.html')

def ver_usuario(request):
    usuarios = Usuarios.objects.all()
    dados = {'usuarios': usuarios}
    return render(request, 'ver_usuarios.html', dados)

def login_view(request):
    from django.contrib.auth import get_user_model
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        Usuarios = get_user_model()
        
        try:
             #verifica se existe um usuário com esse username e email ao mesmo tempo
            user_obj = Usuarios.objects.get(username=usuario, email=email)
            
             #autentica com o username e senha 
            user = authenticate(request, username=user_obj.username, password=senha)
        
            if user is not None:
                login(request, user)
                return redirect('redirecionar_home')
                
            else:
                messages.error(request, "Senha invalida. Verifique se você digitou sua senha coretamente.")
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuário ou e-mail inválido. Verifique os dados e tente novamente.")
                
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def redefinir_senha(request):
    usuario = request.user.id
    novo_usuario = get_object_or_404(Usuarios, pk=usuario)
    if request.method == "POST":
        senha_antiga = novo_usuario.password
        nova_senha = request.POST.get('nova_senha')
        conf_senha = request.POST.get('conf_senha')
        
        print(nova_senha, conf_senha, novo_usuario.check_password(senha_antiga))
        
        if novo_usuario.check_password(senha_antiga):
            if nova_senha == conf_senha and len(nova_senha) >= 8:
                novo_usuario.set_password(nova_senha)
                novo_usuario.save()
                messages.success(request, 'Senha alterada com sucesso')
                
                return redirect('login_view')
            else:
                messages.error(request, "Verifique se você esta digitando a senha corretamente, a senha tem que ser maior que 8 digitos.")  
                return redirect('redefinir_senha')
            
    return render(request, 'redefinir_senha.html')      
