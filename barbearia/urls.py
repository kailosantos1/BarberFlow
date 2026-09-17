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

    path('<slug:slug>/', views.index, name='index'),
    path('<slug:slug>/login/', views.login_view, name='login'),
    path('<slug:slug>/cadastro/', views.cadastro, name='cadastro'),
    path('<slug:slug>/logout/', views.logout_view, name='logout'),

    path('<slug:slug>/agendamentos/', views.agendamentos, name='agendamentos'),
    path('<slug:slug>/agendamentos/excluir/<int:id>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('<slug:slug>/horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),

    path('<slug:slug>/painel-barbeiro/', views.painel_barbeiro, name='painel_barbeiro'),
    path('<slug:slug>/painel-barbeiro/concluir/<int:id>/', views.concluir_agendamento, name='concluir_agendamento'),

    path('<slug:slug>/dashboard/', views.dashboard_gerente, name='dashboard_gerente'),
    path('<slug:slug>/dashboard/barbeiros/', views.gerenciar_barbeiros, name='gerenciar_barbeiros'),
    path('<slug:slug>/dashboard/barbeiros/excluir/<int:id>/', views.excluir_barbeiro, name='excluir_barbeiro'),
    path('<slug:slug>/dashboard/financas/', views.financas, name='financas'),
]