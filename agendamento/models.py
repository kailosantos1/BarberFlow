from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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

    def __str__(self):
        return f"{self.username} ({self.tipo})"


class Agendamento(models.Model):
    SERVICO_CHOICES = [
        ('corte', 'Corte de Cabelo'),
        ('barba', 'Barba'),
        ('combo', 'Combo Completo'),
    ]

    PRECOS = {
        'corte': 35.00,
        'barba': 25.00,
        'combo': 55.00,
    }

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_cliente')
    barbeiro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_barbeiro', limit_choices_to={'tipo': 'barbeiro'})
    servico = models.CharField(max_length=10, choices=SERVICO_CHOICES)
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