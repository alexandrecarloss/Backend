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
        queryset=Molecula.objects.all(), source='molecula', write_only=True
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
    perguntas = PerguntaSerializer(many=True, read_only=True)
    jogador = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'
