"""
URL configuration for proj_software project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Arquivo: proj_software/urls.py (ESTE JÁ EXISTE)

from django.contrib import admin
from django.urls import path, include  # IMPORTANTE: Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conecta o App 'core' à URL base do projeto ('' ou seja, http://127.0.0.1:8000/)
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
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

    # ➤ Aqui entram as novas rotas (update e delete)
    path('avaliacoes/<int:pk>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacoes/<int:pk>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),
]
