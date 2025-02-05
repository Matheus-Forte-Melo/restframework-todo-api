from rest_framework.response import Response
from rest_framework.decorators import api_view

from base.models import Entrada, Lista
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from . import serializers

# Create your views here.
@api_view(['GET'])
def get_full_listas(request):
    listas = Lista.objects.all()
    serializer = serializers.FullListaSerializer(listas, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_all_listas(request):
    listas = Lista.objects.all()
    serializer = serializers.ListaSerializer(listas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    serializer = serializers.UserSerializer(data=request.data)
    
    if serializer.is_valid():
        # print(serializer.data)
        serializer.save()
        return Response({"mensagem": f"Usuário {serializer.data["username"]} criado com sucesso."})
    else:
        print("Ocorreu um erro")

    return Response(serializer.errors) # Retorno os proprios dados, sempre é bom ter algo pra retornar.

@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"mensagem": "Usuário logado.", "dados": request.data})   
    return Response({"mensagem": "Senha ou nome de usuário incorretos.", "dados": request.data})   

# Nota para si: Não usar serializador para autenticar ou logar usuários. Ele meio que já faz o trabalho de autenticação, e eu tava entando fazer DUAS vezes. Pra tirar dados, colocar e atualizar, tudo bem, mas para coisas adversas melhor fazer só com os resquest mesmo.

@api_view(['POST'])
def criar_lista(request):
    serializer = serializers.ListaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        if "usuario" in serializer.errors:
 
            return Response({"erro": "Usuário inválido. Insira um ID válido."})
        
@api_view(['POST'])
def deletar_lista(request):
    id_lista = request.data.get("id")

    try:
        # Existe a função adelete, então talvez seja jogo. Talvez nao na verdade, isso nao é algo a ser autenticado
        lista = Lista.objects.get(id=id_lista)
        lista.delete()   
    except Exception:
        return Response({"erro": "Lista inválida!"})

    return Response({"mensagem": "lista deletada com sucesso"})

@api_view(['POST'])
def adicionar_entrada(request):
    serializer = serializers.EntradaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def deletar_entrada(request):
    id_entrada = request.data.get("id")

    try:
        entrada = Entrada.objects.get(id=id_entrada)
        entrada.delete()   
    except Exception:
        return Response({"erro": "Entrada inválida!"})

    return Response({"mensagem": f"Entrada ({entrada.nome_entrada}) deletada com sucesso"})

@api_view(['POST'])
def atualizar_entrada(request):
    id_entrada = request.data.get("id")
    estado = request.data.get("estado").capitalize()

    if estado not in ["P", "C", "EP"]:
        return Response({"erro": "Estado inválido."})

    try:
        entrada = Entrada.objects.get(id=id_entrada)
        entrada.estado = estado
        entrada.save() 
    except Exception:
        return Response({"erro": "Entrada inválida!"})
    
    return Response({"mensagem": f"Entrada ({entrada.nome_entrada}) alterada para {estado} com sucesso"})

    
