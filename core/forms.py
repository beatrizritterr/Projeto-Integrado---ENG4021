# Arquivo: core/forms.py

from django import forms
from .models import Avaliacao, Disciplina 
from django.contrib.auth.forms import UserCreationForm 

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao 
        fields = ['disciplina', 'professor', 'nota', 'comentario']
