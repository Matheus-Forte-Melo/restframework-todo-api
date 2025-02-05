from django.contrib import admin
from .models import Entrada, Lista

class ListaAdm(admin.ModelAdmin):
    list_display = ('nome_lista', 'data_criacao', 'usuario') # , 'data_criacao'

class EntradaAdm(admin.ModelAdmin):
    list_display = ('nome_entrada', 'estado', "lista_origem")

# Register your models here.
admin.site.register(Entrada, EntradaAdm)
admin.site.register(Lista, ListaAdm)

