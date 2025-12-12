from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Páginas Principais
    path('', views.home, name='home'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('avaliacaoprof/', views.avaliacaoprof, name='avaliacaoprof'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('filtrobusca/', views.filtrobusca, name='filtrobusca'),
    path('filtropost/', views.filtropost, name='filtropost'),
    path('provasantigas/', views.provasantigas, name='provasantigas'),
    path('reset-dev/', views.password_reset_dev, name='password_reset_dev'),
    
    # URL de Busca de Perfis
    path('busca_perfis/', views.busca_perfis, name='busca_perfis'),

    # Perfil e Detalhe de Perfil
    path('perfil/', views.perfil, name='perfil'),
    
        path('perfil/<int:pk>/modal/', views.perfil_detalhe_ajax, name='perfil_detalhe_ajax'), 
    
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/foto/deletar/', views.deletar_foto_perfil, name='deletar_foto_perfil'),
    path('perfil/detalhes/editar/', views.editar_perfil_detalhes, name='editar_perfil_detalhes'),

    # Eventos (Home/Calendário)
    path('evento/adicionar/', views.adicionar_evento, name='adicionar_evento'),
    path('evento/editar/<int:event_id>/', views.editar_evento, name='editar_evento'),
    path('evento/excluir/<int:event_id>/', views.excluir_evento, name='excluir_evento'),

    # Postagens (FiltroPost)
    path('post/<int:pk>/curtir/', views.curtir_postagem, name='curtir_postagem'),
    path('post/<int:pk>/salvar/', views.salvar_postagem, name='salvar_postagem'),
    path('post/<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),

    # Comunidades
    path('comunidades/', views.comunidades, name='comunidades'),
    path('comunidades/criar/', views.criar_comunidade, name='criar_comunidade'), 
    path('comunidades/inscrever/<int:pk>/', views.inscrever_comunidade, name='inscrever_comunidade'), 
    path('comunidades/chat/<int:pk>/', views.chat_comunidade, name='chat_comunidade'),

    # Autenticação
    path('logout/', 
         LogoutView.as_view(next_page='/login/'), 
         name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)