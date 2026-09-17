def empresa_atual(request):
    return {'empresa': getattr(request, 'empresa', None)}