from django.db import models
from django.contrib.auth.models import User

# Nesse projeto, não vou mudar o modelo de usuario padrão do django.

class Lista(models.Model):
    nome_lista = models.CharField(max_length=30)
    data_criacao = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_lista

class Entrada(models.Model):
    class Estado(models.TextChoices):
        PENDENTE = 'P', 'Pendente'
        CONCLUIDO = 'C', 'Concluido'
        EM_PROGRESSO = 'EP', 'Em progresso'

    nome_entrada = models.CharField(max_length=50, null=False, blank=False)
    estado = models.CharField(max_length=2, choices=Estado.choices, default=Estado.PENDENTE)
    lista_origem = models.ForeignKey(Lista, null=False, blank=False, related_name="entradas", on_delete=models.CASCADE) 


    


