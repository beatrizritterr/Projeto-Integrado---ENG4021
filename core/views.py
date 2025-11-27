# Create your views here.
# Arquivo: core/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html') 

def login(request):
    return render(request, 'core/login.html') 

def perfil(request):
    return render(request, 'core/perfil.html')

def avaliacaoprof(request):
    return render(request, 'core/avaliacaoprof.html')

def configuracoes(request):
    return render(request, 'core/configuracoes.html')

def comunidades(request):
    return render(request, 'core/comunidades.html')

def filtrobusca(request):
    return render(request, 'core/filtrobusca.html')

def filtropost(request):
    return render(request, 'core/filtropost.html')

def provasantigas(request):
    return render(request, 'core/provasantigas.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')