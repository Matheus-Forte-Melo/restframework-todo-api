💡 NOTA: Abaixo está uma introdução de como utilizar esta API. Note que ela não está hospedada, então recomendo rodá-la localmente. Basta ativar o ambiente virtual e executar o comando:

```bash
python manage.py runserver
```

Depois, basta acessar o link gerado para interagir com a API.

Além disso, a documentação foi escrita por mim, mas aprimorada com auxílio de inteligência artificial para torná-la mais clara e agradável. Sinta-se à vontade para modificá-la conforme necessário!

---

# 📖 Introdução
Esta API permite o gerenciamento de listas e entradas de tarefas. Para utilizá-la, é necessário estar autenticado.

- **Usuários comuns** podem gerenciar apenas suas próprias listas e entradas.
- **Superusuários** têm acesso irrestrito.

---

## 🛠 Superusuário Padrão
- **Username**: Admin
- **Password**: admin123
- **ID no banco de dados**: 9 (caso necessário)

Nota #1: Qualquer pessoa pode acessar a API utilizando este superusuário, que possui permissão para todas as operações.

Nota #2: Com esse usuário você pode manipular os dados usando o admin panel do Django, se quiser saber mais sobre, desça até o fim deste readme.

---

## 🔑 Autenticação
Antes de realizar qualquer operação, é necessário autenticar-se. Você pode registrar um novo usuário ou fazer login com um existente.

### ✍️ Registrar um Usuário
**Endpoint:** `POST /todo-api/usuario/signin/`

📩 **Corpo da requisição:**
```json
{
  "username": "meu_usuario",
  "password": "minha_senha",
  "email": "meu@email.com"
}
```
✅ **Resposta de sucesso:**
```json
{
  "mensagem": "Usuário meu_usuario criado com sucesso."
}
```

### 🔓 Login de Usuário
**Endpoint:** `POST /todo-api/usuario/login/`

📩 **Corpo da requisição:**
```json
{
  "username": "meu_usuario",
  "password": "minha_senha"
}
```
✅ **Resposta de sucesso:**
```json
{
  "mensagem": "Usuário logado.",
  "dados": {
    "id": 10,
    "username": "meu_usuario",
    "email": "meu@email.com"
  }
}
```

---

# 📋 Endpoints

IMPORTANTE: `<int:pk>` refere-se ao ID do que você estiver alterando. Se estiver no endpoint de pegar listas, por exemplo, e quiser pegar os dados da lista de ID `35`, você deve alterar `<int:pk>` pelo ID da lista.
Ex: `GET /todo-api/usuario/lista/pegar/35/`

NOTA: Se você está hospedando este projeto localmente, conforme recomendado no início, acesse os endpoints usando http://127.0.0.1:8000/<endpoint>.

Por exemplo, para visualizar as listas de um usuário pelo navegador, basta acessar:
http://127.0.0.1:8000/todo-api/usuario/lista/pegar/35/.

Os métodos GET, POST, PATCH e DELETE podem ser ignorados ao acessar via navegador. No entanto, se você estiver consumindo esta API por meio de um script (como usando requests.py), essa informação pode ser útil para você.

## 🗂 Listas

### 📥 Pegar Listas de um Usuário
**Endpoint:** `GET /todo-api/usuario/lista/pegar/<int:pk>/`

📌 **Descrição:** Retorna todas as listas pertencentes a um usuário.
🔒 **Restrição:** Apenas o próprio usuário ou um superusuário pode acessar.

### 🔍 Pegar Todas as Listas com Informações Avançadas (Somente Superusuário)
**Endpoint:** `GET /todo-api/lista/pegar_listas_inteiras/`

📌 **Descrição:** Retorna todas as listas com informações adicionais.

### 📋 Pegar Todas as Listas com Informações Básicas (Somente Superusuário)
**Endpoint:** `GET /todo-api/lista/pegar_todas/`

📌 **Descrição:** Retorna todas as listas com informações básicas.

### ➕ Criar uma Nova Lista
**Endpoint:** `POST /todo-api/lista/criar/`

📩 **Corpo da requisição:**
```json
{
  "nome_lista": "Minha Nova Lista"
}
```
🔒 **Restrição:** Apenas o próprio usuário pode criar listas para si, ou um superusuário pode criar para qualquer usuário.

### ❌ Deletar uma Lista
**Endpoint:** `DELETE /todo-api/lista/deletar/<int:pk>/`

🔒 **Restrição:** Apenas o criador da lista ou um superusuário pode deletá-la.
✅ **Resposta de sucesso:**
```json
{
  "mensagem": "Lista deletada com sucesso."
}
```

---

## ✅ Entradas

### 📥 Pegar Entradas de uma Lista
**Endpoint:** `GET /todo-api/lista/entradas/pegar/<int:pk>/`

📌 **Descrição:** Retorna todas as entradas pertencentes a uma lista.

### ➕ Adicionar uma Entrada
**Endpoint:** `POST /todo-api/entrada/criar/<int:pk>` 

Obs: `<int:pk>` deve ser substituido pelo ID da lista que você deseja atrelar essa tarefa.

📩 **Corpo da requisição:**
```json
{
  "nome_entrada": "Minha nova tarefa",
  "estado": "P", # Os estados devem ser P (Pendente), EP (Em Progresso) e C (Concluído). Colocar qualquer coisa além disso nesse campo resultara em erro.
}
```
🔒 **Restrição:** Apenas o dono da lista e superusuários podem adicionar entradas.

### ✏️ Atualizar uma Entrada
**Endpoint:** `PATCH /todo-api/entrada/atualizar/<int:pk>/`

📩 **Corpo da requisição:**
```json
{
  "estado": "C"
}
```
🔒 **Restrição:** Apenas o dono da lista e superusuários podem atualizar entradas.

### ❌ Deletar uma Entrada
**Endpoint:** `DELETE /todo-api/entrada/deletar/<int:pk>/`

🔒 **Restrição:** Apenas o dono da lista e superusuários podem deletar entradas.
✅ **Resposta de sucesso:**
```json
{
  "mensagem": "Entrada deletada com sucesso."
}
```

---

## 🛠 Banco de Dados
Para visualizar o banco de dados, basta acessar o arquivo `db.sqlite3` dentro da pasta do projeto.

Se preferir uma interface gráfica, você pode utilizar o painel administrativo do Django. Para acessá-lo:

1. Crie um superusuário caso ainda não tenha feito:

```bash
python manage.py createsuperuser
```

2. Rode o servidor e acesse:

```
http://127.0.0.1:8000/admin/
```

3. Faça login com as credenciais do superusuário e gerencie os dados diretamente pelo painel.

---

🚀 **Pronto! Agora você já sabe como utilizar essa API. Qualquer dúvida, sinta-se à vontade para explorar o código e fazer melhorias!**

