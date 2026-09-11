from django.contrib import admin
from agendamento.models import *

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('idagendamento', 'cliente', 'servico', 'data_agendamento', 'horario')

#    list_display = ('idagendamento','data_agendamento','horario','observacao','email','valor')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'data_nascimento', 'sexo')