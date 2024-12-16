# CodeLeap Network - Backend Social Media Platform

## Descrição do Projeto
Este é um projeto de backend para uma plataforma de rede social, desenvolvido com Django Rest Framework, utilizando Docker para containerização e PostgreSQL como banco de dados.
Além das funcionalidades solicitadas, implementei algumas melhorias que, na minha visão, podem agregar valor ao sistema e proporcionar uma experiência mais completa.
Caso tenha ficado alguma dúvida posso explicar melhor em uma reunião.

## Tecnologias Utilizadas
- Python 3.12.7
- Django 5.1.2
- Django Rest Framework 3.15.2
- PostgreSQL 16
- Docker
- Gunicorn

## Pré-requisitos
- Docker
- Docker Compose
- Git

## Configuração do Projeto

### Clonar o Repositório
```bash
git clone https://github.com/jonatasolialmeida/TESTE_CODE.git
```

### Configuração do Ambiente

1. Criar arquivo de variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do Django
SECRET_KEY=sua_secret_key_aqui
DEBUG=False

# Configurações do Banco de Dados
POSTGRES_USER=testecodeleap
POSTGRES_PASSWORD=testecodeleap
POSTGRES_HOST=db
POSTGRES_PORT=5432  
POSTGRES_DB=TESTECODELEAP

ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:80,http://localhost,http://127.0.0.1
```
### Criar Ambiente Virtual (Recomendo criar para instalar as dependências do projeto após ativar a venv)

```bash
# Na pasta backend
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows

# Instalar dependências
pip install -r requirements.txt
```

### Instalação e Inicialização

#### Usando Docker

1. Construir e iniciar os containers:
```bash
docker-compose up --build
```

2. Executar migrações:
```bash
# Em outro terminal
# Criar migrações
docker-compose exec backend python manage.py makemigrations

# Aplicar migrações no banco de dados
docker-compose exec backend python manage.py migrate
```

3. Criar superusuário para acesso ao admin:
```bash
docker-compose exec backend python manage.py createsuperuser
```
   - Siga as instruções interativas para criar o superusuário
   - Informe username, email (opcional) e senha

### Acessando a Interface de Administração

1. Inicie o servidor Docker
2. Acesse: `http://127.0.0.1:8000/admin/`
3. Faça login com o superusuário criado

#### Criando Usuários e Tokens

Na interface de administração:

1. Vá para "Users"
2. Clique em "ADD USER +" no canto superior direito
3. Preencha o formulário de criação de usuário
4. Após salvar, você pode:
   - Definir permissões
   - Redefinir senhas

#### Gerando Tokens de Autenticação

1. Na interface admin, vá para "Tokens"
2. Clique em "ADD TOKEN +"
3. Selecione o usuário
4. Salve para gerar o token

## Endpoints da API

### Autenticação
- Todos os endpoints requerem autenticação via Token

### Posts
- `GET /api/social-posts/`: Listar todos os posts ativos
  - Retorna uma lista paginada de posts
  - Cada post inclui: id, título, conteúdo, autor, data de criação
- `GET /api/social-posts/<id>/`: Detalhes de um post específico
- `POST /api/social-posts/`: Criar novo post
- `PATCH /api/social-posts/<id>/`: Atualizar post
- `DELETE /api/social-posts/<id>/`: Deletar post

### Comentários
- `POST /api/social-posts/<id>/comment/`: Comentar em um post
#### Irei implementar a funcionalidade abaixo
- `GET /api/social-posts/<id>/comments/`: Listar comentários de um post específico
  - Retorna todos os comentários associados ao post


### Notificações
- `GET /api/notifications/`: Listar notificações não lidas do usuário autenticado

## Testes

Para executar os testes:
```bash
docker-compose exec backend python manage.py test
```

## Estrutura do Projeto
```
.
├── backend
│   ├── Dockerfile
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── admin.cpython-312.pyc
│   │   │   ├── apps.cpython-312.pyc
│   │   │   ├── models.cpython-312.pyc
│   │   │   └── urls.cpython-312.pyc
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   │       ├── 0001_initial.cpython-312.pyc
│   │   │       ├── 0002_alter_notification_options_post_title.cpython-312.pyc
│   │   │       └── __init__.cpython-312.pyc
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-312.pyc
│   │   │   │   └── serializers.cpython-312.pyc
│   │   │   └── serializers.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-312.pyc
│   │   │   │   └── services.cpython-312.pyc
│   │   │   └── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   └── views.cpython-312.pyc
│   │       └── views.py
│   ├── codeleap_network
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── settings.cpython-312.pyc
│   │   │   ├── urls.cpython-312.pyc
│   │   │   └── wsgi.cpython-312.pyc
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── readme.md
└── test.rest
```

## Contribuição
1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Contato
```
Caso tenha dúvidas de como rodar o projeto, não hesite em me contactar
Jonatas Almeida - jonatas.olialmeida@gmail.com
https://www.linkedin.com/in/jônatas-almeida-24933a26/
```
