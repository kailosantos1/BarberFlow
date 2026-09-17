from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def somente_tipo(*tipos_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            slug = kwargs.get('slug')

            if not request.user.is_authenticated:
                return redirect('login', slug=slug)

            if request.user.tipo not in tipos_permitidos:
                messages.error(request, 'Você não tem permissão para acessar essa página.')
                return redirect('index', slug=slug)

            # Segurança de tenant: impede acessar dados de outra empresa pela URL
            if request.user.tipo in ('gerente', 'barbeiro'):
                if request.user.empresa_id != request.empresa.id:
                    messages.error(request, 'Acesso negado a essa barbearia.')
                    return redirect('index', slug=slug)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator