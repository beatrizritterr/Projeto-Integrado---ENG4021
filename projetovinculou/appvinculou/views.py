from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm 

def calendario_page(request):
    return render(request, 'index.html', {})

def login_usuario(request):
    return render(request, 'login.html', {})

def perfil_usuario(request):
    return render(request, 'perfil.html', {})

def avaliar_prof(request):
    return render(request, 'avaliacaooprof.html', {})

def listar_avaliacoes_professores(request):
    return render(request, 'avaliacoesprof.html', {})

def comunidades(request):
    return render(request, 'comunidades.html', {})

def configuracoes(request):
    return render(request, 'configuracoes.html', {})

def filtro_busca(request):
    return render(request, 'filtrobusca.html', {})

def filtro_post(request):
    return render(request, 'filtropost.html', {})

def provas_antigas(request):
    return render(request, 'provasantigas.html', {})


def cadastro_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST) 
        
        if form.is_valid():
            
            dados = form.cleaned_data 
            return redirect('pagina_inicial') 
        
    else:
        form = CadastroUsuarioForm()

    context = {
        'form': form,
        'titulo': 'Página de Cadastro'
    }
    
    return render(request, 'cadastro.html', context)