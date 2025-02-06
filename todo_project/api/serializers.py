from rest_framework import serializers
from base.models import Lista, Entrada
from django.contrib.auth.models import User


class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = "__all__"

class FullListaSerializer(serializers.ModelSerializer):
    # Primeiro, crio os campos que quero colocar a mais na minha serialização.
     # Naturalmente, iria retornar só os três primerios ali do fields.
    nome_autor = serializers.SerializerMethodField()
    id_autor = serializers.SerializerMethodField()

    # Os nomes são importantes, pois temos que criar funcoes com o prefixo get_

    class Meta:
        model = Lista
        fields = ["id", "nome_lista", "data_criacao", "nome_autor", "id_autor"]

    # O obj é passado automaticamente, como eu sei que o objeto lista tem o campo usuário, e o campo usuario tem username, consigo retornar de boa
    def get_nome_autor(self, obj):
        return obj.usuario.username
    
    def get_id_autor(self, obj):
        return obj.usuario.id
    
class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
