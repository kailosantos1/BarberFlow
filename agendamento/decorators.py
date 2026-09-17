from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def somente_tipo(*tipos_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.tipo not in tipos_permitidos:
                messages.error(request, 'Você não tem permissão para acessar essa página.')
                return redirect('index')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator