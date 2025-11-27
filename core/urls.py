
from django.urls import path
from . import views

urlpatterns = [
    # Mapeia a URL raiz da app para a função 'home' em views.py
    path('', views.home, name='home'),
    # Exemplo para a página de login
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('comunidades/', views.comunidades, name='comunidades'),
    path('avaliacaoprof/', views.avaliacaoprof, name='avaliacaoprof'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('filtrobusca/', views.filtrobusca, name='filtrobusca'),
    path('filtropost/', views.filtropost, name='filtropost'),
    path('provasantigas/', views.provasantigas, name='provasantigas'),
    path('reset-dev/', views.password_reset_dev, name='password_reset_dev'),

]