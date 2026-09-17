from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Agendamento


class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'tipo', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('tipo', 'telefone', 'data_nascimento', 'sexo')}),
    )

admin.site.register(Usuario, UsuarioAdmin)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'barbeiro', 'servico', 'data', 'horario')