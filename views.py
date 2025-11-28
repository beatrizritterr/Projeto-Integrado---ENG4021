from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Disciplina, Avaliacao
from .forms import AvaliacaoForm

@login_required
def avaliar_disciplinas(request):
    disciplinas = Disciplina.objects.all()

    if request.method == 'POST':
        disciplina_id = request.POST.get('disciplina_id')
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        form = AvaliacaoForm(request.POST)

        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.aluno = request.user
            avaliacao.disciplina = disciplina
            avaliacao.save()
            return redirect('avaliar_disciplinas')
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacoes_form.html', {
        'disciplinas': disciplinas,
        'form': form
    })