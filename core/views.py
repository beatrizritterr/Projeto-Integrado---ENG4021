# ARQUIVO: core/views.py - CÓDIGO CONSOLIDADO E CORRIGIDO

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
    ComentarioForm,
    ProfileUpdateForm,
    ComunidadeForm,
    MensagemForm
)

from .models import (
    Avaliacao, 
    Disciplina, 
    Evento, 
    Postagem, 
    Comunidade,
    ProvaAntiga,
    Comentario,
    Departamento,
    Professor,
    UserProfile,
    MensagemComunidade
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
   
    profile_instance, created = UserProfile.objects.get_or_create(user=usuario_logado)
    
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Sua foto de perfil foi atualizada!')
            return redirect('perfil') 
        else:
            messages.error(request, 'Erro ao atualizar a foto. Verifique o arquivo.')
    else:
        p_form = ProfileUpdateForm(instance=profile_instance)

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
        'profile_form': p_form,      
        'profile_data': profile_instance,
    }
    return render(request, 'core/perfil.html', context)


def password_reset_dev(request):
    """
    View de desenvolvimento que simula o fluxo de reset de senha para testes.
    OBS: NÃO USAR EM PRODUÇÃO.
    """
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

@login_required 
def avaliacaoprof(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user 
            avaliacao.save()
            messages.success(request, "Avaliação enviada com sucesso!")
            return redirect('avaliacaoprof')
        else:
            messages.error(request, "Erro ao enviar avaliação. Verifique os campos.")
    else:
        form = AvaliacaoForm()

    avaliacoes = Avaliacao.objects.all().order_by('-data_criacao')[:5]
    
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



def filtrobusca(request):
    context = {'usuario': request.user} 
    return render(request, 'core/filtrobusca.html', context)

@login_required 
def comunidades(request):
    form_comunidade = ComunidadeForm() 
    
    if request.method == 'POST':
        if 'criar_comunidade_btn' in request.POST:
            form_comunidade = ComunidadeForm(request.POST, request.FILES)
            
            if form_comunidade.is_valid():
                comunidade = form_comunidade.save(commit=False)
                comunidade.membros_count = 1 
                comunidade.save()
                comunidade.membros.add(request.user) 
                messages.success(request, f"Comunidade '{comunidade.nome}' criada com sucesso!")
                return redirect('comunidades')
            else:
                messages.error(request, "Erro ao criar comunidade. Verifique os campos.")
        
        elif 'inscrever_comunidade_pk' in request.POST:
            pk = request.POST.get('inscrever_comunidade_pk')
            comunidade = get_object_or_404(Comunidade, pk=pk)
            return inscrever_comunidade(request, pk) 

    lista_comunidades = Comunidade.objects.all().order_by('-membros_count')
    
    for comunidade in lista_comunidades:
        comunidade.is_member = comunidade.membros.filter(pk=request.user.pk).exists()

    context = {
        'lista_comunidades': lista_comunidades,
        'usuario': request.user,
        'form_comunidade': form_comunidade 
    }
    return render(request, 'core/comunidades.html', context)

def provasantigas(request):
    disciplinas = Disciplina.objects.all().order_by('nome')
    
    provas_antigas = ProvaAntiga.objects.all().select_related('disciplina').prefetch_related('arquivo_set').order_by('-periodo_semestral', 'disciplina__nome')
    
    context = {
        'disciplinas': disciplinas,
        'provas_antigas': provas_antigas,
        'usuario': request.user
    }
    return render(request, 'core/provasantigas.html', context)



@login_required 
def filtropost(request):
    if request.method == 'POST':
        form_postagem = PostagemForm(request.POST, request.FILES) 
        
        if form_postagem.is_valid():
            postagem = form_postagem.save(commit=False)
            postagem.autor = request.user
            postagem.save()
            messages.success(request, "Postagem publicada com sucesso!")
            return redirect('filtropost') 
    else:
        form_postagem = PostagemForm() 

    tipo_selecionado = request.GET.get('tipo', 'todos') 
    postagens_qs = Postagem.objects.all()

    if tipo_selecionado != 'todos':
        mapeamento = {'noticias': 'NOT', 'eventos': 'EVT', 'oportunidades': 'OPR', 'discussao': 'DSC'}
        codigo_tipo = mapeamento.get(tipo_selecionado)
        if codigo_tipo:
            postagens_qs = postagens_qs.filter(tipo=codigo_tipo)

    postagens = postagens_qs.order_by('-data_publicacao').select_related('autor').prefetch_related('comentarios')
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
        messages.info(request, "Curtida removida.")
    else:
        postagem.curtidas.add(user)
        messages.success(request, "Postagem curtida!")
        
    return redirect(request.META.get('HTTP_REFERER', 'filtropost')) 

@login_required
def salvar_postagem(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)
    user = request.user
    
    if user in postagem.salvamentos.all():
        postagem.salvamentos.remove(user)
        messages.info(request, "Postagem removida dos salvos.")
    else:
        postagem.salvamentos.add(user)
        messages.success(request, "Postagem salva com sucesso!")
        
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
            
            postagem.comentarios_count = postagem.comentarios.count() 
            postagem.save()
            
            messages.success(request, "Comentário adicionado com sucesso!")
        else:
            messages.error(request, "Erro ao processar o comentário.")
    
    return redirect(request.META.get('HTTP_REFERER', 'filtropost'))


@login_required
def editar_perfil(request):
    """
    Lida com a submissão do formulário de foto de perfil
    e atualiza o Model UserProfile associado ao usuário logado.
    """
    usuario_logado = request.user
    
    profile_instance, created = UserProfile.objects.get_or_create(user=usuario_logado)
    
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, 
                                   instance=profile_instance)
        
        if p_form.is_valid():
            p_form.save() 
            messages.success(request, 'Sua foto de perfil foi atualizada!')
            return redirect('perfil') 
        else:
            messages.error(request, 'Erro ao atualizar a foto. Verifique o arquivo.')
    else:
        p_form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'usuario': usuario_logado,
        'profile_form': p_form, 
    }
    return render(request, 'core/editar_perfil.html', context)

@login_required
def deletar_foto_perfil(request):
    """Deleta a foto de perfil do usuário e reverte para a padrão."""
    
    if request.method == 'POST':
        profile = request.user.userprofile 
        
        if profile.foto_perfil and profile.foto_perfil.name != 'perfil_padrao.png':
            
            profile.foto_perfil.delete(save=False) 
            
            profile.foto_perfil = 'perfil_padrao.png' 
            profile.save()
            messages.success(request, "Foto de perfil excluída com sucesso!")
        
    return redirect('perfil')

@login_required
def criar_comunidade(request):
    if request.method == 'POST':
        form = ComunidadeForm(request.POST, request.FILES)
        
        if form.is_valid():
            comunidade = form.save()
            comunidade.membros.add(request.user)
            messages.success(request, f"Comunidade '{comunidade.nome}' criada com sucesso!")
            return redirect('comunidades')
        else:
            messages.error(request, "Erro ao criar comunidade. Verifique os campos.")
    else:
        form = ComunidadeForm()
        
    context = {'form': form, 'usuario': request.user}
    return render(request, 'core/criar_comunidade.html', context)

@login_required
def inscrever_comunidade(request, pk):
    comunidade = get_object_or_404(Comunidade, pk=pk)
    
    if request.method == 'POST':
        user = request.user
        
        if user not in comunidade.membros.all():
            comunidade.membros.add(user)
            comunidade.membros_count = comunidade.membros.count() 
            comunidade.save()
            messages.success(request, f"Você se inscreveu em '{comunidade.nome}'.")
        else:
            comunidade.membros.remove(user)
            comunidade.membros_count = comunidade.membros.count()
            comunidade.save()
            messages.warning(request, f"Você saiu de '{comunidade.nome}'.")
            
    return redirect('comunidades')


@login_required
def chat_comunidade(request, pk):
    comunidade = get_object_or_404(Comunidade, pk=pk)
    
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.comunidade = comunidade 
            mensagem.autor = request.user     
            mensagem.save()
            
            return redirect('chat_comunidade', pk=pk)
    else:
        form = MensagemForm()
    
    mensagens = MensagemComunidade.objects.filter(comunidade=comunidade).order_by('data_envio')[:50]
    
    context = {
        'comunidade': comunidade,
        'mensagens': mensagens,
        'form_mensagem': form,
        'usuario': request.user 
    }
    return render(request, 'core/chat_comunidade.html', context)