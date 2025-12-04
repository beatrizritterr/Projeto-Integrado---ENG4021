
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
import calendar
from datetime import datetime, date, timedelta 

from .forms import (
    CustomUserCreationForm, 
    AvaliacaoForm, 
    EventoForm, 
    PostagemForm,
    ComentarioForm

)

from .models import (
    Avaliacao, 
    Disciplina, 
    Evento, 
    Postagem, 
    Comunidade,
    ProvaAntiga
)
User = get_user_model()


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

def password_reset_dev(request):
    user_id = 1 
    user = get_object_or_404(User, pk=user_id) 
    uid = 'MQ' 
    token = 'set-password' 
    reset_url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    return redirect(reset_url)



@login_required 
def configuracoes(request):
    context = {'usuario': request.user}
    return render(request, 'core/configuracoes.html', context)

def filtrobusca(request):
    context = {'usuario': request.user} 
    return render(request, 'core/filtrobusca.html', context)

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

    avaliacoes = Avaliacao.objects.all().order_by('-data_criacao')
    
    context = {
        'form': form,
        'avaliacoes': avaliacoes, 
        'usuario': request.user
    }
    return render(request, 'core/avaliacaoprof.html', context)


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
        eventos_por_dia.setdefault(day, []).append(evento)

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
    
    messages.info(request, f"Função de edição para o evento: {evento.titulo}.")
    return redirect('home')

@login_required
def excluir_evento(request, event_id):
    evento = get_object_or_404(Evento, pk=event_id, usuario=request.user)
    
    if request.method == 'POST':
        evento.delete()
        messages.warning(request, f"Evento '{evento.titulo}' excluído.")
    
    return redirect('home')




def provasantigas(request):
    disciplinas = Disciplina.objects.all().order_by('nome')
    
    provas_antigas = ProvaAntiga.objects.all().select_related('disciplina').prefetch_related('arquivo_set').order_by('-periodo_semestral', 'disciplina__nome')
    
    context = {
        'disciplinas': disciplinas,
        'provas_antigas': provas_antigas,
        'usuario': request.user
    }
    return render(request, 'core/provasantigas.html', context)

def comunidades(request):
    """Carrega todas as comunidades para exibição na grade."""
    lista_comunidades = Comunidade.objects.all().order_by('-membros_count')
    
    context = {
        'lista_comunidades': lista_comunidades,
        'usuario': request.user
    }
    return render(request, 'core/comunidades.html', context)

@login_required 
def filtropost(request):
    if request.method == 'POST':
        form_postagem = PostagemForm(request.POST)
        if form_postagem.is_valid():
            postagem = form_postagem.save(commit=False)
            postagem.autor = request.user
            postagem.save()
            messages.success(request, "Postagem publicada com sucesso!")
            return redirect('filtropost') 
        else:
            form_postagem = form_postagem 
    else:
        form_postagem = PostagemForm() 

    tipo_selecionado = request.GET.get('tipo', 'todos') 
    postagens_qs = Postagem.objects.all()

    if tipo_selecionado != 'todos':
        mapeamento = {'noticias': 'NOT', 'eventos': 'EVT', 'oportunidades': 'OPR', 'discussao': 'DSC'}
        codigo_tipo = mapeamento.get(tipo_selecionado)
        if codigo_tipo:
            postagens_qs = postagens_qs.filter(tipo=codigo_tipo)

    postagens = postagens_qs.order_by('-data_publicacao').select_related('autor')
    comunidades = Comunidade.objects.all()[:5]

    context = {
        'postagens': postagens,
        'comunidades': comunidades,
        'tipo_selecionado': tipo_selecionado, 
        'form_postagem': form_postagem, 
        'usuario': request.user
    }
    return render(request, 'core/filtropost.html', context)

@login_required
def curtir_postagem(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    user = request.user
    
    if user in postagem.curtidas.all():
        postagem.curtidas.remove(user)
    else:
        postagem.curtidas.add(user)
        
    return redirect(request.META.get('HTTP_REFERER', 'filtropost')) 

@login_required
def salvar_postagem(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    user = request.user
    
    if user in postagem.salvamentos.all():
        postagem.salvamentos.remove(user)
    else:
        postagem.salvamentos.add(user)
        
    return redirect(request.META.get('HTTP_REFERER', 'filtropost')) 

@login_required
def adicionar_comentario(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST) 
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.postagem = postagem
            comentario.autor = request.user
            comentario.save()
            messages.success(request, "Comentário adicionado com sucesso!")
        else:
            messages.error(request, "Erro ao processar o comentário.")
    
    return redirect(request.META.get('HTTP_REFERER', 'filtropost'))