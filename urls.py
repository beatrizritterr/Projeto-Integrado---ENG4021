from django.urls import path
from . import views

urlpatterns = [
    ath('admin/', admin.site.urls),
    path('', include('core.urls')), 
    path('', views.home, name='home'),
    path('avaliacoes/', views.avaliar_disciplinas, name='avaliar_disciplinas'),
]