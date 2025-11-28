from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('comunidades/', views.comunidades, name='comunidades'),
    path('avaliacaoprof/', views.avaliacaoprof, name='avaliacaoprof'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('filtrobusca/', views.filtrobusca, name='filtrobusca'),
    path('filtropost/', views.filtropost, name='filtropost'),
    path('provasantigas/', views.provasantigas, name='provasantigas'),
    path('reset-dev/', views.password_reset_dev, name='password_reset_dev'),
    path('adicionar-evento/', views.adicionar_evento, name='adicionar_evento'),

    # ROTAS DO FORMULÁRIO DE AVALIAÇÃO (devem estar DENTRO da lista)
    path('avaliar-disciplina/', views.avaliar_disciplina, name='avaliar_disciplina'),
    path('avaliar-disciplina/sucesso/', views.avaliacao_sucesso, name='avaliacao_sucesso'),

    path('conta/editar/', views.editar_conta, name='editar_conta'),
    path('conta/excluir/', views.excluir_conta, name='excluir_conta'),

]
