from django.db import models

# Create your models here.

class Agendamento(models.Model):
    SERVICO_CHOICES =[
        ('corte', 'Corte de Cabelo'),
        ('barba', 'Barba'),
        ('combo', 'Combo Completo'),
    ]
    
    idagendamento = models.BigAutoField('Identificador', primary_key=True)
    nome = models.CharField('Nome', max_length=150)
    telefone = models.CharField('Telefone', max_length=20)
    servico = models.CharField('Servico', max_length=10, choices=SERVICO_CHOICES)
    data_agendamento = models.DateField('Data do Agendamento')
    horario = models.TimeField('Horario Agendamento')
    def __str__(self):
        return f'{self.nome} - {self.data_agendamento} {self.horario}'
    
class Clientes(models.Model):
    idcliente = models.CharField('Nome
    nome =
    data_nascimento = 
    email = 
    sexo =
    senha = 
    telefone =
     
    