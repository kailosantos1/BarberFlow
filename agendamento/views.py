from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Usuario, Agendamento, Empresa, Lead
from .decorators import somente_tipo

HORARIO_INICIO = 8
HORARIO_FIM = 22
INTERVALO_MINUTOS = 30

def landing(request):
    if request.method == 'POST':
        Lead.objects.create(
            nome=request.POST.get('nome'),
            email=request.POST.get('email'),
            telefone=request.POST.get('telefone'),
            nome_barbearia=request.POST.get('nome_barbearia'),
            mensagem=request.POST.get('mensagem'),
        )
        messages.success(request, 'Recebemos sua mensagem! Em breve entraremos em contato.')
        return redirect('landing')

    return render(request, 'landing.html')


def acessar_barbearia(request):
    slug_digitado = request.GET.get('slug', '').strip().lower().replace(' ', '-')

    if not slug_digitado:
        messages.error(request, 'Digite o código da sua barbearia.')
        return redirect('landing')

    if not Empresa.objects.filter(slug=slug_digitado).exists():
        messages.error(request, 'Barbearia não encontrada. Confira o código.')
        return redirect('landing')

    return redirect('login', slug=slug_digitado)

def gerar_horarios():
    horarios = []
    atual = datetime.strptime(f'{HORARIO_INICIO}:00', '%H:%M')
    fim = datetime.strptime(f'{HORARIO_FIM}:00', '%H:%M')
    while atual < fim:
        horarios.append(atual.strftime('%H:%M'))
        atual += timedelta(minutes=INTERVALO_MINUTOS)
    return horarios


def index(request, slug):
    return render(request, 'index.html')


def cadastro(request, slug):
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
            # repara: cliente NÃO recebe empresa fixa, ele é "global" na plataforma
        )

        auth_login(request, user)
        return redirect('agendamentos', slug=slug)

    return render(request, 'cadastro.html')


def login_view(request, slug):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.tipo == 'gerente':
                return redirect('dashboard_gerente', slug=slug)
            elif user.tipo == 'barbeiro':
                return redirect('painel_barbeiro', slug=slug)
            else:
                return redirect('agendamentos', slug=slug)
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')


def logout_view(request, slug):
    logout(request)
    return redirect('index', slug=slug)


@somente_tipo('cliente')
def agendamentos(request, slug):
    empresa = request.empresa
    barbeiros = Usuario.objects.filter(tipo='barbeiro', empresa=empresa)

    if request.method == 'POST':
        barbeiro_id = request.POST.get('barbeiro')
        servico = request.POST.get('servico')
        data = request.POST.get('data')
        horario = request.POST.get('horario')

        if not barbeiro_id or not horario:
            messages.error(request, 'Escolha o barbeiro e o horário.')
            return redirect('agendamentos', slug=slug)

        # Garante que o barbeiro escolhido pertence mesmo a essa empresa
        barbeiro_valido = Usuario.objects.filter(id=barbeiro_id, tipo='barbeiro', empresa=empresa).exists()
        if not barbeiro_valido:
            messages.error(request, 'Barbeiro inválido.')
            return redirect('agendamentos', slug=slug)

        ja_existe = Agendamento.objects.filter(barbeiro_id=barbeiro_id, data=data, horario=horario).exists()
        if ja_existe:
            messages.error(request, 'Esse horário acabou de ser reservado. Escolha outro.')
            return redirect('agendamentos', slug=slug)

        Agendamento.objects.create(
            empresa=empresa,
            cliente=request.user,
            barbeiro_id=barbeiro_id,
            servico=servico,
            data=data,
            horario=horario,
        )
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('agendamentos', slug=slug)

    meus_agendamentos = Agendamento.objects.filter(cliente=request.user, empresa=empresa).order_by('data', 'horario')

    return render(request, 'agendamentos.html', {
        'barbeiros': barbeiros,
        'precos': Agendamento.PRECOS,
        'meus_agendamentos': meus_agendamentos,
    })


@somente_tipo('cliente')
def excluir_agendamento(request, slug, id):
    agendamento = Agendamento.objects.get(id=id, cliente=request.user, empresa=request.empresa)
    agendamento.delete()
    messages.success(request, 'Agendamento cancelado com sucesso.')
    return redirect('agendamentos', slug=slug)


def horarios_disponiveis(request, slug):
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
def painel_barbeiro(request, slug):
    meus_agendamentos = Agendamento.objects.filter(barbeiro=request.user, empresa=request.empresa).order_by('data', 'horario')
    return render(request, 'painel_barbeiro.html', {'agendamentos': meus_agendamentos})


@somente_tipo('barbeiro')
def concluir_agendamento(request, slug, id):
    agendamento = Agendamento.objects.get(id=id, barbeiro=request.user, empresa=request.empresa)
    agendamento.status = 'concluido'
    agendamento.save()
    messages.success(request, 'Atendimento marcado como concluído!')
    return redirect('painel_barbeiro', slug=slug)


@somente_tipo('gerente')
def dashboard_gerente(request, slug):
    empresa = request.empresa
    filtro_status = request.GET.get('status', 'todos')

    agendamentos = Agendamento.objects.filter(empresa=empresa).select_related('cliente', 'barbeiro').order_by('-data', '-horario')
    if filtro_status == 'pendente':
        agendamentos = agendamentos.filter(status='pendente')
    elif filtro_status == 'concluido':
        agendamentos = agendamentos.filter(status='concluido')

    total_pendentes = Agendamento.objects.filter(empresa=empresa, status='pendente').count()
    total_concluidos = Agendamento.objects.filter(empresa=empresa, status='concluido').count()
    barbeiros = Usuario.objects.filter(tipo='barbeiro', empresa=empresa)

    resumo_barbeiros = []
    for b in barbeiros:
        ags_b = Agendamento.objects.filter(barbeiro=b, empresa=empresa)
        concluidos_b = ags_b.filter(status='concluido')
        resumo_barbeiros.append({
            'nome': b.first_name or b.username,
            'pendentes': ags_b.filter(status='pendente').count(),
            'concluidos': concluidos_b.count(),
            'receita': sum(ag.preco for ag in concluidos_b),
        })

    return render(request, 'dashboard_gerente.html', {
        'agendamentos': agendamentos,
        'total_pendentes': total_pendentes,
        'total_concluidos': total_concluidos,
        'resumo_barbeiros': resumo_barbeiros,
        'filtro_status': filtro_status,
        'barbeiros': barbeiros,
    })


@somente_tipo('gerente')
def gerenciar_barbeiros(request, slug):
    empresa = request.empresa
    barbeiros = Usuario.objects.filter(tipo='barbeiro', empresa=empresa)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return redirect('gerenciar_barbeiros', slug=slug)

        Usuario.objects.create_user(username=username, password=senha, first_name=nome, tipo='barbeiro', empresa=empresa)
        messages.success(request, 'Barbeiro adicionado!')
        return redirect('gerenciar_barbeiros', slug=slug)

    return render(request, 'gerenciar_barbeiros.html', {'barbeiros': barbeiros})


@somente_tipo('gerente')
def excluir_barbeiro(request, slug, id):
    barbeiro = Usuario.objects.get(id=id, tipo='barbeiro', empresa=request.empresa)
    barbeiro.delete()
    messages.success(request, 'Barbeiro removido.')
    return redirect('gerenciar_barbeiros', slug=slug)


@somente_tipo('gerente')
def financas(request, slug):
    empresa = request.empresa
    concluidos = Agendamento.objects.filter(empresa=empresa, status='concluido').select_related('cliente', 'barbeiro').order_by('-data')
    total = concluidos.count()
    receita_total = sum(ag.preco for ag in concluidos)
    ticket_medio = receita_total / total if total > 0 else 0

    return render(request, 'financas.html', {
        'agendamentos': concluidos,
        'total_agendamentos': total,
        'receita_total': receita_total,
        'ticket_medio': ticket_medio,
    })