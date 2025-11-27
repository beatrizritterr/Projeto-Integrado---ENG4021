# Create your views here.
# Arquivo: core/views.py

from django.shortcuts import render
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'core/index.html') 


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
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'core/cadastro.html', context)