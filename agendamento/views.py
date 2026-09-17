from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Usuario, Agendamento
from .decorators import somente_tipo


HORARIO_INICIO = 8   # 08:00
HORARIO_FIM = 22     # 22:00
INTERVALO_MINUTOS = 30


def gerar_horarios():
    horarios = []
    atual = datetime.strptime(f'{HORARIO_INICIO}:00', '%H:%M')
    fim = datetime.strptime(f'{HORARIO_FIM}:00', '%H:%M')
    while atual < fim:
        horarios.append(atual.strftime('%H:%M'))
        atual += timedelta(minutes=INTERVALO_MINUTOS)
    return horarios


def index(request):
    return render(request, 'index.html')


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'erro': 'Esse usuário já existe!'})

        user = Usuario.objects.create_user(
            username=username,
            password=senha,
            email=email,
            first_name=nome,
            telefone=telefone,
            data_nascimento=data_nascimento or None,
            sexo=sexo,
            tipo='cliente'
        )

        auth_login(request, user)
        return redirect('agendamentos')

    return render(request, 'cadastro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.tipo == 'gerente':
                return redirect('dashboard_gerente')
            elif user.tipo == 'barbeiro':
                return redirect('painel_barbeiro')
            else:
                return redirect('agendamentos')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@somente_tipo('cliente')
def agendamentos(request):
    barbeiros = Usuario.objects.filter(tipo='barbeiro')

    if request.method == 'POST':
        barbeiro_id = request.POST.get('barbeiro')
        servico = request.POST.get('servico')
        data = request.POST.get('data')
        horario = request.POST.get('horario')

        if not barbeiro_id or not horario:
            messages.error(request, 'Escolha o barbeiro e o horário.')
            return redirect('agendamentos')

        ja_existe = Agendamento.objects.filter(barbeiro_id=barbeiro_id, data=data, horario=horario).exists()
        if ja_existe:
            messages.error(request, 'Esse horário acabou de ser reservado por outra pessoa. Escolha outro.')
            return redirect('agendamentos')

        Agendamento.objects.create(
            cliente=request.user,
            barbeiro_id=barbeiro_id,
            servico=servico,
            data=data,
            horario=horario,
        )
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('agendamentos')

    meus_agendamentos = Agendamento.objects.filter(cliente=request.user).order_by('data', 'horario')

    return render(request, 'agendamentos.html', {
        'barbeiros': barbeiros,
        'precos': Agendamento.PRECOS,
        'meus_agendamentos': meus_agendamentos,
    })


def horarios_disponiveis(request):
    barbeiro_id = request.GET.get('barbeiro')
    data = request.GET.get('data')

    todos = gerar_horarios()

    if not barbeiro_id or not data:
        return JsonResponse({'horarios': todos})

    ocupados = Agendamento.objects.filter(barbeiro_id=barbeiro_id, data=data).values_list('horario', flat=True)
    ocupados_str = [h.strftime('%H:%M') for h in ocupados]

    livres = [h for h in todos if h not in ocupados_str]
    return JsonResponse({'horarios': livres})


@somente_tipo('barbeiro')
def painel_barbeiro(request):
    meus_agendamentos = Agendamento.objects.filter(barbeiro=request.user).order_by('data', 'horario')
    return render(request, 'painel_barbeiro.html', {'agendamentos': meus_agendamentos})


@somente_tipo('gerente')
def dashboard_gerente(request):
    total_agendamentos = Agendamento.objects.count()
    barbeiros = Usuario.objects.filter(tipo='barbeiro')
    return render(request, 'dashboard_gerente.html', {
        'total_agendamentos': total_agendamentos,
        'barbeiros': barbeiros,
    })


@somente_tipo('gerente')
def gerenciar_barbeiros(request):
    barbeiros = Usuario.objects.filter(tipo='barbeiro')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return redirect('gerenciar_barbeiros')

        Usuario.objects.create_user(username=username, password=senha, first_name=nome, tipo='barbeiro')

        messages.success(request, 'Barbeiro adicionado!')
        return redirect('gerenciar_barbeiros')

    return render(request, 'gerenciar_barbeiros.html', {'barbeiros': barbeiros})


@somente_tipo('gerente')
def excluir_barbeiro(request, id):
    barbeiro = Usuario.objects.get(id=id, tipo='barbeiro')
    barbeiro.delete()
    messages.success(request, 'Barbeiro removido.')
    return redirect('gerenciar_barbeiros')


@somente_tipo('gerente')
def financas(request):
    agendamentos = Agendamento.objects.select_related('cliente', 'barbeiro').order_by('-data')
    total_agendamentos = agendamentos.count()
    receita_total = sum(ag.preco for ag in agendamentos)
    ticket_medio = receita_total / total_agendamentos if total_agendamentos > 0 else 0

    return render(request, 'financas.html', {
        'agendamentos': agendamentos,
        'total_agendamentos': total_agendamentos,
        'receita_total': receita_total,
        'ticket_medio': ticket_medio,
    })