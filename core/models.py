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
    
class ProvaAntiga(models.Model):
    
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    
    # Ex: '2025.1'
    periodo_semestral = models.CharField(max_length=10) 
    
    data_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.disciplina.nome} - {self.periodo_semestral}'


class ArquivoProva(models.Model):
    """Representa o arquivo real (P1, P2, P3) que pode ser baixado."""
    
    prova_antiga = models.ForeignKey(ProvaAntiga, on_delete=models.CASCADE)
    
    tipo_prova = models.CharField(max_length=10) 
    
    arquivo = models.FileField(upload_to='provas/') 

    def __str__(self):
        return f'{self.prova_antiga.disciplina.nome} - {self.tipo_prova}'
    

class Evento(models.Model):
    
    # Usuário que criou o evento (se for um evento pessoal/de comunidade)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    
    # O campo mais importante: a data e hora do evento
    data_hora = models.DateTimeField() 
    
    # Cor/Categoria do evento (Ex: 'azul', 'laranja')
    categoria = models.CharField(max_length=15, default='azul') 
    
    def __str__(self):
        return f'{self.titulo} em {self.data_hora.strftime("%d/%m/%Y")}'