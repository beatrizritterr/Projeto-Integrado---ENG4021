# Arquivo: core/forms.py

from django import forms
from .models import (
    Avaliacao, 
    Disciplina, 
    Evento, 
    Postagem,
    Comunidade
)
from django.contrib.auth.forms import UserCreationForm 

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao 
        fields = ['disciplina', 'professor', 'nota', 'comentario']
class EventoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data e Hora do Evento"
    )
    class Meta:
        model = Evento
        fields = ['titulo', 'data_hora', 'categoria', 'descricao'] 

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: P1 de Cálculo II'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Detalhes (opcional)', 'rows': 3}),
        }
class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'conteudo', 'tipo'] 
        
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da Postagem'}),
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva seu conteúdo aqui...', 'rows': 5}),
        }