from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    professores = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Avaliacao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.codigo} ({self.nota})"