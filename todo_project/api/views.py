from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import Entrada, Lista
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from . import serializers

def not_permit(request, id_alternativo=None) -> bool:
    """
    Essa forma de validação NÃO é a recomendada, muita manutenção terá que ser feita caso algo seja mudado.
    Fiz só porque estou com pressa para aprender novas tecnologias e esse é um dos meus ultimos projetos grandes nessa linguagem por enquanto.
    """
    if not id_alternativo:
        return not request.user.is_superuser and str(request.user.id) != request.data.get("usuario")
    else:
        return not request.user.is_superuser and str(request.user.id) != str(id_alternativo)
        
@api_view(["GET"])
def pegar_listas_usuario(request, pk):
    """
    Pega todas as listas conforme o id do usuário informado
    """
    try:
        user = User.objects.get(id=pk)
        if not_permit(request, user.id):
            return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
        listas = Lista.objects.filter(usuario=user)
    except User.DoesNotExist:
        return Response({"erro": "Esse usuário não existe."}, status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.ListaSerializer(listas, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
    
@api_view(["GET"])
def pegar_entradas_lista(request, pk):
    """
    Pega todas as entradas conforme o id da lista informado
    """
    try:
        entradas = Entrada.objects.filter(lista_origem=pk)
    except Entrada.DoesNotExist:
        return Response({"erro": "Essa lista não existe."}, status.HTTP_404_NOT_FOUND)
    serializer = serializers.EntradaSerializer(entradas, many=True)

    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def pegar_listas_inteiras(request):
    """
    Retorna TODAS as listas com informações mais avançadas. Apenas para superusuarios.
    """
    if not request.user.is_superuser:
        return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)

    listas = Lista.objects.all()
    serializer = serializers.FullListaSerializer(listas, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['GET'])
def pegar_listas(request):
    """
    Retorna TODAS as listas com informações basicas. Apenas para superusuarios.
    """
    if not request.user.is_superuser:
        return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
    listas = Lista.objects.all()
    serializer = serializers.ListaSerializer(listas, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    """
    Registra e autentica um usuário.
    Devo revisar essa função. Acho que está com algum erro na hora de criar a senha.
    """
    serializer = serializers.UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"mensagem": f"Usuário {serializer.data["username"]} criado com sucesso."}, status.HTTP_201_CREATED)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# Pensando em remover, ja existe API_AUTH, então sinceramente nem sei se é necessário
@api_view(["POST"])
def login_user(request):
    """
    Faz o login de um usuário, para que possa usar o sistema. (OBRIGATÓRIO, SEM CONTA VOCÊ NÃO PODERÁ FAZER NADA)
    """
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    serializer = serializers.UserSerializer(user)

    if user is not None:
        login(request, user)
        return Response({"mensagem": "Usuário logado.", "dados": serializer.data}, status.HTTP_202_ACCEPTED)   
    return Response({"mensagem": "Senha ou nome de usuário incorretos.", "dados": serializer.data}, status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
def criar_lista(request):
    """
    Cria uma lista.
    """
    serializer = serializers.ListaSerializer(data=request.data)
    if not_permit(request):
        return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        if "usuario" in serializer.errors:
            return Response({"erro": "Usuário inválido. Insira um ID válido."}, status.HTTP_404_NOT_FOUND)
        
@api_view(['DELETE'])
def deletar_lista(request, pk):
    """
    Deleta uma lista e todas suas entradas conforme o ID da lista
    """
    try:
        # Existe a função adelete, então talvez seja jogo. Talvez nao na verdade, isso nao é algo a ser autenticado
        lista = Lista.objects.get(id=pk)
        if not_permit(request, lista.usuario.id):
            return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)

        lista.delete()   
    except Lista.DoesNotExist:
        return Response({"erro": "Lista inválida!"}, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"erro": "Erro desconhecido."}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"mensagem": "lista deletada com sucesso"}, status.HTTP_200_OK)

@api_view(['POST'])
def adicionar_entrada(request):
    """
    Adiciona uma entrada a uma lista anteriormente criada pelo usuário.
    """
    serializer = serializers.EntradaSerializer(data=request.data)
    if serializer.is_valid():
        # Chamo os validated_data invez de data. Pq data ja esta formatado pro BD e nao pode ser alterado.
        # Já validated_data é o objeto em si, sem formatação.
        lista = serializer.validated_data["lista_origem"]
        if not_permit(request, lista.usuario.id):
            return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deletar_entrada(request, pk):
    """
    Deleta uma entrada da lista conforme seu ID.
    """
    try:
        entrada = Entrada.objects.get(id=pk)
        if not_permit(request, entrada.lista_origem.usuario.id):
            return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
        entrada.delete()   
    except Entrada.DoesNotExist:
        return Response({"erro": "Entrada inválida!"}, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"erro": "Erro desconhecido."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"mensagem": f"Entrada ({entrada.nome_entrada}) deletada com sucesso"}, status.HTTP_200_OK)

@api_view(['PATCH'])
def atualizar_entrada(request, pk):
    """
    Atualiza entrada. No momento, o proprietário da entrada pode transferir sua entrada para outra lista. Isso será corrigido
    assim que eu implementar um sistema de autorização melhor.
    """
    try:
        entrada = Entrada.objects.get(id=pk)
        # Um usuário pode setar a origem de sua entrada para outra lista. Assim transfindo-a. Interessante.
        if not_permit(request, entrada.lista_origem.usuario.id):
            return Response("Você não tem permissão para isso", status.HTTP_401_UNAUTHORIZED)
    except Entrada.DoesNotExist:
        return Response({"erro": "Essa entrada não existe"}, status=status.HTTP_404_NOT_FOUND)
    # Pra atualizar tem que passar o objeto, se não nao atualiza, e sim cria. Tal qual o partial
    serializer = serializers.EntradaSerializer(entrada, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status.HTTP_200_OK)