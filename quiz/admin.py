from django.contrib import admin
from .models import Molecula, Pergunta, Sala, JogadorSala

# Register your models here.
admin.site.register(Molecula)
admin.site.register(Pergunta)
admin.site.register(Sala)
admin.site.register(JogadorSala)
