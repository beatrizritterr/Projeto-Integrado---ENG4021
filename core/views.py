from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, AvaliacaoForm, EventoForm # Importado EventoForm
from .models import Disciplina, ProvaAntiga
from django.contrib.auth.decorators import login_required
from .models import Avaliacao 
from .models import Evento
import calendar
from datetime import datetime, date, timedelta # IMPORT OBRIGATÓRIO: Adicionei timedelta
from django.contrib import messages

User = get_user_model() 

# ----------------------------------------------------
# VIEWS DE CALENDÁRIO (HOME) E CRUD DE EVENTOS
# A função 'home' agora está completa e carrega o formulário.
# ----------------------------------------------------

@login_required 
def home(request):
    # 1. Obter Mês e Ano (usa o mês/ano atual por padrão)
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    cal_date = date(year, month, 1)
    
    # 2. Navegação (Próximo/Anterior)
    # Lógica que usa timedelta
    try:
        prev_month = cal_date.replace(day=1) - timedelta(days=1)
        next_month = cal_date.replace(day=28) + timedelta(days=4)
        
        prev_url = f"?year={prev_month.year}&month={prev_month.month}"
        next_url = f"?year={next_month.year}&month={next_month.month}"
    except ValueError:
        prev_url = '#'
        next_url = '#'
    
    # 3. Buscar Eventos do Usuário para o Mês
    start_of_month = datetime(year, month, 1)
    
    if month == 12:
        next_month_dt = datetime(year + 1, 1, 1)
    else:
        next_month_dt = datetime(year, month + 1, 1)

    eventos_mes = Evento.objects.filter(
        usuario=request.user, 
        data_hora__gte=start_of_month,
        data_hora__lt=next_month_dt 
    ).order_by('data_hora') 

    # 4. Mapear Eventos por dia (para fácil acesso no template)
    eventos_por_dia = {}
    for evento in eventos_mes:
        day = evento.data_hora.day
        if day not in eventos_por_dia:
            eventos_por_dia[day] = []
        eventos_por_dia[day].append(evento)

    # 5. Gerar o grid do calendário
    cal = calendar.Calendar(firstweekday=6) # 6 = Domingo
    month_weeks = cal.monthdays2calendar(year, month) # Lista de semanas
    
    # 6. Adicionar o Formulário (para o Modal)
    evento_form = EventoForm() 

    context = {
        'mes_ano': cal_date.strftime("%B %Y").capitalize(), # Título
        'month_weeks': month_weeks, # O grid do calendário (dias)
        'eventos_por_dia': eventos_por_dia, # Eventos mapeados
        'hoje': date.today().day,
        'mes_atual': date.today().month,
        'ano_atual': date.today().year,
        'mes_sendo_renderizado': month,
        'prev_url': prev_url,
        'next_url': next_url,
        'usuario': request.user, 
        'evento_form': evento_form, # Passa o formulário para o modal no index.html
    }
    return render(request, 'core/index.html', context)


# ----------------------------------------------------
# VIEWS SECUNDÁRIAS E CRUD DE EVENTOS (Mantidas Abaixo)
# ----------------------------------------------------

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

def configuracoes(request):
    return render(request, 'core/configuracoes.html')

def comunidades(request):
    return render(request, 'core/comunidades.html')

def filtrobusca(request):
    return render(request, 'core/filtrobusca.html')

def filtropost(request):
    return render(request, 'core/filtropost.html')

def provasantigas(request):
    disciplinas = Disciplina.objects.all().order_by('nome')
    
    provas_antigas = ProvaAntiga.objects.all().select_related('disciplina').prefetch_related('arquivo_set').order_by('-periodo_semestral', 'disciplina__nome')
    
    context = {
        'disciplinas': disciplinas,
        'provas_antigas': provas_antigas
    }
    return render(request, 'core/provasantigas.html', context)


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

# 1. Adicionar Evento (Create)
@login_required
def adicionar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST) 
        if form.is_valid():
            evento = form.save(commit=False) 
            evento.usuario = request.user 
            evento.save() 
            messages.success(request, "Evento adicionado com sucesso!")
        else:
            messages.error(request, "Erro ao adicionar evento. Verifique os campos.")
            
    return redirect('home') 

# 2. Editar Evento (Update)
@login_required
def editar_evento(request, event_id):
    evento = get_object_or_404(Evento, pk=event_id, usuario=request.user)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Evento atualizado com sucesso!")
        else:
            messages.error(request, "Erro ao editar evento. Verifique os campos.")
            
    return redirect('home')

# 3. Excluir Evento (Delete)
@login_required
def excluir_evento(request, event_id):
    
    evento = get_object_or_404(Evento, pk=event_id, usuario=request.user)
    
    if request.method == 'POST':
        evento.delete()
        messages.warning(request, f"Evento '{evento.titulo}' excluído.")
    
    return redirect('home')