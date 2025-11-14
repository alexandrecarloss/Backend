from django.db import models
from user.models import User
import random, string
from django.utils import timezone

class Molecula(models.Model):
    nome = models.CharField(max_length=100)
    formula = models.CharField(max_length=50)
    massaMolar = models.FloatField()
    polaridade = models.CharField(max_length=50)
    densidade = models.FloatField(null=True, blank=True)
    pontoEbulicao = models.FloatField(null=True, blank=True)
    pontoFusao = models.FloatField(null=True, blank=True)
    caracteristicas = models.TextField(blank=True)
    geometria = models.CharField(max_length=100, blank=True)
    fontes = models.TextField(blank=True)
    aplicacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.formula})"


class Sala(models.Model):
    codigo = models.CharField(max_length=6, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salas_hosteadas")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Sala {self.codigo} ({'Ativa' if self.ativa else 'Encerrada'})"


class JogadorSala(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="jogadores")
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    conectado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.jogador.username} - {self.sala.codigo}"


class Pergunta(models.Model):
    RESPOSTA_CHOICES = (
        ('a', 'A'), 
        ('b', 'B'), 
        ('c', 'C'), 
        ('d', 'D')
      )
    DIFICULDADE_CHOICES = (
        ('F', 'Fácil'), 
        ('M', 'Média'), 
        ('D', 'Difícil')
      )

    molecula = models.ForeignKey(Molecula, on_delete=models.CASCADE, related_name="perguntas", blank=True, null=True)
    enunciado = models.CharField(max_length=255)
    alternativa_a = models.CharField(max_length=255)
    alternativa_b = models.CharField(max_length=255)
    alternativa_c = models.CharField(max_length=255)
    alternativa_d = models.CharField(max_length=255)
    resposta_correta = models.CharField(max_length=1, choices=RESPOSTA_CHOICES)
    dica = models.CharField(max_length=255)
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE_CHOICES)
    referencia = models.CharField(max_length=255)

    def __str__(self):
        if self.molecula:
            return f"{self.molecula.nome}: {self.enunciado[:50]}..."
        return f"{self.enunciado[:50]}..."


class Quiz(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    perguntas = models.ManyToManyField("Pergunta", related_name="quizzes")
    pontuacao = models.IntegerField(default=0)
    dataHora = models.DateTimeField(default=timezone.now)
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True, related_name="quizzes")

    def __str__(self):
        return f"Quiz de {self.jogador.username} - {self.pontuacao} pts em {self.dataHora.strftime('%d/%m/%Y %H:%M')}"
