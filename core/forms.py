# Arquivo: core/forms.py

from django import forms
from .models import Avaliacao, Disciplina, Evento
from django.contrib.auth.forms import UserCreationForm 

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao 
        fields = ['disciplina', 'professor', 'nota', 'comentario']
class EventoForm(forms.ModelForm):
    # O widget DateTimeInput com type="datetime-local" melhora a experiência no navegador
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data e Hora do Evento"
    )
    class Meta:
        model = Evento
        # Não incluímos 'usuario' aqui, pois ele será adicionado na View
        fields = ['titulo', 'data_hora', 'categoria', 'descricao'] 

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: P1 de Cálculo II'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Detalhes (opcional)', 'rows': 3}),
        }
