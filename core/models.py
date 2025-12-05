from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

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
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    nota = models.DecimalField(max_digits=3, decimal_places=1)
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.disciplina.nome} ({self.professor.nome}) - Nota: {self.nota}'


class ProvaAntiga(models.Model):

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    periodo_semestral = models.CharField(max_length=10)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.disciplina.nome} - {self.periodo_semestral}'


class ArquivoProva(models.Model):
    prova_antiga = models.ForeignKey(ProvaAntiga, on_delete=models.CASCADE)
    tipo_prova = models.CharField(max_length=10)
    arquivo = models.FileField(upload_to='provas/')

    def __str__(self):
        return f'{self.prova_antiga.disciplina.nome} - {self.tipo_prova}'


class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField()
    categoria = models.CharField(max_length=15, default='azul')

    def __str__(self):
        return f'{self.titulo} em {self.data_hora.strftime("%d/%m/%Y")}'


class Comunidade(models.Model):
    """Representa uma comunidade ou grupo."""
    
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(max_length=500, blank=True, null=True) # <-- NOVO
    
    icone = models.ImageField(upload_to='comunidade_icones/', blank=True, null=True) # <-- NOVO
    
    membros_count = models.IntegerField(default=0)
    
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comunidades_inscritas', blank=True)

    def __str__(self):
        return self.nome


class Postagem(models.Model):
    TIPO_POST = [
        ('NOT', 'Notícia'),
        ('EVT', 'Evento'),
        ('OPR', 'Oportunidade'),
        ('DSC', 'Discussão'),
    ]

    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=3, choices=TIPO_POST, default='DSC')

    comentarios_count = models.IntegerField(default=0)
    curtidas = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='curtidas_post', blank=True)
    salvamentos = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='salvamentos_post', blank=True)

    arquivo_anexo = models.FileField(upload_to='post_anexos/', blank=True, null=True)

    def __str__(self):
        return f'{self.titulo} por {self.autor.username}'


class Comentario(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()    
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor.username} em "{self.postagem.titulo[:20]}"'

class UserProfile(models.Model):
    """Armazena informações adicionais do usuário, como foto e biografia."""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    foto_perfil = models.ImageField(default='perfil_padrao.png', upload_to='profile_pics')
    
    curso = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class MensagemComunidade(models.Model):
    """Armazena as mensagens trocadas dentro de uma comunidade."""
    
    comunidade = models.ForeignKey('Comunidade', on_delete=models.CASCADE, related_name='mensagens')
    
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    conteudo = models.TextField()
    
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor.username}: {self.conteudo[:30]}'

    class Meta:
        ordering = ['data_envio'] 