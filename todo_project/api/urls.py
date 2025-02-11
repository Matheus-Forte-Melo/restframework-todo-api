from django.urls import path
from . import views

urlpatterns = [
    path("lista/entradas/pegar/<int:pk>/", views.pegar_entradas_lista, name="pegar_entradas_lista"),
    path("usuario/lista/pegar/<int:pk>/", views.pegar_listas_usuario, name="pegar_listas_usuario"),
    path("lista/pegar_listas_inteiras/", views.pegar_listas_inteiras, name="pegar_listas_inteiras"),
    path("lista/pegar_todas/", views.pegar_listas, name="pegar_listas"),
    path("usuario/signin/", views.register_user, name="register_user"),
    path("usuario/login/", views.login_user, name="login_user"),
    path("lista/criar/", views.criar_lista, name="criar_lista"),
    path("lista/deletar/<int:pk>/", views.deletar_lista, name="deletar_lista"),
    path("entrada/criar/", views.adicionar_entrada, name="adicionar_entrada"),
    path("entrada/deletar/<int:pk>/", views.deletar_entrada, name="deletar_entrada"),
    path("entrada/atualizar/<int:pk>/", views.atualizar_entrada, name="atualizar_entrada")   
]