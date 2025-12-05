# Arquivo: core/models.py

from django.db import models
from django.contrib.auth import get_user_model
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Professor(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    professores = models.ManyToManyField(Professor, related_name='departamentos', blank=True)

    def __str__(self):
        return self.nome
    
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
    
    periodo_semestral = models.CharField(max_length=10) 
    
    data_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.disciplina.nome} - {self.periodo_semestral}'


class Evento(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    
    data_hora = models.DateTimeField() 
    
    categoria = models.CharField(max_length=15, default='azul') 
    
    def __str__(self):
        return f'{self.titulo} em {self.data_hora.strftime("%d/%m/%Y")}'
    

class Comunidade(models.Model):
    
    nome = models.CharField(max_length=150, unique=True)
    membros_count = models.IntegerField(default=0)
    icone_url = models.URLField(max_length=300, blank=True, null=True)
    membros = models.ManyToManyField(User, related_name='comunidades_inscritas', blank=True)

    def __str__(self):
        return self.nome
    
class Postagem(models.Model):
    TIPO_POST = [
        ('NOT', 'Notícia'),
        ('EVT', 'Evento'),
        ('OPR', 'Oportunidade'),
        ('DSC', 'Discussão'),
    ]
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=3, choices=TIPO_POST, default='DSC')
    
    curtidas_count = models.IntegerField(default=0)
    comentarios_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.titulo} por {self.autor.username}'

class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentário de {self.autor.username} em "{self.postagem.titulo}"'


def renomear_prova(instance, filename):
    """
    Renomeia o arquivo para o padrão: NomeDisciplina_Grau_Periodo.extensao
    Exemplo: Calculo1_P1_2023.1.pdf
    """
    ext = filename.split('.')[-1]
    nome_disciplina = instance.disciplina.nome.replace(' ', '')
    novo_nome = f"{nome_disciplina}_{instance.grau}_{instance.periodo}.{ext}"
    return os.path.join('provas_antigas/', novo_nome)

class ProvaAntiga(models.Model):
    OPCOES_GRAU = [
        ('P1', 'P1'),
        ('P2', 'P2'),
        ('P3', 'P3'),
        ('PF', 'PF'),
        ('2CH', '2ª Chamada'),
        ('Outro', 'Outro'),
    ]

    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    grau = models.CharField(max_length=10, choices=OPCOES_GRAU)
    periodo = models.CharField(max_length=10, help_text="Ex: 2023.1")
    arquivo = models.FileField(upload_to=renomear_prova, null=True, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disciplina} - {self.grau} ({self.periodo})"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100, blank=True)
    periodo = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()