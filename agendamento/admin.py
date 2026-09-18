from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Agendamento, Empresa, Lead


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'plano', 'ativo', 'licenca_validade')
    list_filter = ('plano', 'ativo')
    prepopulated_fields = {'slug': ('nome',)}


class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'tipo', 'empresa', 'email')
    list_filter = ('tipo', 'empresa')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('tipo', 'empresa', 'telefone', 'data_nascimento', 'sexo')}),
    )

admin.site.register(Usuario, UsuarioAdmin)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa', 'cliente', 'barbeiro', 'servico', 'status', 'data', 'horario')
    list_filter = ('empresa', 'status', 'servico')
        
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'nome_barbearia', 'criado_em')
    list_filter = ('criado_em',)