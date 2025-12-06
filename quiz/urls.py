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
    path("moleculas/count/", moleculas_count),
    path("perguntas/count/", perguntas_count),
]
