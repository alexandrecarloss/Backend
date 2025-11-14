from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import random

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def guest(self, request):
        nome = request.data.get("nome", None)

        if not nome:
            return Response({"erro": "Informe um nome"}, status=400)

        # Evitar nomes duplicados
        if User.objects.filter(username=nome).exists():
            nome = f"{nome}_{random.randint(1000, 9999)}"

        user = User.objects.create(username=nome, is_guest=True)
        return Response({"id": user.id, "username": user.username})

