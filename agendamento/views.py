from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def servicos(request):
    return render(request, 'servicos.html')