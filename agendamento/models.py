from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Agendamento(models.Model):
    SERVICO_CHOICES =[
        ('corte', 'Corte de Cabelo'),
        ('barba', 'Barba'),
        ('combo', 'Combo Completo'),
    ]
    
    idagendamento = models.BigAutoField('Identificador', primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')
    servico = models.CharField('Servico', max_length=10, choices=SERVICO_CHOICES)
    data_agendamento = models.DateField('Data do Agendamento')
    horario = models.TimeField('Horario Agendamento')
    
    def __str__(self):
        return f'{self.cliente.username} - {self.data_agendamento} {self.horario}'
    
class Cliente(models.Model):
    SEXO_CHOICES=[
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
    ]
    
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    data_nascimento = models.DateField('Data de Nascimento')
    sexo = models.CharField('Sexo', max_length=10, choices=SEXO_CHOICES )
    
    def __str__(self):
        return self.user.username
     
    