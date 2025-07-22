# Iara Flow BFF - Backend para Frontend

Este repositório contém o backend para frontend (BFF) do Iara Flow, um agente de modelos construído com LangChain e banco de dados SQLite. O projeto foi modularizado para facilitar a manutenção e escalabilidade.

## 🔧 Correções Recentes (Branch: fix-optimize-backlog-generation)

### Problema Corrigido
- **Erro**: `'EnhancedMemoryService' object has no attribute 'optimize_backlog_generation'`
- **Causa**: Método `optimize_backlog_generation` estava sendo chamado no `ReviewAgentService` mas não estava implementado na classe `EnhancedMemoryService`
- **Solução**: Implementado o método faltante com funcionalidades completas de otimização de backlog

### Implementações Adicionadas
1. **`optimize_backlog_generation()`**: Método principal que otimiza a geração de backlog baseado na memória de longo prazo
2. **`_calculate_priority_adjustments()`**: Calcula ajustes de prioridade baseados em padrões e tendências
3. **`_identify_focus_areas()`**: Identifica áreas de foco baseadas em problemas frequentes e tendências negativas

### Funcionalidades do Método
- Análise de padrões de otimização aprendidos
- Identificação de soluções efetivas para problemas similares
- Análise de tendências de sentimento
- Ajustes automáticos de prioridade
- Recomendação de áreas de foco

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
│       ├── review_agent_routes.py # Rotas relacionadas ao agente de revisão
│       └── data_analysis_routes.py # Rotas de análise de dados
├── models/                   # Definições de modelos de dados
│   ├── __init__.py
│   ├── flow.py
│   └── review_models.py
└── services/                 # Lógica de negócio e serviços
    ├── __init__.py
    ├── langchain_agent_service.py
    ├── memory_service.py
    ├── enhanced_memory_service.py  # ✅ CORRIGIDO
    ├── review_agent_service.py
    ├── backlog_generator_service.py
    ├── sentiment_analysis_service.py
    └── ... (outros serviços)
```

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.11+
- `pip` (gerenciador de pacotes Python)

### Instalação e Execução
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/cledsondevs/iara-flow-bff.git
   cd iara-flow-bff
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente** (crie um arquivo `.env`):
   ```env
   SECRET_KEY=sua_chave_secreta_aqui
   DB_PATH=./iara_flow.db
   OPENAI_API_KEY=sua_chave_openai_aqui
   GEMINI_API_KEY=sua_chave_gemini_aqui
   FLASK_ENV=development
   PORT=5000
   DEBUG=true
   ```

4. **Execute a aplicação**:
   ```bash
   python app/main.py
   ```

5. **Acesse a aplicação**:
   - URL: `http://localhost:5000`
   - Health Check: `http://localhost:5000/` (deve retornar `{"status": "ok", "message": "Iara Flow BFF is running"}`)

### 🧪 Testando o Endpoint Corrigido

O endpoint que estava com erro agora funciona corretamente:

```bash
# Teste do endpoint de geração de backlog
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"days": 7}' \
  http://localhost:5000/api/review-agent/apps/com.tau.investimentos/backlog
```

**Resposta esperada**: JSON com backlog gerado e otimizações aplicadas.

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

### 6. Sistema de Memória Aprimorado ✅
- **Enhanced Memory Service**: Serviço de memória com funcionalidades avançadas para análise de reviews
- **Otimização de Backlog**: Algoritmos inteligentes para priorização e otimização de itens de backlog
- **Análise de Tendências**: Monitoramento de tendências de sentimento ao longo do tempo

## 📋 Endpoints Principais

### Autenticação
- `POST /api/auth/register` - Registro de usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/verify` - Verificação de sessão
- `GET /api/auth/users` - Listar usuários

### Review Agent
- `GET /api/review-agent/health` - Health check do agente
- `POST /api/review-agent/apps/<package_name>/backlog` - ✅ **CORRIGIDO** - Gerar backlog
- `POST /api/review-agent/apps/<package_name>/analyze` - Analisar sentimento
- `GET /api/review-agent/apps/<package_name>/dashboard` - Dashboard do app

## Testes Realizados

Durante o desenvolvimento e correções, os seguintes endpoints foram testados:
- ✅ **Health Check**: `GET /`
- ✅ **Registro de Usuário**: `POST /api/auth/register`
- ✅ **Login de Usuário**: `POST /api/auth/login`
- ✅ **Verificação de Sessão**: `POST /api/auth/verify`
- ✅ **Obtenção de Informações do Usuário**: `GET /api/auth/user/{id}`
- ✅ **Listagem de Usuários**: `GET /api/auth/users`
- ✅ **Geração de Backlog**: `POST /api/review-agent/apps/<package_name>/backlog` **[CORRIGIDO]**

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

## 🔄 Histórico de Branches

- **`main`**: Branch principal com código estável
- **`fix-optimize-backlog-generation`**: ✅ **NOVA BRANCH** - Correção do método `optimize_backlog_generation`

## Próximos Passos Sugeridos

1. **Testes Unitários Abrangentes**: Implementar testes unitários mais detalhados para cada módulo e função.
2. **Documentação da API (Swagger/OpenAPI)**: Gerar uma documentação interativa da API para facilitar o consumo por outros serviços ou frontends.
3. **Sistema de Logging Estruturado**: Implementar um sistema de logging mais robusto para monitoramento e depuração em produção.
4. **Validação de Dados**: Utilizar bibliotecas como `Marshmallow` ou `Pydantic` para validação de dados de entrada e saída.
5. **Cache**: Implementar estratégias de cache para melhorar a performance de endpoints frequentemente acessados.
6. **Monitoramento**: Adicionar métricas e health checks avançados para monitorar a saúde da aplicação em tempo real.

## Contribuição

Sinta-se à vontade para contribuir com o projeto! Para isso:

1. Crie uma nova branch a partir da branch principal.
2. Faça suas alterações e adicione novos testes, se aplicável.
3. Teste suas alterações localmente.
4. Crie um Pull Request descrevendo suas modificações.

---

**Última atualização**: 22/07/2025 - Correção do método `optimize_backlog_generation`


