from rest_framework import serializers
from .models import Molecula, Pergunta, Sala, JogadorSala, Quiz
from user.models import User

class MoleculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Molecula
        fields = '__all__'

class PerguntaSerializer(serializers.ModelSerializer):
    molecula = MoleculaSerializer(read_only=True)
    molecula_id = serializers.PrimaryKeyRelatedField(
        queryset=Molecula.objects.all(),
        source="molecula",
        allow_null=True,
        required=False
    )

    class Meta:
        model = Pergunta
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Sala
        fields = '__all__'

class JogadorSalaSerializer(serializers.ModelSerializer):
    jogador = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = JogadorSala
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    perguntas = serializers.PrimaryKeyRelatedField(
        queryset=Pergunta.objects.all(),
        many=True
    )

    class Meta:
        model = Quiz
        fields = "__all__"
        extra_kwargs = {
            "jogador": {"required": False, "allow_null": True},
            "pontuacao": {"required": False},
            "sala": {"required": False, "allow_null": True},
        }



class UnityPerguntaSerializer(serializers.Serializer):
    molecula = serializers.CharField()
    enunciado = serializers.CharField()
    alternativas = serializers.ListField(child=serializers.CharField())
    respostaCorreta = serializers.IntegerField()
    dica = serializers.CharField()
    dificuldade = serializers.CharField()
    referencia = serializers.CharField()
    tempo = serializers.IntegerField()
