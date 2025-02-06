from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from base.models import Entrada, Lista
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from . import serializers

# Create your views here.

@api_view(["GET"])
def get_listas_usuario(request, pk):
    try:
        user = User.objects.get(id=pk)
        listas = Lista.objects.filter(usuario=user)
        print(user, listas)
    except User.DoesNotExist:
        return Response({"erro": "Esse usuário não existe."}, status.HTTP_404_NOT_FOUND)

    # Se o usuario tiver só uma lista, dá erro, arruamr
    serializer = serializers.ListaSerializer(listas, many=True)

    return Response(serializer.data, status.HTTP_200_OK)
    
@api_view(["GET"])
def get_entradas_lista(request, pk):
    try:
        entradas = Entrada.objects.filter(lista_origem=pk)
    except Entrada.DoesNotExist:
        return Response({"erro": "Essa lista não existe."}, status.HTTP_404_NOT_FOUND)

    serializer = serializers.EntradaSerializer(entradas, many=True)

    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def get_full_listas(request):
    listas = Lista.objects.all()
    serializer = serializers.FullListaSerializer(listas, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def get_all_listas(request):
    listas = Lista.objects.all()
    serializer = serializers.ListaSerializer(listas, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    # Talvez eu precise de um algoritimo melhor para senhas. Acho que não ta funcionando muito bem
    # Talvez algo haver com token? ou o hashing?
    serializer = serializers.UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"mensagem": f"Usuário {serializer.data["username"]} criado com sucesso."}, status.HTTP_201_CREATED)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)
    serializer = serializers.UserSerializer(user)

    if user is not None:
        login(request, user)
        return Response({"mensagem": "Usuário logado.", "dados": serializer.data}, status.HTTP_202_ACCEPTED)   
    return Response({"mensagem": "Senha ou nome de usuário incorretos.", "dados": serializer.data}, status.HTTP_400_BAD_REQUEST)   

# Nota para si: Não usar serializador para autenticar ou logar usuários. Ele meio que já faz o trabalho de autenticação, e eu tava entando fazer DUAS vezes. Pra tirar dados, colocar e atualizar, tudo bem, mas para coisas adversas melhor fazer só com os resquest mesmo.

@api_view(['POST'])
def criar_lista(request):
    serializer = serializers.ListaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        if "usuario" in serializer.errors:
            return Response({"erro": "Usuário inválido. Insira um ID válido."}, status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def deletar_lista(request):
    id_lista = request.data.get("id")

    try:
        # Existe a função adelete, então talvez seja jogo. Talvez nao na verdade, isso nao é algo a ser autenticado
        lista = Lista.objects.get(id=id_lista)
        lista.delete()   
    except Lista.DoesNotExist:
        return Response({"erro": "Lista inválida!"}, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"erro": "Erro desconhecido."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"mensagem": "lista deletada com sucesso"}, status.HTTP_200_OK)

@api_view(['POST'])
def adicionar_entrada(request):
    serializer = serializers.EntradaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def deletar_entrada(request):
    id_entrada = request.data.get("id")

    try:
        entrada = Entrada.objects.get(id=id_entrada)
        entrada.delete()   
    except Entrada.DoesNotExist:
        return Response({"erro": "Entrada inválida!"}, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"erro": "Erro desconhecido."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"mensagem": f"Entrada ({entrada.nome_entrada}) deletada com sucesso"}, status.HTTP_200_OK)

@api_view(['PATCH'])
def atualizar_entrada(request):
    id_entrada = request.data.get("id")

    try:
        entrada = Entrada.objects.get(id=id_entrada)
    except Entrada.DoesNotExist:
        return Response({"erro": "Essa entrada não existe"}, status=status.HTTP_404_NOT_FOUND)

    # Pra atualizar tem que passar o objeto, se não nao atualiza, e sim cria. Tal qual o partial
    serializer = serializers.EntradaSerializer(entrada, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status.HTTP_200_OK)

# @api_view(['PATCH'])
# def atualizar_entrada(request):
#     id_entrada = request.data.get("id")
#     estado = request.data.get("estado").upper()

#     print(estado)

#     if estado not in ["P", "C", "EP"]:
#         return Response({"erro": "Estado inválido."})

#     try:
#         entrada = Entrada.objects.get(id=id_entrada)
#         entrada.estado = estado
#         entrada.save() 
#     except Exception:
#         return Response({"erro": "Entrada inválida!"})
    
#     return Response({"mensagem": f"Entrada ({entrada.nome_entrada}) alterada para {estado} com sucesso"})

    
