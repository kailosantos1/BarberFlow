from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


class Empresa(models.Model):
    PLANO_CHOICES = [
        ('teste', 'Teste Grátis'),
        ('basico', 'Básico'),
        ('premium', 'Premium'),
    ]

    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=60, unique=True, help_text='Usado na URL. Ex: joao-barbearia')
    plano = models.CharField(max_length=10, choices=PLANO_CHOICES, default='teste')
    ativo = models.BooleanField(default=True, help_text='Desative pra bloquear o acesso imediatamente.')
    licenca_validade = models.DateField(help_text='Data até quando a licença é válida.')
    criada_em = models.DateTimeField(auto_now_add=True)

    def licenca_valida(self):
        return self.ativo and self.licenca_validade >= timezone.localdate()

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('barbeiro', 'Barbeiro'),
        ('gerente', 'Gerente'),
    ]

    SEXO_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='cliente')
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    sexo = models.CharField('Sexo', max_length=10, choices=SEXO_CHOICES, blank=True)

    # Só barbeiro e gerente pertencem a uma empresa. Cliente fica sem empresa fixa
    # (o vínculo dele com uma empresa acontece através do Agendamento).
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios')

    def __str__(self):
        return f"{self.username} ({self.tipo})"

class Lead(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    nome_barbearia = models.CharField(max_length=100, blank=True)
    mensagem = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.email}'

class Agendamento(models.Model):
    SERVICO_CHOICES = [
        ('corte', 'Corte de Cabelo'),
        ('barba', 'Barba'),
        ('combo', 'Combo Completo'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
    ]

    PRECOS = {
        'corte': 35.00,
        'barba': 25.00,
        'combo': 55.00,
    }

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='agendamentos')
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_cliente')
    barbeiro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_barbeiro', limit_choices_to={'tipo': 'barbeiro'})
    servico = models.CharField(max_length=10, choices=SERVICO_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data = models.DateField()
    horario = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('barbeiro', 'data', 'horario')

    @property
    def preco(self):
        return self.PRECOS.get(self.servico, 0)

    def __str__(self):
        return f'{self.cliente.username} - {self.barbeiro} {self.data}'