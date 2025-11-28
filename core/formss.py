# core/formss.py
from django import forms
from .models import Avaliacao, Evento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------------------
# FORM DE CRIAÇÃO DE USUÁRIO
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields


# ----------------------------
# FORMULÁRIO DE AVALIAÇÃO
# ----------------------------
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['disciplina', 'professor', 'nota', 'comentario']

        widgets = {
            'disciplina': forms.Select(attrs={'class': 'input'}),
            'professor': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome do professor'}),
            'nota': forms.NumberInput(attrs={
                'class': 'input',
                'step': '0.1',
                'min': '0',
                'max': '5',
                'placeholder': 'Ex: 4.5'
            }),
            'comentario': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
        }

        labels = {
            'disciplina': 'Disciplina',
            'professor': 'Professor',
            'nota': 'Nota (0 a 5)',
            'comentario': 'Comentário',
        }


# ----------------------------
# FORMULÁRIO DE EVENTO (corrigido)
# ----------------------------
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
            'categoria': forms.TextInput(),
        }

class ContaPessoalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'email@exemplo.com'}),
        }

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
