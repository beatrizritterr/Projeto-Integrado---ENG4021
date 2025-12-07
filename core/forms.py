# Arquivo: core/forms.py - CÓDIGO CONSOLIDADO FINAL

from django import forms
from .models import (
    Avaliacao, 
    Disciplina, 
    Evento, 
    Postagem,
    Comunidade,
    Comentario,
    UserProfile,
    MensagemComunidade,
    # Modelos adicionados do segundo código:
    ProvaAntiga, 
    Perfil # Assumindo que Perfil é o modelo de dados adicionais do usuário
)
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model # Necessário para UserUpdateForm

User = get_user_model() # Define o modelo de Usuário para UserUpdateForm

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
        
# --- Forms Adicionados do Segundo Código ---

class ProvaAntigaForm(forms.ModelForm):
    class Meta:
        model = ProvaAntiga
        fields = ['disciplina', 'grau', 'periodo', 'arquivo']
        widgets = {
            'periodo': forms.TextInput(attrs={'placeholder': 'Ex: 2023.1'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        # Se você usa UserProfile para dados de perfil e Perfil para foto, 
        # mantenha Perfil (ou ajuste para UserProfile se for o mesmo modelo)
        model = Perfil 
        fields = ['curso', 'periodo', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

# --- Forms Originais ---

class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'conteudo', 'tipo', 'arquivo_anexo'] 
        
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título da Postagem'}),
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva seu conteúdo aqui...', 'rows': 5}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo'] 
        widgets = {
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva um comentário...', 'rows': 2}),        
            }
        
class ProfileUpdateForm(forms.ModelForm):
    # Este form é mantido, presumivelmente para lidar especificamente com 'foto_perfil'
    class Meta:
        model = UserProfile
        fields = ['foto_perfil']

class ComunidadeForm(forms.ModelForm):
    class Meta:
        model = Comunidade
        fields = ['nome', 'descricao', 'icone']
        
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }


class MensagemForm(forms.ModelForm):
    class Meta:
        model = MensagemComunidade
        fields = ['conteudo']
        
        widgets = {
            'conteudo': forms.TextInput(attrs={'placeholder': 'Digite sua mensagem...', 'autocomplete': 'off'}),
        }