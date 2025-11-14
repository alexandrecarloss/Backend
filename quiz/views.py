import random
from rest_framework import viewsets ,permissions, status
from .models import Molecula, Pergunta, Sala, JogadorSala, Quiz
from .serializers import (
    MoleculaSerializer, PerguntaSerializer, SalaSerializer,
    JogadorSalaSerializer, QuizSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from user.models import User
from rest_framework.decorators import action
from firebase_admin import db

# --- Permissão: apenas admin pode editar moléculas e perguntas ---
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# --- ViewSets ---
class MoleculaViewSet(viewsets.ModelViewSet):
    queryset = Molecula.objects.all()
    serializer_class = MoleculaSerializer
    permission_classes = [IsAdminOrReadOnly]


class PerguntaViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntaSerializer
    permission_classes = [IsAdminOrReadOnly]


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [permissions.AllowAny]  # pode mudar depois se quiser

    def perform_create(self, serializer):
        sala = serializer.save(host=self.request.user if self.request.user.is_authenticated else None)

        # Cria sala no Firebase
        ref = db.reference(f"rooms/{sala.codigo}")
        ref.set({
            "status": "waiting",
            "current_question": 0,
            "players": {}
        })
        

    @action(detail=False, methods=['post'], url_path='entrar', permission_classes=[permissions.AllowAny])
    def entrar_sala(self, request):
        nome = request.data.get("nome")
        codigo_sala = request.data.get("codigo")

        if not nome or not codigo_sala:
            return Response({"erro": "Nome e código da sala são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        # Cria jogador anônimo se não existir
        if User.objects.filter(username=nome).exists():
            nome = f"{nome}_{random.randint(1000, 9999)}"
        jogador, _ = User.objects.get_or_create(username=nome, defaults={"is_guest": True})

        # Localiza sala
        try:
            sala = Sala.objects.get(codigo=codigo_sala, ativa=True)
        except Sala.DoesNotExist:
            return Response({"erro": "Sala não encontrada ou encerrada"}, status=status.HTTP_404_NOT_FOUND)

        # Adiciona jogador à sala
        JogadorSala.objects.get_or_create(sala=sala, jogador=jogador)
        
        # Cria sala no firebase
        ref = db.reference(f"rooms/{sala.codigo}/players/{jogador.id}")
        ref.set({
            "nome": jogador.username,
            "score": 0,
            "ready": False
        })

        return Response({
            "mensagem": f"{jogador.username} entrou na sala {sala.codigo}!",
            "jogador_id": jogador.id,
            "sala": SalaSerializer(sala).data
        })
    
        

class JogadorSalaViewSet(viewsets.ModelViewSet):
    queryset = JogadorSala.objects.all()
    serializer_class = JogadorSalaSerializer
    permission_classes = [permissions.AllowAny]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny]  # quiz pode ser criado anonimamente

    def perform_create(self, serializer):
        jogador = None
        if self.request.user.is_authenticated:
            jogador = self.request.user
        else:
            nome = self.request.data.get("nome", f"Guest_{random.randint(1000,9999)}")
            jogador, _ = User.objects.get_or_create(username=nome, defaults={"is_guest": True})

        serializer.save(jogador=jogador)
