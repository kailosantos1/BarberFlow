from django.shortcuts import render, redirect
from django.contrib import messages
from agendamento.models import Agendamento

# Create your views here.

def index(request):
    return render(request, 'index.html')

def agendamentos(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        servico = request.POST.get('servico')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        
        Agendamento.objects.create(
            nome = nome,
            telefone = telefone,
            servico = servico,
            data_agendamento = data,
            horario = horario,
        )
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('agendamentos')
    return render(request, 'agendamentos.html')