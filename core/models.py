# Arquivo: core/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f'{self.nome} ({self.codigo or "Sem Código"})'


class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    professor = models.CharField(max_length=100) 
    
    nota = models.DecimalField(max_digits=2, decimal_places=1) 
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.disciplina.nome} ({self.professor}) - Nota: {self.nota}'