"""
URL configuration for barbearia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from agendamento import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('agendamentos/', views.agendamentos, name='agendamentos'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Horários disponíveis (usado via JavaScript no formulário de agendamento)
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),

    # Barbeiro
    path('painel-barbeiro/', views.painel_barbeiro, name='painel_barbeiro'),

    # Gerente
    path('dashboard/', views.dashboard_gerente, name='dashboard_gerente'),
    path('dashboard/barbeiros/', views.gerenciar_barbeiros, name='gerenciar_barbeiros'),
    path('dashboard/barbeiros/excluir/<int:id>/', views.excluir_barbeiro, name='excluir_barbeiro'),
    path('dashboard/financas/', views.financas, name='financas'),
]