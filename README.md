# 📌 To-Do API Documentation

💡 NOTA: Abaixo está uma pequena introdução de como mexer nessa API. Note que ela não está hosteada, então recomendo hosteá-la localmente. Basta rodar o ambiente virtual e dar um ```python manage.py runserver ``` e clicar no link gerado.


Além disso, <b>a documentação que você vai ler abaixo foi escrita por mim</b>, porém EMBELEZADA por inteligência artificial, pois não estava totalmente satisfeito com a forma bruta dessa documentação. Sinta-se a vontade para fazer o que quiser com isso aqui!

## 📖 Introdução

Esta é uma API para gerenciamento de listas e entradas de tarefas. Para utilizá-la, é necessário estar autenticado.

- **Usuários comuns** podem gerenciar apenas suas próprias listas e entradas.
- **Superusuário** tem acesso irrestrito.

### 🛠 Superusuário Padrão

```plaintext
Username: Admin
Password: admin123
ID no banco de dados: 9
```

> **Nota:** Qualquer um pode acessar a API com este superusuário, que possui permissão para todas as operações.

---

## 🔑 Autenticação

Antes de qualquer operação, é necessário estar autenticado. Você pode **registrar um novo usuário** ou **fazer login** com um existente.

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

## 🗂 Listas

### 📥 Pegar Listas de um Usuário
**Endpoint:** `GET /todo-api/usuario/lista/pegar/<int:pk>/`

📌 **Descrição:** Retorna todas as listas pertencentes a um usuário.

🔒 **Restrição:** Apenas o próprio usuário ou um superusuário pode acessar.

### 🔍 Pegar Todas as Listas com Informações Avançadas *(Somente Superusuário)*
**Endpoint:** `GET /todo-api/lista/pegar_listas_inteiras/`

📌 **Descrição:** Retorna todas as listas com informações adicionais.

### 📋 Pegar Todas as Listas com Informações Básicas *(Somente Superusuário)*
**Endpoint:** `GET /todo-api/lista/pegar_todas/`

📌 **Descrição:** Retorna todas as listas com informações básicas.

### ➕ Criar uma Nova Lista
**Endpoint:** `POST /todo-api/lista/criar/`

📩 **Corpo da requisição:**
```json
{
  "nome_lista": "Minha Nova Lista",
  "usuario": 10
}
```
🔒 **Restrição:** Apenas o próprio usuário pode criar listas para si, ou um superusuario.

### ❌ Deletar uma Lista
**Endpoint:** `POST /todo-api/lista/deletar/`

📩 **Corpo da requisição:**
```json
{
  "id": 5
}
```
🔒 **Restrição:** Apenas o criador da lista ou um superusuário pode deletá-la.

---

## ✅ Entradas

### 📥 Pegar Entradas de uma Lista
**Endpoint:** `GET /todo-api/lista/entradas/pegar/<int:pk>/`

📌 **Descrição:** Retorna todas as entradas pertencentes a uma lista.

### ➕ Adicionar uma Entrada
**Endpoint:** `POST /todo-api/entrada/criar/`

📩 **Corpo da requisição:**
```json
{
  "nome_entrada": "Minha nova tarefa",
  "estado": "P",
  "lista_origem": 3
}
```
🔒 **Restrição:** Apenas o dono da lista e superusuarios podem deletar entradas.

### ✏️ Atualizar uma Entrada
**Endpoint:** `PATCH /todo-api/entrada/atualizar/`

📩 **Corpo da requisição:**
```json
{
  "id": 8,
  "estado": "C"
}
```
🔒 **Restrição:** Apenas o dono da lista e superusuarios podem deletar entradas.

### ❌ Deletar uma Entrada
**Endpoint:** `POST /todo-api/entrada/deletar/`

📩 **Corpo da requisição:**
```json
{
  "id": 15
}
```
🔒 **Restrição:** Apenas o dono da lista e superusuarios podem deletar entradas.

---


