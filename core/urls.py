
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

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
    path('evento/adicionar/', views.adicionar_evento, name='adicionar_evento'),
    path('evento/editar/<int:event_id>/', views.editar_evento, name='editar_evento'),
    path('evento/excluir/<int:event_id>/', views.excluir_evento, name='excluir_evento'),
    path('post/<int:pk>/curtir/', views.curtir_postagem, name='curtir_postagem'),
    path('post/<int:pk>/salvar/', views.salvar_postagem, name='salvar_postagem'),
    path('post/<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    path('logout/', 
         LogoutView.as_view(next_page='/login/'), 
         name='logout'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/foto/deletar/', views.deletar_foto_perfil, name='deletar_foto_perfil'),
    path('comunidades/criar/', views.criar_comunidade, name='criar_comunidade'), 
    path('comunidades/inscrever/<int:pk>/', views.inscrever_comunidade, name='inscrever_comunidade'), 
    path('comunidades/chat/<int:pk>/', views.chat_comunidade, name='chat_comunidade'),
    path('busca_perfis/', views.busca_perfis, name='busca_perfis'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)