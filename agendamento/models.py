from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Agendamento(models.Model):
    SERVICO_CHOICES =[
        ('corte', 'Corte de Cabelo'),
        ('barba', 'Barba'),
        ('combo', 'Combo Completo'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_cliente')
    barbeiro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_barbeiro', limit_choices_to={'perfil__tipo': 'barbeiro'})
    servico = models.CharField(max_length=10, choices=SERVICO_CHOICES)
    data = models.DateField()
    horario = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.cliente.username} - {self.barbeiro} {self.data}'
    
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
    
class Perfil(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('barbeiro', 'Barbeiro'),
        ('gerente', 'Gerente'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='cliente')
    
    def __str__(self):
        return f"{self.usuario.username} ({self.tipo})"
     
    