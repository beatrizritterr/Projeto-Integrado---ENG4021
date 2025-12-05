from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, AvaliacaoForm, EventoForm, ProvaAntigaForm
from .models import Disciplina, ProvaAntiga
from django.contrib.auth.decorators import login_required
from .models import Avaliacao, ProvaAntiga
from .models import Evento
import calendar
from datetime import datetime, date, timedelta 
from django.contrib import messages
from .models import Comunidade 
from .models import Postagem, Comunidade, Perfil, Avaliacao
from .forms import UserUpdateForm, PerfilUpdateForm
from django.db.models import Q


User = get_user_model() 



@login_required 
def home(request):
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    cal_date = date(year, month, 1)

    try:
        prev_month = cal_date.replace(day=1) - timedelta(days=1)
        next_month = cal_date.replace(day=28) + timedelta(days=4)
        
        prev_url = f"?year={prev_month.year}&month={prev_month.month}"
        next_url = f"?year={next_month.year}&month={next_month.month}"
    except ValueError:
        prev_url = '#'
        next_url = '#'
    
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

    eventos_por_dia = {}
    for evento in eventos_mes:
        day = evento.data_hora.day
        if day not in eventos_por_dia:
            eventos_por_dia[day] = []
        eventos_por_dia[day].append(evento)

    cal = calendar.Calendar(firstweekday=6) 
    month_weeks = cal.monthdays2calendar(year, month) 
    
    evento_form = EventoForm() 

    context = {
        'mes_ano': cal_date.strftime("%B %Y").capitalize(),
        'month_weeks': month_weeks,
        'eventos_por_dia': eventos_por_dia, 
        'hoje': date.today().day,
        'mes_atual': date.today().month,
        'ano_atual': date.today().year,
        'mes_sendo_renderizado': month,
        'prev_url': prev_url,
        'next_url': next_url,
        'usuario': request.user, 
        'evento_form': evento_form, 
    }
    return render(request, 'core/index.html', context)



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
        
    context = {
        'form': form,
        'usuario': request.user 
    }
    return render(request, 'core/cadastro.html', context)

def password_reset_dev(request):
    user_id = 1 
    user = get_object_or_404(User, pk=user_id) 

    uid = 'MQ' 
    token = 'set-password' 


    reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    
    return redirect(reset_url)

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

@login_required
def excluir_evento(request, event_id):
    
    evento = get_object_or_404(Evento, pk=event_id, usuario=request.user)
    
    if request.method == 'POST':
        evento.delete()
        messages.warning(request, f"Evento '{evento.titulo}' excluído.")
    
    return redirect('home')

def comunidades(request):
    lista_comunidades = Comunidade.objects.all().order_by('-membros_count')
    
    context = {
        'lista_comunidades': lista_comunidades,
        'usuario': request.user 
    }
    return render(request, 'core/comunidades.html', context)

def filtrobusca(request):
    context = {'usuario': request.user} 
    return render(request, 'core/filtrobusca.html', context)

def filtropost(request): 
    postagens = Postagem.objects.all().order_by('-data_publicacao').select_related('autor') 

    comunidades = Comunidade.objects.all()[:5]
    
    context = {
        'postagens': postagens,
        'comunidades': comunidades,
        'usuario': request.user
    }
    return render(request, 'core/filtropost.html', context) 


@login_required 
def provasantigas(request):
    if request.method == 'POST':
        form = ProvaAntigaForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('provasantigas')
    else:
        form = ProvaAntigaForm()

    disciplina_id = request.GET.get('disciplina')
    if disciplina_id:
        provas = ProvaAntiga.objects.filter(disciplina_id=disciplina_id).order_by('-periodo')
    else:
        provas = ProvaAntiga.objects.all().order_by('-periodo')

    context = {
        'form': form,
        'provas': provas,
        'disciplinas': ProvaAntiga.objects.values_list('disciplina__id', 'disciplina__nome', 'disciplina__codigo').distinct()
    }
    return render(request, 'core/provasantigas.html', context)



@login_required
def perfil(request):
    perfil_usuario, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, instance=perfil_usuario)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('perfil') 

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=perfil_usuario)

    atividades = Avaliacao.objects.filter(usuario=request.user).order_by('-data_criacao')[:5]

    context = {
        'usuario': request.user,
        'u_form': u_form,
        'p_form': p_form,
        'atividades': atividades,
        'info_extra': perfil_usuario 
    }

    return render(request, 'core/perfil.html', context)


def buscar_perfis(request):
    query = request.GET.get('q') 
    perfis = Perfil.objects.exclude(user=request.user).select_related('user')
    
    if query:
        perfis = perfis.filter(
            Q(bio__icontains=query) | 
            Q(curso__icontains=query) | 
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query)
        ).distinct()

    context = {
        'lista_perfis': perfis,
        'termo_busca': query 
    }
    return render(request, 'core/busca_perfis.html', context)