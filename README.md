## Iara Flow BFF - Backend para Frontend

Este repositório contém o backend para frontend (BFF) do Iara Flow, um agente de modelos construído com LangChain e banco de dados SQLite. O projeto foi modularizado para facilitar a manutenção e escalabilidade.

## Estrutura do Projeto

A estrutura do projeto foi organizada de forma modular, separando as responsabilidades em diretórios claros:

```
app/
├── __init__.py
├── main.py                    # Aplicação principal Flask
├── config/
│   ├── __init__.py
│   └── settings.py           # Configurações centralizadas da aplicação
├── utils/
│   ├── __init__.py
│   └── database.py           # Utilitários para conexão e inicialização do banco de dados
├── auth/
│   ├── __init__.py
│   ├── routes.py             # Rotas de autenticação (registro, login, logout, verificação, usuários)
│   └── middleware.py         # Middleware de autenticação para proteção de rotas
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── agent_routes.py   # Rotas relacionadas ao agente de IA
│       └── review_agent_routes.py # Rotas relacionadas ao agente de revisão
├── models/                   # Definições de modelos de dados
│   ├── __init__.py
│   ├── flow.py
│   └── review_models.py
└── services/                 # Lógica de negócio e serviços
    ├── __init__.py
    ├── langchain_agent_service.py
    ├── memory_service.py
    ├── review_agent_service.py
    └── ... (outros serviços)
```

## Principais Melhorias e Funcionalidades

### 1. Estrutura Modularizada
- **Separação de Responsabilidades**: Cada módulo tem uma função específica, tornando o código mais organizado e fácil de entender.
- **Manutenção e Escalabilidade**: A nova estrutura facilita a adição de novas funcionalidades e a manutenção do código existente.

### 2. Configurações Centralizadas
- O arquivo `app/config/settings.py` centraliza todas as configurações da aplicação, incluindo chaves secretas, caminhos de banco de dados e configurações de ambiente (desenvolvimento/produção).

### 3. Sistema de Autenticação Completo e Corrigido
- **Rotas de Autenticação**: Inclui rotas para registro (`/api/auth/register`), login (`/api/auth/login`), logout (`/api/auth/logout`), verificação de sessão (`/api/auth/verify`) e obtenção de informações de usuário (`/api/auth/user/<id>`).
- **Correção do Erro 405**: O problema de acesso às rotas de autenticação (erro 405) foi resolvido garantindo que o `auth_bp` (Blueprint de autenticação) seja corretamente registrado na aplicação principal.
- **Middleware de Autenticação**: Rotas sensíveis são protegidas por um middleware (`@require_auth`) que verifica a validade do token de sessão.

### 4. API para Listar Usuários
- **Nova Rota**: Adicionada a rota `GET /api/auth/users` que permite listar todos os usuários cadastrados no banco de dados.
- **Proteção**: Esta rota é protegida por autenticação, exigindo um token de sessão válido.

### 5. Utilitários de Banco de Dados
- Funções centralizadas em `app/utils/database.py` para gerenciar a conexão com o SQLite e inicializar as tabelas necessárias.

## Como Executar

### Pré-requisitos
- Python 3.x
- `pip` (gerenciador de pacotes Python)

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/cledsondevs/iara-flow-bff.git
   cd iara-flow-bff
   ```
2. Instale as dependências:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (exemplo):
   ```
   SECRET_KEY=sua_chave_secreta_aqui
   DB_PATH=./iara_flow.db
   OPENAI_API_KEY=sua_chave_openai_aqui
   FLASK_ENV=development
   PORT=5000
   ```

### Rodando a Aplicação
Para iniciar o servidor Flask:
```bash
python3 app/main.py
```

A aplicação estará disponível em `http://localhost:5000` (ou na porta configurada no `.env`).

### Testes da API
Para executar os testes automatizados da API (incluindo a nova rota de listagem de usuários):
```bash
python3 test_api.py
```

## Testes Realizados

Durante o desenvolvimento e modularização, os seguintes endpoints foram testados:
- ✅ **Health Check**: `GET /`
- ✅ **Registro de Usuário**: `POST /api/auth/register`
- ✅ **Login de Usuário**: `POST /api/auth/login`
- ✅ **Verificação de Sessão**: `POST /api/auth/verify`
- ✅ **Obtenção de Informações do Usuário**: `GET /api/auth/user/{id}`
- ✅ **Listagem de Usuários**: `GET /api/auth/users`

### Usuário de Teste Padrão
Um usuário de teste é criado/utilizado nos testes automatizados:
- **Username**: `usuario_teste`
- **Password**: `senha123`
- **Email**: `teste@exemplo.com`

## Deploy em Servidor (Gunicorn/Systemd)

Para deploy em um servidor de produção utilizando Gunicorn e Systemd, certifique-se de que:

1. **`wsgi.py` está configurado corretamente**: O arquivo `wsgi.py` deve apontar para a instância da aplicação Flask em `app.main:create_app()`.
   Exemplo de `wsgi.py`:
   ```python
   import sys
   import os

   sys.path.insert(0, os.path.dirname(__file__))

   from app.main import create_app

   application = create_app()
   ```

2. **Serviço Systemd aponta para o `wsgi:application`**: A configuração do seu serviço `.service` (ex: `/etc/systemd/system/iara-flow-bff.service`) deve ter a linha `ExecStart` apontando para `wsgi:application`.
   Exemplo de `ExecStart`:
   ```
   ExecStart=/caminho/para/seu/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:application
   ```

3. **Recarregue e Reinicie o Serviço**: Após qualquer alteração nos arquivos de configuração ou código, execute:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart iara-flow-bff
   ```

## Próximos Passos Sugeridos

1. **Testes Unitários Abrangentes**: Implementar testes unitários mais detalhados para cada módulo e função.
2. **Documentação da API (Swagger/OpenAPI)**: Gerar uma documentação interativa da API para facilitar o consumo por outros serviços ou frontends.
3. **Sistema de Logging Estruturado**: Implementar um sistema de logging mais robusto para monitoramento e depuração em produção.
4. **Validação de Dados**: Utilizar bibliotecas como `Marshmallow` ou `Pydantic` para validação de dados de entrada e saída.
5. **Cache**: Implementar estratégias de cache para melhorar a performance de endpoints frequentemente acessados.
6. **Monitoramento**: Adicionar métricas e health checks avançados para monitorar a saúde da aplicação em tempo real.

## Contribuição

Sinta-se à vontade para contribuir com o projeto! Para isso:

1. Crie uma nova branch a partir da branch principal (ou da branch `feature/modularizacao-backend` se estiver trabalhando nela).
2. Faça suas alterações e adicione novos testes, se aplicável.
3. Teste suas alterações localmente.
4. Crie um Pull Request descrevendo suas modificações.


