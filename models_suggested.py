from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_veteran = models.BooleanField(default=False)
    matricula = models.CharField(max_length=30, blank=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    curso = models.CharField(max_length=150, blank=True)
    semestre = models.PositiveSmallIntegerField(blank=True, null=True)
    contatos = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'

class Course(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    departamento = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    departamento = models.CharField(max_length=200, blank=True)
    perfil = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Subject(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=200)
    curso = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    professores = models.ManyToManyField(Professor, blank=True, related_name='subjects')
    semestre_oferecimento = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('codigo','nome')

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

class Evaluation(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1,6)]
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations')
    disciplina = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations')
    nota = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    dificuldades = models.TextField(blank=True)
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        who = self.professor or self.disciplina or 'Avaliação'
        return f'{self.autor} -> {who} ({self.nota}/5)'

class Community(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    membros = models.ManyToManyField(User, related_name='communities', blank=True)
    criado_em = models.DateTimeField(default=timezone.now)
    publico = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    titulo = models.CharField(max_length=250, blank=True)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo or (self.conteudo[:30] + '...')

class Message(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    conteudo = models.TextField()
    enviado_em = models.DateTimeField(default=timezone.now)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f'Mensagem de {self.remetente} para {self.destinatario}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    texto = models.CharField(max_length=300)
    link = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f'Notificação para {self.user} - {self.texto[:25]}'
