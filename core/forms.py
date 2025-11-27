
from django import forms
from .models import Avaliacao
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['disciplina', 'professor', 'nota', 'comentario']
        
        widgets = {
            'disciplina': forms.TextInput(attrs={'placeholder': 'Ex: Cálculo 2'}),
            'professor': forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}),
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.5}),
            'comentario': forms.Textarea(attrs={'placeholder': 'Compartilhe sua experiência...'}),
        }