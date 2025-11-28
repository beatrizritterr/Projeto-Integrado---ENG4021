
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, AvaliacaoForm
from django.contrib.auth.decorators import login_required
from .models import Professor, Disciplina, Curso
from django.db.models import Prefetch

User = get_user_model() 


def home(request):
    if request.user.is_authenticated:
        status_login = f"Bem-vindo(a), {request.user.username}!"
    else:
        status_login = "Você não está logado(a)."
        
    context = {'status_login': status_login}
    return render(request, 'core/index.html', context)


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


def password_reset_dev(request):
    user_id = 1 
    user = get_object_or_404(User, pk=user_id) 

    uid = 'MQ' 
    token = 'set-password' 


    reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    
    return redirect(reset_url)

@login_required
def avaliacaoprof(request):
    """
    View para exibir a lista de professores/disciplinas para avaliação
    E TAMBÉM processar o formulário de nova avaliação.
    """

    # --- PARTE 1: Lógica para SALVAR uma nova avaliação (Método POST) ---
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user 
            avaliacao.save()
            
            # Opcional: Adicionar uma mensagem de sucesso aqui (usando django.contrib.messages)
            
            # Redireciona para a mesma página para limpar o formulário e mostrar os dados atualizados
            return redirect('avaliacaoprof')
            
    # --- PARTE 2: Lógica para exibir a página (Método GET ou se o formulário for inválido) ---
    else:
        # Se for GET, cria um formulário em branco
        form = AvaliacaoForm()

    # --- PARTE 3: Buscar os dados do banco de dados para exibir na tela ---
    # Isso roda tanto no GET quanto se o POST falhar na validação, 
    # garantindo que a lista de professores sempre apareça.

    # Busca os cursos, pré-carregando disciplinas e seus professores para otimizar
    cursos_data = Curso.objects.prefetch_related(
        Prefetch('disciplinas', queryset=Disciplina.objects.prefetch_related('professores'))
    ).all().order_by('nome')

    # Busca todos os professores para a lista de referência no final da página
    todos_professores_data = Professor.objects.all().order_by('nome')

    # --- PARTE 4: Montar o contexto e renderizar ---
    context = {
        'form': form,                         # O formulário (em branco ou com erros de validação)
        'cursos': cursos_data,                # Os dados scrapeados dos cursos
        'todos_professores': todos_professores_data, # Lista geral de professores
    }

    return render(request, 'core/avaliacaoprof.html', context)