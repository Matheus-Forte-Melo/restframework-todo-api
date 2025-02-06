from django.urls import path
from . import views

urlpatterns = [
    path("get_entradas_lista/<int:pk>/", views.get_entradas_lista, name="get_entradas_lista"),
    path("get_listas_usuario/<int:pk>/", views.get_listas_usuario, name="get_listas_usuario"),
    path("get_full_listas/", views.get_full_listas, name="get_full_listas"),
    path("get_all_listas/", views.get_all_listas, name="get_all_listas"),
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("criar_lista/", views.criar_lista, name="criar_lista"),
    path("deletar_lista/", views.deletar_lista, name="deletar_lista"),
    path("adicionar_entrada/", views.adicionar_entrada, name="adicionar_entrada"),
    path("deletar_entrada/", views.deletar_entrada, name="deletar_entrada"),
    path("atualizar_entrada/", views.atualizar_entrada, name="atualizar_entrada")
    
]