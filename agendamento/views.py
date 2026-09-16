from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Perfil, Cliente, Agendamento

# Create your views here.

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'erro': 'Esse usuário já existe!'})
        
        
        user = User.objects.create_user(
            username = username,
            password = senha,
            email = email,
            first_name = nome
        )
        
        Perfil.objects.create(usuario=user, tipo='cliente')
        
        Cliente.objects.create(
            user = user,
            telefone = telefone,
            data_nascimento = data_nascimento,
            sexo = sexo
        )
        
        auth_login(request, user)
        return redirect('agendamentos')
    
    return render(request, 'cadastro.html')

def index(request):
    return render(request, 'index.html')

@login_required
def agendamentos(request):
    if request.method == 'POST':
        servico = request.POST.get('servico')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        
        Agendamento.objects.create(
            cliente=request.user,
            servico = servico,
            data_agendamento = data,
            horario = horario,
        )
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('agendamentos')
    return render(request, 'agendamentos.html')