from django.db import models

# Create your models here.

class Agendamento(models.Model):
    idagendamento = models.BigIntegerField('Identificador', primary_key=True, unique=True, blank=False)
    data_agendamento = models.DateField('Data do Agendamento')
    horario = models.TimeField('Horario Agendamento')
    observacao = models.CharField('Observacao', max_length=200)
    email = models.EmailField('Email', max_length=150, unique=True)
    valor = models.DecimalField('Valor', max_digits=5, decimal_places=2, blank=False)
    
    
    
    def __str__(self):
        return f'{self.email}'