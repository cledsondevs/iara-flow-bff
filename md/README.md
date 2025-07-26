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

## 📊 Funcionalidade de Dashboards Gerenciais

Uma nova funcionalidade de dashboards gerenciais foi adicionada, permitindo a visualização personalizada dos dados do backlog.

### Geração de Dashboards

Os dashboards podem ser gerados de duas formas:

1.  **Automaticamente com a Geração de Backlog**:
    Ao chamar o endpoint de geração de backlog, um dashboard será criado automaticamente se a flag `generate_dashboard` for `True` (padrão).

    ```bash
    curl -X POST \
      -H "Content-Type: application/json" \
      -d '{"package_name": "com.example.app", "days": 7, "generate_dashboard": true}' \
      http://localhost:5000/api/review-agent/apps/com.example.app/backlog
    ```

    A resposta incluirá um campo `dashboard` com a `custom_url` para acesso.

2.  **Via Endpoint Dedicado**:
    Você pode gerar um dashboard diretamente, fornecendo os dados do backlog (ou deixando o backend gerá-los).
    ```bash
    curl -X POST \
      -H "Content-Type: application/json" \
      -d '{"package_name": "com.example.app", "days": 7, "user_id": "user123", "session_id": "session456"}' \
      http://localhost:5000/api/dashboard/generate
    ```

### Visualização de Dashboards

Para visualizar um dashboard, acesse a URL personalizada gerada:

```
http://localhost:5000/api/dashboard/{custom_url}
```

Exemplo:

```
http://localhost:5000/api/dashboard/dashboard-com-example-test-202507220801-d944f9a4-150d28ee
```

### Endpoints de Dashboard

- `POST /api/dashboard/generate` - Gerar um novo dashboard.
- `GET /api/dashboard/{custom_url}` - Visualizar um dashboard específico.
- `GET /api/dashboard/list` - Listar todos os dashboards criados.
- `GET /api/dashboard/stats` - Obter estatísticas gerais sobre os dashboards.
- `POST /api/dashboard/preview` - Gerar um preview de dashboard sem salvá-lo.
- `DELETE /api/dashboard/{dashboard_id}` - Deletar um dashboard (soft delete).
- `POST /api/dashboard/cleanup` - Limpar dashboards expirados.

### Frontend de Visualização (React)

Para uma experiência de visualização mais rica, você pode usar o frontend React desenvolvido para consumir esses dashboards. Ele está disponível em outro repositório:

[https://github.com/cledsondevs/iara-flow-prototyper](https://github.com/cledsondevs/iara-flow-prototyper)

**Como executar o frontend (após clonar o repositório `iara-flow-prototyper`):**

1.  **Instale as dependências**:

    ```bash
    cd iara-flow-prototyper
    pnpm install
    ```

2.  **Inicie o servidor de desenvolvimento**:

    ```bash
    pnpm run dev --host 0.0.0.0
    ```

3.  **Acesse no navegador**:
    Normalmente em `http://localhost:5173` ou outra porta disponível.

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

### Dashboards Gerenciais

- `POST /api/dashboard/generate` - Gerar um novo dashboard. Exemplo de uso:
  ```bash
  curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"package_name": "com.example.app", "days": 7, "user_id": "user123", "session_id": "session456"}' \
    http://localhost:5000/api/dashboard/generate
  ```
- `GET /api/dashboard/{custom_url}` - Visualizar um dashboard específico. Exemplo de uso:
  ```bash
  curl http://localhost:5000/api/dashboard/dashboard-com-example-test-202507220801-d944f9a4-150d28ee
  ```
- `GET /api/dashboard/list` - Listar todos os dashboards criados. Exemplo de uso:
  ```bash
  curl http://localhost:5000/api/dashboard/list?package_name=com.example.app
  ```
- `GET /api/dashboard/stats` - Obter estatísticas gerais sobre os dashboards. Exemplo de uso:
  ```bash
  curl http://localhost:5000/api/dashboard/stats
  ```
- `POST /api/dashboard/preview` - Gerar um preview de dashboard sem salvá-lo. Exemplo de uso:
  ```bash
  curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"package_name": "com.example.app", "days": 7}' \
    http://localhost:5000/api/dashboard/preview
  ```
- `DELETE /api/dashboard/{dashboard_id}` - Deletar um dashboard (soft delete). Exemplo de uso:
  ```bash
  curl -X DELETE http://localhost:5000/api/dashboard/SEU_DASHBOARD_ID
  ```
- `POST /api/dashboard/cleanup` - Limpar dashboards expirados. Exemplo de uso:
  ```bash
  curl -X POST http://localhost:5000/api/dashboard/cleanup
  ```

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

1.  **`wsgi.py` está configurado corretamente**: O arquivo `wsgi.py` deve apontar para a instância da aplicação Flask em `app.main:create_app()`.
    Exemplo de `wsgi.py`:

    ```python
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from app.main import create_app

    application = create_app()
    ```

2.  **Serviço Systemd aponta para o `wsgi:application`**: A configuração do seu serviço `.service` (ex: `/etc/systemd/system/iara-flow-bff.service`) deve ter a linha `ExecStart` apontando para `wsgi:application`.
    Exemplo de `ExecStart`:

    ```
    ExecStart=/caminho/para/seu/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:application
    ```

3.  **Recarregue e Reinicie o Serviço**: Após qualquer alteração nos arquivos de configuração ou código, execute:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart iara-flow-bff
    ```

## 🔄 Histórico de Branches

- **`main`**: Branch principal com código estável
- **`fix-optimize-backlog-generation`**: ✅ **NOVA BRANCH** - Correção do método `optimize_backlog_generation`
- **`feat-dashboard-integration`**: ✅ **NOVA BRANCH** - Adição da funcionalidade de dashboards gerenciais

## Próximos Passos Sugeridos

1.  **Testes Unitários Abrangentes**: Implementar testes unitários mais detalhados para cada módulo e função.
2.  **Documentação da API (Swagger/OpenAPI)**: Gerar uma documentação interativa da API para facilitar o consumo por outros serviços ou frontends.
3.  **Sistema de Logging Estruturado**: Implementar um sistema de logging mais robusto para monitoramento e depuração em produção.
4.  **Validação de Dados**: Utilizar bibliotecas como `Marshmallow` ou `Pydantic` para validação de dados de entrada e saída.
5.  **Cache**: Implementar estratégias de cache para melhorar a performance de endpoints frequentemente acessados.
6.  **Monitoramento**: Adicionar métricas e health checks avançados para monitorar a saúde da aplicação em tempo real.

## Contribuição

Sinta-se à vontade para contribuir com o projeto! Para isso:

1.  Crie uma nova branch a partir da branch principal.
2.  Faça suas alterações e adicione novos testes, se aplicável.
3.  Teste suas alterações localmente.
4.  Crie um Pull Request descrevendo suas modificações.

---

**Última atualização**: 22/07/2025 - Correção do método `optimize_backlog_generation` e Adição da funcionalidade de Dashboards Gerenciais

## 🧠 Funcionalidade de Memória do Agente (Gemini)

O backend agora suporta um sistema de memória para os agentes conversacionais, permitindo que eles mantenham o contexto da conversa ao longo do tempo. Isso é crucial para interações mais naturais e coerentes.

### Como Funciona

1.  **`user_id`**: Cada usuário é identificado por um `user_id` único. Este ID é usado para associar o histórico de conversas a um usuário específico.
2.  **`session_id`**: Dentro de cada interação do usuário, um `session_id` é utilizado para agrupar mensagens que fazem parte da mesma sessão de conversa.
3.  **Persistência**: O histórico da conversa (mensagens do usuário e respostas do agente) é salvo no banco de dados (SQLite) associado ao `user_id` e `session_id`.
4.  **Recuperação**: Antes de processar uma nova mensagem, o agente recupera o histórico recente da conversa usando o `user_id` e `session_id` fornecidos. Isso permite que o modelo de linguagem (ex: Gemini) tenha acesso ao contexto anterior para gerar respostas relevantes.

### Benefícios

- **Coerência da Conversa**: O agente se lembra do que foi dito anteriormente, evitando repetições e fornecendo respostas mais precisas.
- **Personalização**: A interação se torna mais personalizada, pois o agente tem conhecimento do histórico individual de cada usuário.
- **Continuidade**: Permite que as conversas sejam retomadas de onde pararam, mesmo após um período de inatividade ou em sessões diferentes.

### Implementação

A lógica de persistência e recuperação da memória está implementada principalmente nos serviços `memory_service.py` e `gemini_agent_service.py`.

Ao chamar o endpoint `/gemini/chat`, certifique-se de fornecer o `user_id` e, opcionalmente, o `session_id` para garantir que o histórico seja corretamente gerenciado:

````json
{
  "message": "Olá, tudo bem?",
  "user_id": "seu_user_id_aqui",
  "session_id": "seu_session_id_aqui",
  "api_key": "sua_chave_api_gemini_aqui"
}


## 🧠 Como o LangChain Aprende Através de Conversas

O coração de qualquer agente de IA conversacional eficaz reside na sua capacidade de "lembrar" o que foi dito anteriormente. Sem essa funcionalidade, cada interação seria um novo começo, resultando em respostas genéricas, repetitivas e, em última análise, uma experiência de usuário frustrante. No Iara Flow BFF, utilizamos o framework LangChain em conjunto com um serviço de memória persistente baseado em SQLite para dotar nossos agentes com essa capacidade crucial de aprendizado e contextualização.

### O Conceito de Memória no LangChain

No ecossistema LangChain, a memória é o componente responsável por preservar o estado de uma conversa. Isso permite que os Large Language Models (LLMs) como o Gemini, que são inerentemente "sem estado" (ou seja, não retêm informações de interações passadas por padrão), possam acessar o histórico da conversa e gerar respostas que são contextualmente relevantes. Existem diversos tipos de memória no LangChain, desde buffers simples que armazenam as últimas N interações até memórias mais complexas que utilizam embeddings para recuperar informações semanticamente similares.

No nosso projeto, a implementação da memória é realizada através do `MemoryService`, que atua como uma camada de abstração sobre o banco de dados SQLite. Cada turno da conversa (mensagem do usuário e resposta do agente) é salvo de forma estruturada, permitindo que o agente recupere esse histórico quando necessário.

### Mecanismo de Aprendizado e Contextualização

O processo pelo qual o LangChain "aprende" e mantém o contexto das conversas no Iara Flow BFF pode ser detalhado em algumas etapas:

1.  **Captura da Interação**: Sempre que um usuário envia uma mensagem para o agente de IA, e o agente gera uma resposta, essa dupla (mensagem do usuário, resposta do agente) é capturada pelo sistema.

2.  **Persistência no SQLite**: O `MemoryService` é invocado para salvar essa interação no banco de dados SQLite. Cada registro inclui o `user_id` (identificador único do usuário), o `session_id` (identificador da sessão de conversa atual), a mensagem do usuário, a resposta do agente, e um timestamp. A inclusão do `session_id` é fundamental, pois permite que um mesmo usuário tenha múltiplas conversas independentes, ou que uma conversa seja retomada em diferentes momentos, mantendo seu próprio contexto.

3.  **Recuperação do Histórico**: Antes de processar uma nova mensagem do usuário, o `LangChainAgentService` consulta o `MemoryService` para recuperar o histórico de conversas relevante. Essa recuperação é feita com base no `user_id` e no `session_id` fornecidos na requisição. Por padrão, um número limitado de interações mais recentes é recuperado para manter a relevância e evitar sobrecarga do contexto.

4.  **Injeção de Contexto no LLM**: O histórico de conversas recuperado é então formatado de uma maneira que o modelo de linguagem (LLM) entenda. No caso do LangChain, isso geralmente envolve a conversão das mensagens em objetos `HumanMessage` e `AIMessage`, que representam as falas do usuário e do assistente, respectivamente. Esse histórico formatado é passado como parte do prompt para o LLM. É como se o agente estivesse lendo as últimas páginas de um livro antes de continuar a história.

5.  **Geração de Resposta Contextualizada**: Com o histórico da conversa em mãos, o LLM é capaz de gerar uma resposta que não apenas aborda a mensagem atual do usuário, mas também leva em consideração o que foi discutido anteriormente. Isso resulta em interações mais fluidas, naturais e inteligentes, onde o agente demonstra compreensão do fluxo da conversa.

### Importância da Memória

A memória é vital para:

*   **Coerência e Continuidade**: Garante que o agente mantenha o fio da meada, evitando que ele se contradiga ou peça informações já fornecidas.
*   **Personalização**: Permite que o agente adapte suas respostas com base nas preferências ou informações previamente compartilhadas pelo usuário.
*   **Eficiência**: Reduz a necessidade de o usuário repetir informações, tornando a interação mais eficiente e menos cansativa.
*   **Experiência do Usuário Aprimorada**: Transforma um chatbot simples em um assistente verdadeiramente conversacional, capaz de engajar em diálogos complexos e de longo prazo.

Em resumo, a funcionalidade de memória implementada no Iara Flow BFF é a espinha dorsal para a criação de agentes de IA que não apenas respondem, mas realmente interagem e aprendem com cada conversa, proporcionando uma experiência de usuário superior.



## 🧹 Como Limpar o Histórico de Conversas via API

Manter o histórico de conversas é essencial para a coerência e personalização das interações com o agente de IA. No entanto, em certos cenários, pode ser necessário limpar esse histórico. Isso pode ser útil para iniciar uma nova conversa do zero, para fins de privacidade, ou para depuração. O Iara Flow BFF oferece um endpoint específico para gerenciar a limpeza da memória do agente.

### Endpoint de Limpeza de Memória

O método `clear_memory` no `LangChainAgentService` é responsável por orquestrar a limpeza do histórico de conversas. Ele utiliza o `MemoryService` para interagir diretamente com o banco de dados SQLite e remover os registros de conversa.

Você pode limpar o histórico de conversas de um usuário ou de uma sessão específica através do seguinte endpoint:

*   **`POST /api/gemini/clear-memory`**

Este endpoint aceita um corpo de requisição JSON com os seguintes parâmetros:

*   **`user_id`** (obrigatório): O identificador único do usuário cujo histórico de conversas será limpo.
*   **`session_id`** (opcional): O identificador da sessão específica a ser limpa. Se este parâmetro for fornecido, apenas o histórico daquela sessão para o `user_id` especificado será removido. Se `session_id` não for fornecido, **todo o histórico de conversas** para o `user_id` será limpo.

### Exemplos de Uso

#### 1. Limpar o histórico de uma sessão específica

Para limpar apenas o histórico de uma sessão de conversa específica para um determinado usuário, inclua ambos `user_id` e `session_id` na sua requisição:

```json
{
  "user_id": "seu_user_id_aqui",
  "session_id": "seu_session_id_aqui"
}
````

**Exemplo de `curl`:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usuario123", "session_id": "sessaoABC"}' \
  http://localhost:5000/api/gemini/clear-memory
```

#### 2. Limpar todo o histórico de um usuário

Para limpar todo o histórico de conversas de um usuário (todas as sessões associadas a ele), forneça apenas o `user_id` na sua requisição:

```json
{
  "user_id": "seu_user_id_aqui"
}
```

**Exemplo de `curl`:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usuario123"}' \
  http://localhost:5000/api/gemini/clear-memory
```

### Considerações Importantes

- **Irreversibilidade**: A limpeza do histórico de conversas é uma operação irreversível. Uma vez que os dados são removidos do banco de dados, eles não podem ser recuperados.
- **Impacto na Coerência**: Limpar o histórico de uma sessão fará com que o agente "esqueça" o contexto anterior para aquela sessão, iniciando uma nova conversa do zero. Limpar todo o histórico de um usuário terá o mesmo efeito para todas as suas interações futuras.
- **Segurança**: Certifique-se de que o acesso a este endpoint seja devidamente protegido (por exemplo, através de autenticação e autorização) para evitar a exclusão indevida de dados de conversas.

Esta funcionalidade oferece flexibilidade para gerenciar a memória do agente de acordo com as necessidades da aplicação e as preferências do usuário, garantindo tanto a privacidade quanto a capacidade de reiniciar interações quando desejado.

```

O `session_id` pode ser gerado no frontend ou no backend, dependendo da sua estratégia de gerenciamento de sessão. Se não for fornecido, um novo `session_id` pode ser gerado ou o último `session_id` do `user_id` pode ser utilizado para continuar a conversa.

```





---

# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Sistema de Memória Isolado V2 (Persistência por Usuário)**
  - Implementação de um sistema de memória completamente novo e isolado, garantindo persistência de conversas por `user_id` (independente da `session_id`).
  - **Novas Rotas API V2 para Chat Gemini:**
    - `POST /api/v2/chat/gemini` - Chat principal com memória persistente.
    - `GET /api/v2/chat/gemini/memory` - Recupera todo o histórico de memória do usuário.
    - `DELETE /api/v2/chat/gemini/memory` - Limpa toda a memória do usuário.
    - `GET /api/v2/chat/gemini/stats` - Obtém estatísticas de uso da memória do usuário.
    - `PUT /api/v2/chat/gemini/profile` - Atualiza o perfil do usuário.
    - `POST /api/v2/chat/gemini/fact` - Salva fatos específicos sobre o usuário.
    - `GET /api/v2/chat/gemini/context` - Obtém o contexto completo da conversa do usuário.
    - `GET /api/v2/chat/health` - Health check para o serviço V2.
    - `POST /api/v2/chat/migrate` - Endpoint para futuras migrações de dados.
  - **Persistência de Histórico por `user_id`:**
    - A função `get_conversation_history_isolated` no `IsolatedMemoryService` agora busca o histórico apenas por `user_id`, ignorando a `session_id`.
    - O `GeminiChatServiceV2` foi ajustado para utilizar este histórico expandido para construir o contexto da conversa.
  - **Comandos de Memória Aprimorados:**
    - A funcionalidade "Lembre-se disso:" agora utiliza o novo sistema de memória isolado, garantindo que os fatos sejam persistidos por `user_id`.

### Removed
- **Código da Versão 1 (V1) do Sistema de Memória e Chat:**
  - `app/chats/routes/chat_routes.py` (Rotas de chat V1).
  - `app/services/memory_service.py` (Serviço de memória V1).
  - `app/services/enhanced_memory_service.py` (Serviço de memória aprimorado V1).
  - `app/chats/services/gemini_chat_service.py` (Serviço de chat Gemini V1).
  - Todas as importações e registros relacionados à V1 foram removidos do `app/main.py`.

### Fixed
- **Problemas críticos de salvamento e acesso de memórias resolvidos**
  - Corrigidos problemas de DEFAULT (lower(hex(randomblob(16)))) em todas as tabelas
  - Removidas expressões SQL incompatíveis que causavam erros de criação de tabelas
  - Corrigidos arquivos: `backlog_generator_service.py`, `dashboard_service.py`, `review_collector_service.py`
  - Sistema de memória de curto e longo prazo agora funciona corretamente
  - Conversas são salvas e recuperadas adequadamente

- **Dados padrão implementados no banco de dados**
  - Criado script `create_sample_data.py` para popular o banco com dados de exemplo
  - Inseridos 3 usuários padrão: admin, demo_user, test_user
  - Criadas 3 conversas de exemplo com sistema de memória funcionando
  - Inseridos 3 reviews de exemplo para testes
  - Banco de dados não fica mais vazio após inicialização

- **Problema crítico de bloqueio do banco de dados SQLite resolvido**
  - Implementado gerenciamento adequado de conexões usando context managers
  - Corrigidas todas as funções de autenticação para usar `with get_db_connection()`
  - Eliminados vazamentos de conexão que causavam bloqueios
  - Adicionado script `fix_database_lock.py` para diagnóstico e correção de bloqueios

- **APIs de Login totalmente funcionais**
  - Corrigidas rotas de autenticação com prefixos incorretos
  - Resolvido erro "405 METHOD NOT ALLOWED" 
  - Todas as rotas de autenticação agora funcionam corretamente:
    - `POST /api/auth/register` - Registro de usuários
    - `POST /api/auth/login` - Login de usuários  
    - `POST /api/auth/logout` - Logout de usuários
    - `POST /api/auth/verify` - Verificação de sessão
    - `GET /api/auth/user/<id>` - Obter dados do usuário

- **Sistema de configuração de chaves de API restaurado**
  - Corrigidas rotas de API keys: `POST /api/keys` e `GET /api/keys/<user_id>/<service_name>`
  - Adicionados imports necessários no arquivo `api_key_routes.py`
  - Sistema de armazenamento e recuperação de chaves funcionando

- **Tabelas de memória de longo prazo criadas corretamente**
  - Corrigida criação automática das tabelas `conversations` e `user_profiles`
  - MemoryService agora usa configuração centralizada do banco
  - Criação automática do diretório `data/` se não existir
  - Sincronização entre todos os serviços de banco de dados

- **Configuração de banco de dados unificada**
  - Unificada configuração em `Config.DATABASE_PATH`
  - Consistência entre todos os arquivos (`auth_routes.py`, `memory_service.py`, `database.py`)
  - Criação automática de diretórios em todos os pontos de acesso

- **Usuário padrão criado automaticamente**
  - Criação automática de usuário administrador na inicialização
  - **Credenciais:** `admin` / `admin` (email: `admin@iaraflow.com`)
  - Script independente `create_default_user.py` para criação manual

- **Dependências instaladas e configuradas**
  - Instaladas todas as dependências necessárias: Flask, LangChain, Google AI, etc.
  - Aplicação Flask inicializa corretamente sem erros de módulos
  - Todas as funcionalidades principais testadas e funcionando

### Technical Details
- Implementado padrão de context manager para conexões SQLite
- Eliminados bloqueios de banco através de gerenciamento adequado de recursos
- Corrigidas estruturas try/except aninhadas que causavam problemas de sintaxe
- Adicionado tratamento robusto de erros em todas as operações de banco

### Testing
- ✅ Login com usuário padrão (admin/admin) funcionando
- ✅ Registro de novos usuários funcionando  
- ✅ Verificação de sessão funcionando
- ✅ Obtenção de dados de usuário funcionando
- ✅ Configuração de chaves de API funcionando
- ✅ Recuperação de chaves de API funcionando
- ✅ Banco de dados sem bloqueios
  - Criação automática do diretório `data/` se não existir
  - Tabelas `conversations` e `user_profiles` criadas corretamente na inicialização
  - Sincronização entre `init_database()` e `MemoryService._init_sqlite_tables()`

- **Configuração de Banco de Dados**: Unificada configuração de caminho do banco
  - Todos os serviços agora usam `Config.DATABASE_PATH` ao invés de caminhos hardcoded
  - Criação automática do diretório do banco em todos os pontos de acesso
  - Consistência entre `auth_routes.py`, `memory_service.py` e `database.py`

### Added
- **Usuário Padrão**: Criação automática de usuário administrador na inicialização
  - Username: `admin`
  - Password: `admin`
  - Email: `admin@iaraflow.com`
  - Criado automaticamente se não existir durante a inicialização da aplicação
  - Script independente `create_default_user.py` para criação manual

### Changed
- **Inicialização da Aplicação**: Melhorada sequência de inicialização
  - Banco de dados inicializado primeiro
  - MemoryService inicializado em seguida
  - Usuário padrão criado automaticamente
  - Logs informativos para cada etapa da inicialização

### Technical Details
- **Arquivos modificados**:
  - `app/auth/auth_routes.py` - Corrigidas rotas e configuração de banco
  - `app/services/memory_service.py` - Unificada configuração de banco e criação de diretório
  - `app/main.py` - Adicionada criação automática de usuário padrão
  - `app/utils/database.py` - Mantida consistência na configuração

- **Arquivos criados**:
  - `create_default_user.py` - Script para criação manual de usuário padrão

### Notes
- As APIs de autenticação agora funcionam corretamente com os endpoints esperados
- O sistema de memória de longo prazo está totalmente funcional
- Usuário padrão permite acesso imediato ao sistema após instalação
- Todas as configurações de banco de dados estão centralizadas em `Config.DATABASE_PATH`

### Added
- **Memória de Longo Prazo para Chats**: Implementação de sistema de memória persistente para os endpoints de chat Gemini e OpenAI
  - Novo endpoint `/api/gemini/chat` com memória de longo prazo
  - Novo endpoint `/api/openai/chat` com memória de longo prazo
  - Endpoints para gerenciar memória: GET e DELETE para `/api/gemini/memory` e `/api/openai/memory`
  - Endpoint de verificação de saúde: `/api/chat/health`
  - Sistema de sessões para isolar conversas por usuário e sessão
  - Armazenamento persistente de conversas no banco SQLite
  - Contexto de conversa mantido entre sessões diferentes

- **Memória de Longo Prazo para LangChain Agent**: Extensão da funcionalidade de memória persistente para o agente LangChain
  - Endpoint `/api/agent/chat` agora utiliza memória de longo prazo
  - Histórico de conversas mantido entre reinicializações do servidor
  - Integração com ferramentas (web_search, file operations) preservada
  - Metadados aprimorados incluindo ferramentas utilizadas e tipo de agente

- **Suporte ao Groq Chat**: Novo provedor de IA adicionado ao sistema de chat
  - Novo endpoint `/api/groq/chat` com memória de longo prazo
  - Endpoints para gerenciar memória: GET e DELETE para `/api/groq/memory`
  - Endpoint para listar modelos disponíveis: `/api/groq/models`
  - Suporte a múltiplos modelos Groq (llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it)
  - Integração completa com sistema de memória unificado

- **Memória Global por Usuário**: Sistema de perfil persistente que transcende sessões individuais
  - Nova tabela `user_profiles` para armazenar informações globais do usuário
  - Extração automática de informações pessoais das mensagens (nome, profissão, idade)
  - Contexto do usuário incluído automaticamente em todas as conversas
  - Funciona em todos os provedores: Gemini, OpenAI, Groq e LangChain
  - Permite que o assistente "lembre" do usuário mesmo em sessões diferentes

- **Funcionalidade "Lembre-se disso"**: Sistema de salvamento explícito de informações pelo usuário
  - Palavras-chave para salvar fatos: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:"
  - Detecção automática e extração de fatos das mensagens do usuário
  - Fatos salvos são incluídos automaticamente no contexto de futuras conversas
  - Funciona em todos os provedores de IA (Gemini, OpenAI, Groq, LangChain)
  - Limite de 10 fatos por usuário para otimização de performance
  - Confirmação visual quando um fato é salvo (✅ Informação salva na memória!)

### Changed
- Estrutura do projeto expandida com novos serviços de chat
- **LangChain Agent Service**: Refatorado para usar memória persistente ao invés de memória em tempo de execução
  - Modelo atualizado para `gpt-4o-mini` (compatibilidade com API)
  - Histórico de conversa limitado a 20 mensagens para otimização
  - Ordem cronológica corrigida para manter contexto adequado
- **Sistema de Chat**: Expandido para suportar quatro provedores de IA (Gemini, OpenAI, Groq, LangChain)
- **Endpoint de Health Check**: Atualizado para incluir todos os serviços disponíveis
- **MemoryService**: Expandido com funcionalidades de perfil global por usuário e salvamento explícito
  - Método `save_message_with_profile_update()` para extração automática de informações
  - Método `get_user_context_for_chat()` para incluir contexto em conversas
  - Método `extract_user_info_from_message()` para análise de mensagens
  - Método `detect_and_save_user_fact()` para processamento de comandos "Lembre-se disso"
  - Método `save_user_fact()` para salvamento de fatos específicos
  - Método `get_user_facts()` para recuperação de fatos salvos
  - Método `remove_user_fact()` para remoção de fatos específicos
- **Todos os Serviços de Chat**: Atualizados para usar memória global por usuário e funcionalidade "Lembre-se disso"
  - Processamento automático de palavras-chave para salvamento de fatos
  - Confirmação visual quando informações são salvas
  - Metadados aprimorados incluindo flag `fact_saved`
- Sistema de memória aprimorado para suportar múltiplos provedores de IA

### Technical Details
- **Novos arquivos criados**:
  - `src/services/gemini_chat_service.py` - Serviço para integração com Google Gemini
  - `src/services/openai_chat_service.py` - Serviço para integração com OpenAI
  - `src/services/groq_chat_service.py` - Serviço para integração com Groq
  - `src/routes/chat_routes.py` - Rotas para endpoints de chat
  - `test_gemini_chat.py` - Script de teste para validação do chat Gemini
  - `test_langchain_memory.py` - Script de teste para validação da memória do LangChain
  - `test_groq_chat.py` - Script de teste para validação do chat Groq
  - `test_global_memory.py` - Script de teste para validação da memória global por usuário
  - `test_remember_this.py` - Script de teste para validação da funcionalidade "Lembre-se disso"
  - `README_MEMORY_IMPLEMENTATION.md` - Documentação técnica da implementação

- **Arquivos modificados**:
  - `src/services/memory_service.py` - Adicionada funcionalidade de perfil global por usuário e "Lembre-se disso"
  - `src/services/langchain_agent_service.py` - Integração com memória de longo prazo, global e "Lembre-se disso"
  - `src/services/gemini_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
  - `src/services/openai_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
  - `src/services/groq_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
  - `src/main.py` - Registro das novas rotas de chat
  - `.env` - Configuração das chaves de API

- **Dependências adicionadas**:
  - `google-generativeai` - SDK oficial do Google Gemini
  - `groq` - SDK oficial do Groq
  - Configuração de variáveis de ambiente para `GEMINI_API_KEY` e `GROQ_API_KEY`

- **Funcionalidades implementadas**:
  - Recuperação automática do histórico de conversas para todos os provedores
  - Construção de contexto para manter continuidade das conversas
  - Isolamento de sessões por `user_id` e `session_id`
  - Metadados de uso e estatísticas para cada interação
  - Tratamento de erros robusto em todos os serviços
  - Suporte a diferentes modelos OpenAI e Groq via parâmetro opcional
  - Integração transparente do LangChain com ferramentas e memória persistente
  - Endpoint para listar modelos disponíveis do Groq
  - **Memória global por usuário**: Perfil persistente que transcende sessões
  - **Extração automática**: Detecção de nome, profissão e idade nas mensagens
  - **Contexto inteligente**: Informações do usuário incluídas automaticamente em conversas
  - **Sistema "Lembre-se disso"**: Salvamento explícito de fatos pelo usuário
  - **Palavras-chave inteligentes**: Detecção automática de comandos de salvamento
  - **Confirmação visual**: Feedback imediato quando informações são salvas
  - **Gestão de fatos**: Limite automático e prevenção de duplicatas

### Notes
- O sistema mantém compatibilidade com a estrutura existente do projeto
- As conversas são armazenadas de forma segura no banco SQLite local
- Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário
- O histórico é limitado às últimas 20 interações por sessão para otimização de performance
- **LangChain Agent**: Mantém todas as funcionalidades originais (ferramentas, busca web, operações de arquivo) com memória persistente
- **Groq**: Oferece modelos rápidos e eficientes, incluindo Llama 3 e Mixtral
- **Memória Global**: Permite que o assistente "lembre" do usuário mesmo em diferentes sessões
  - Funciona automaticamente: quando o usuário diz seu nome, é salvo no perfil
  - Contexto é incluído em todas as conversas futuras daquele `user_id`
  - Informações persistem mesmo após reinicialização do servidor
- **Sistema "Lembre-se disso"**: Controle total do usuário sobre o que é salvo
  - Palavras-chave: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:"
  - Funciona em qualquer provedor (Gemini, OpenAI, Groq, LangChain)
  - Fatos são incluídos automaticamente em futuras conversas
  - Exemplo: "lembre-se disso: eu andei de bicicleta no sábado" → salvo permanentemente
- Todos os quatro provedores (Gemini, OpenAI, Groq, LangChain) agora compartilham o mesmo sistema de memória unificado
- Sistema escalável para adição de novos provedores de IA no futuro
- **Exemplo de uso completo**: 
  - Sessão 1: "Meu nome é João" + "lembre-se disso: gosto de café"
  - Sessão 2 (semana depois): Assistente sabe

