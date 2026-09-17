from django.shortcuts import render, redirect
from django.urls import resolve
from .models import Empresa


class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolved = resolve(request.path_info)
        slug = resolved.kwargs.get('slug')

        request.empresa = None

        if slug:
            try:
                empresa = Empresa.objects.get(slug=slug)
            except Empresa.DoesNotExist:
                return render(request, 'empresa_nao_encontrada.html', status=404)

            if not empresa.licenca_valida():
                return render(request, 'licenca_expirada.html', {'empresa': empresa}, status=403)

            request.empresa = empresa

        return self.get_response(request)