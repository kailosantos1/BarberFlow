from django.contrib import admin
from agendamento.models import *

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('idagendamento', 'nome', 'telefone', 'servico', 'data_agendamento', 'horario')

#    list_display = ('idagendamento','data_agendamento','horario','observacao','email','valor')

