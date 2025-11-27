# Arquivo: core/models.py

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Avaliacao(models.Model):


    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    

    disciplina = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    

    nota = models.DecimalField(max_digits=2, decimal_places=1) 
    
    comentario = models.TextField()
    

    data_criacao = models.DateTimeField(auto_now_add=True) 

    def __str__(self):

        return f'{self.disciplina} ({self.professor}) - Nota: {self.nota}'