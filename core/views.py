
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, AvaliacaoForm, EventoForm, ContaPessoalForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .models import Disciplina, ProvaAntiga
from django.contrib.auth.decorators import login_required
from .models import Avaliacao 
from .models import Evento
import calendar
from datetime import datetime, date

User = get_user_model()



@login_required 
def home(request):
    today = date.today()    
    eventos_por_dia = {} 
    month_days = []      

    if request.user.is_authenticated:
        status_login = f"Bem-vindo(a), {request.user.username}!"
    else:
        status_login = "Você não está logado(a)."
    
    context = {
        'hoje': today.day,
        'mes_ano': today.strftime("%B %Y"), 
        'month_days': month_days,           
        'eventos_por_dia': eventos_por_dia, 
        'status_login': status_login,
        
        'usuario': request.user, 
    }
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

def avaliacaoprof(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            
            avaliacao.usuario = request.user 
            
            avaliacao.save()
            
            return redirect('avaliacaoprof')
    else:
        form = AvaliacaoForm()

    context = {'form': form}
    return render(request, 'core/avaliacaoprof.html', context)

@login_required 
def avaliacaoprof(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            
            avaliacao.usuario = request.user 
            
            avaliacao.save()
            
            return redirect('avaliacaoprof')
    else:
        form = AvaliacaoForm()

    context = {'form': form}
    return render(request, 'core/avaliacaoprof.html', context)

def provasantigas(request):
    disciplinas = Disciplina.objects.all().order_by('nome')
    
    provas_antigas = ProvaAntiga.objects.all().select_related('disciplina').prefetch_related('arquivo_set').order_by('-periodo_semestral', 'disciplina__nome')
    
    context = {
        'disciplinas': disciplinas,
        'provas_antigas': provas_antigas
    }
    return render(request, 'core/provasantigas.html', context)

@login_required 
def perfil(request):
    usuario_logado = request.user 
    
    atividades = Avaliacao.objects.filter(usuario=usuario_logado).order_by('-data_criacao')[:5] 

    info_extra = {
        'curso': 'Engenharia de Computação', 
        'periodo': '5º',
        'bio': 'Apaixonado por tecnologia e inovação...'
    }

    context = {
        'usuario': usuario_logado,
        'atividades': atividades, 
        'info_extra': info_extra,
    }
    return render(request, 'core/perfil.html', context)

@login_required
def adicionar_evento(request):
    if request.method == 'POST':
        # Tenta popular o formulário com dados POST
        form = EventoForm(request.POST) 
        
        if form.is_valid():
            # Não salva no BD ainda
            evento = form.save(commit=False) 
            
            # Atribui o usuário logado
            evento.usuario = request.user 
            
            # Salva no BD
            evento.save() 
            
            # Redireciona de volta para o calendário (home)
            return redirect('home')
    else:
        # Se for GET, cria um formulário vazio
        form = EventoForm()
        
    context = {'form': form}
    # Renderiza o formulário em um novo template simples
    return render(request, 'core/adicionar_evento.html', context)

#/avaliar-disciplina/
@login_required
def avaliar_disciplina(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()
            return redirect('avaliacao_sucesso')
    else:
        form = AvaliacaoForm()
    
    context = {'form': form}
    return render(request, 'core/avaliar_disciplina.html', context)
def avaliacao_sucesso(request):
    return render(request, 'core/avaliacao_sucesso.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Avaliacao
from .forms import AvaliacaoForm

@login_required
def editar_avaliacao(request, pk):
    # Garante que só o dono pode editar
    avaliacao = get_object_or_404(Avaliacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            form.save()  # já salva a edição
            return redirect('avaliacaoprof')  # volta pra tela de avaliações
    else:
        form = AvaliacaoForm(instance=avaliacao)

    context = {
        'form': form,
        'avaliacao': avaliacao,
    }
    return render(request, 'core/editar_avaliacao.html', context)


@login_required
def excluir_avaliacao(request, pk):
    # Garante que só o dono pode excluir
    avaliacao = get_object_or_404(Avaliacao, pk=pk, usuario=request.user)

    if request.method == 'POST':
        avaliacao.delete()
        return redirect('avaliacaoprof')

    context = {
        'avaliacao': avaliacao,
    }
    return render(request, 'core/excluir_avaliacao.html', context)

@login_required
def editar_conta(request):
    usuario = request.user  # usuário logado

    if request.method == 'POST':
        form = ContaPessoalForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # depois de salvar, volta pro perfil
    else:
        form = ContaPessoalForm(instance=usuario)

    context = {
        'form': form,
        'usuario': usuario,
    }
    return render(request, 'core/editar_conta.html', context)
