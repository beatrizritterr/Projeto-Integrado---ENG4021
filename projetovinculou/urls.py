"""
URL configuration for projetovinculou project.

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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('appvinculo/', include('appvinculou.urls')),
    
    path('calendario/', views.calendario_page, name='calendario'), 
    
    path('login/', views.login_usuario, name='login'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    
    path('comunidades/', views.comunidades, name='comunidades'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('provas-antigas/', views.provas_antigas, name='provas_antigas'),
    
    path('avaliar-professor/', views.avaliar_prof, name='avaliar_prof'),
    path('avaliacoes-professores/', views.listar_avaliacoes_professores, name='avaliacoes_prof'),
    
    path('busca/', views.filtro_busca, name='busca'),
    path('filtro-post/', views.filtro_post, name='filtro_post'),
    
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),

]    


