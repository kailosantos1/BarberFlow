from django.contrib import admin

from agendamento.models import *

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('idagendamento','data_agendamento','horario','observacao','email','valor')

