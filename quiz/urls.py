from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    MoleculaViewSet, PerguntaViewSet, SalaViewSet,
    JogadorSalaViewSet, QuizViewSet, moleculas_count, perguntas_count
)

router = DefaultRouter()
router.register('moleculas', MoleculaViewSet)
router.register('perguntas', PerguntaViewSet)
router.register('salas', SalaViewSet)
router.register('jogadores-sala', JogadorSalaViewSet)
router.register('quizzes', QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("perguntas-total/", perguntas_count),
    path("moleculas-total/", moleculas_count),
]
