# Documentação da API Iara Flow BFF

Bem-vindo à documentação da API Iara Flow BFF. Esta API serve como um Backend for Frontend (BFF) para o sistema Iara Flow, orquestrando serviços de IA e gerenciando interações com agentes inteligentes para análise de dados e comunicação.

## Visão Geral

A API Iara Flow BFF é construída com Flask e Python, fornecendo uma interface robusta e escalável para interagir com diversos agentes de IA, incluindo agentes de chat e agentes de análise de reviews. Ela gerencia a comunicação entre o frontend e os serviços de backend, garantindo uma experiência de usuário fluida e eficiente.

### Principais Funcionalidades

*   **Interação com Agentes de IA:** Facilita a comunicação com agentes de IA para chat e outras operações.
*   **Gerenciamento de Memória:** Armazena e recupera o histórico de conversas e dados relevantes para cada usuário e sessão.
*   **Análise de Reviews:** Permite a coleta, análise de sentimento e geração de backlog a partir de reviews de aplicativos.
*   **Relatórios Abrangentes:** Gera relatórios detalhados sobre o status do sistema, análise de sentimento e backlog.
*   **Verificação de Saúde:** Endpoints dedicados para monitoramento da saúde da API.

## Autenticação

Atualmente, a autenticação não é explicitamente detalhada nos arquivos analisados (`index.py`, `main.py`, `agent_routes.py`, `review_agent_routes.py`). Para ambientes de produção, é altamente recomendável implementar um mecanismo de autenticação robusto (e.g., OAuth2, JWT) para proteger os endpoints da API.

## Estrutura da API

A API é organizada em blueprints Flask, com rotas definidas para diferentes funcionalidades. Os principais módulos de rota identificados são:

*   `agent_routes.py`: Contém endpoints relacionados à interação geral com agentes de IA, como chat e gerenciamento de memória.
*   `review_agent_routes.py`: Contém endpoints específicos para o agente de análise de reviews, incluindo coleta, análise e geração de relatórios.

## Endpoints

A seguir, detalhamos os endpoints disponíveis na API Iara Flow BFF, incluindo seus métodos HTTP, URLs, parâmetros de requisição e exemplos de resposta.



### Endpoints do Agente de IA (`/api`)

#### `POST /api/agent/chat`

**Descrição:** Endpoint principal para conversar com o agente de IA.

**Parâmetros de Requisição (JSON):**

*   `message` (string, obrigatório): A mensagem do usuário para o agente.
*   `user_id` (string, obrigatório): O ID único do usuário.
*   `session_id` (string, opcional): O ID da sessão de chat. Se não fornecido, uma nova sessão pode ser iniciada ou inferida.

**Exemplo de Requisição:**

```json
{
    "message": "Olá, qual é a previsão do tempo para hoje?",
    "user_id": "user123",
    "session_id": "chat_session_abc"
}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "response": "A previsão do tempo para hoje é de sol com algumas nuvens.",
    "session_id": "chat_session_abc",
    "timestamp": "2025-07-24T10:30:00.000Z"
}
```

**Exemplo de Resposta (Erro - 400 Bad Request):**

```json
{
    "error": "Mensagem é obrigatória",
    "code": 400
}
```

#### `GET /api/agent/memory`

**Descrição:** Recupera a memória do agente para um usuário e sessão específicos.

**Parâmetros de Requisição (Query):**

*   `user_id` (string, obrigatório): O ID único do usuário.
*   `session_id` (string, opcional): O ID da sessão de chat.

**Exemplo de Requisição:**

```
GET /api/agent/memory?user_id=user123&session_id=chat_session_abc
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "memory": [
        {"role": "user", "content": "Olá"},
        {"role": "agent", "content": "Olá! Como posso ajudar?"}
    ],
    "timestamp": "2025-07-24T10:35:00.000Z"
}
```

#### `DELETE /api/agent/memory`

**Descrição:** Limpa a memória do agente para um usuário e sessão específicos.

**Parâmetros de Requisição (JSON):**

*   `user_id` (string, obrigatório): O ID único do usuário.
*   `session_id` (string, opcional): O ID da sessão de chat.

**Exemplo de Requisição:**

```json
{
    "user_id": "user123",
    "session_id": "chat_session_abc"
}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "message": "Memória limpa com sucesso",
    "timestamp": "2025-07-24T10:40:00.000Z"
}
```

#### `GET /api/agent/health`

**Descrição:** Endpoint de verificação de saúde da API do agente.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```
GET /api/agent/health
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "message": "Agente de IA está funcionando!",
    "timestamp": "2025-07-24T10:45:00.000Z"
}
```



### Endpoints do Agente de Análise de Reviews (`/api/review-agent`)

#### `GET /api/review-agent/health`

**Descrição:** Verificação de saúde da API do agente de reviews.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```
GET /api/review-agent/health
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "status": "healthy",
    "system_status": {
        "database_connection": "OK",
        "agent_status": "running"
    },
    "timestamp": "2025-07-24T11:00:00.000Z"
}
```

#### `POST /api/review-agent/autonomous/start`

**Descrição:** Iniciar o modo autônomo do agente de reviews.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```json
{}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Modo autônomo iniciado com sucesso.",
    "timestamp": "2025-07-24T11:05:00.000Z"
}
```

#### `POST /api/review-agent/autonomous/stop`

**Descrição:** Parar o modo autônomo do agente de reviews.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```json
{}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Modo autônomo parado com sucesso.",
    "timestamp": "2025-07-24T11:10:00.000Z"
}
```

#### `POST /api/review-agent/apps`

**Descrição:** Adicionar um aplicativo para monitoramento de reviews.

**Parâmetros de Requisição (JSON):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo (e.g., `com.example.app`).
*   `app_name` (string, obrigatório): O nome amigável do aplicativo.
*   `stores` (array de strings, opcional): Lista de lojas de aplicativos para monitorar (e.g., `["google_play", "apple_app_store"]`). Padrão: `["google_play"]`.
*   `collection_frequency` (inteiro, opcional): Frequência de coleta em horas. Padrão: `6`.

**Exemplo de Requisição:**

```json
{
    "package_name": "com.mycompany.myapp",
    "app_name": "Meu Aplicativo",
    "stores": ["google_play"],
    "collection_frequency": 12
}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Aplicativo 'Meu Aplicativo' adicionado para monitoramento.",
    "timestamp": "2025-07-24T11:15:00.000Z"
}
```

#### `POST /api/review-agent/apps/<package_name>/collect`

**Descrição:** Coletar reviews para um aplicativo específico.

**Parâmetros de Requisição (URL):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.

**Exemplo de Requisição:**

```
POST /api/review-agent/apps/com.mycompany.myapp/collect
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Coleta de reviews iniciada para com.mycompany.myapp.",
    "timestamp": "2025-07-24T11:20:00.000Z"
}
```

#### `POST /api/review-agent/apps/<package_name>/analyze`

**Descrição:** Analisar o sentimento dos reviews para um aplicativo específico.

**Parâmetros de Requisição (URL):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.

**Exemplo de Requisição:**

```
POST /api/review-agent/apps/com.mycompany.myapp/analyze
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Análise de sentimento iniciada para com.mycompany.myapp.",
    "timestamp": "2025-07-24T11:25:00.000Z"
}
```

#### `POST /api/review-agent/apps/<package_name>/backlog`

**Descrição:** Gerar backlog a partir dos reviews para um aplicativo específico.

**Parâmetros de Requisição (URL):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.

**Parâmetros de Requisição (JSON, opcional):**

*   `days` (inteiro, opcional): Número de dias para considerar na geração do backlog. Padrão: `7`.

**Exemplo de Requisição:**

```json
{
    "days": 14
}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": {
        "high_priority_items": ["Bug de login", "Problema de desempenho"],
        "medium_priority_items": ["Melhoria de UI"],
        "low_priority_items": []
    },
    "timestamp": "2025-07-24T11:30:00.000Z"
}
```

#### `GET /api/review-agent/apps/<package_name>/dashboard`

**Descrição:** Obter o dashboard completo de um aplicativo, incluindo métricas de reviews e sentimentos.

**Parâmetros de Requisição (URL):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.

**Exemplo de Requisição:**

```
GET /api/review-agent/apps/com.mycompany.myapp/dashboard
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": {
        "total_reviews": 1500,
        "positive_reviews": 1200,
        "negative_reviews": 200,
        "neutral_reviews": 100,
        "average_rating": 4.5,
        "sentiment_breakdown": {
            "positive": 80,
            "negative": 13.3,
            "neutral": 6.7
        },
        "top_keywords": ["rápido", "fácil de usar", "travando"],
        "recent_reviews": [
            {"id": "1", "text": "Ótimo app!", "sentiment": "positive"}
        ]
    },
    "timestamp": "2025-07-24T11:35:00.000Z"
}
```

#### `POST /api/review-agent/collect-all`

**Descrição:** Coletar reviews de todos os aplicativos configurados.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```json
{}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Coleta de reviews iniciada para todos os aplicativos.",
    "timestamp": "2025-07-24T11:40:00.000Z"
}
```

#### `POST /api/review-agent/analyze-all`

**Descrição:** Analisar o sentimento de todos os reviews pendentes.

**Parâmetros de Requisição:** Nenhum.

**Exemplo de Requisição:**

```json
{}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Análise de sentimento iniciada para todos os reviews pendentes.",
    "timestamp": "2025-07-24T11:45:00.000Z"
}
```

#### `GET /api/review-agent/backlog/summary`

**Descrição:** Obter um resumo geral do backlog de todos os aplicativos ou de um aplicativo específico.

**Parâmetros de Requisição (Query, opcional):**

*   `package_name` (string, opcional): O nome do pacote do aplicativo para filtrar o resumo.

**Exemplo de Requisição:**

```
GET /api/review-agent/backlog/summary?package_name=com.mycompany.myapp
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": {
        "total_items": 50,
        "high_priority": 10,
        "medium_priority": 25,
        "low_priority": 15,
        "top_issues": ["Bug de crash", "Lentidão"],
        "app_breakdown": {
            "com.mycompany.myapp": {"high_priority": 5},
            "com.anotherapp.game": {"high_priority": 3}
        }
    },
    "timestamp": "2025-07-24T11:50:00.000Z"
}
```

#### `GET /api/review-agent/sentiment/summary`

**Descrição:** Obter um resumo de sentimentos para todos os aplicativos ou para um aplicativo específico.

**Parâmetros de Requisição (Query, opcional):**

*   `package_name` (string, opcional): O nome do pacote do aplicativo para filtrar o resumo.
*   `days` (inteiro, opcional): Número de dias para considerar no resumo. Padrão: `30`.

**Exemplo de Requisição:**

```
GET /api/review-agent/sentiment/summary?package_name=com.mycompany.myapp&days=7
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": {
        "overall_sentiment": "positive",
        "positive_percentage": 75,
        "negative_percentage": 15,
        "neutral_percentage": 10,
        "sentiment_by_day": [
            {"date": "2025-07-23", "positive": 80, "negative": 10, "neutral": 10}
        ]
    },
    "timestamp": "2025-07-24T11:55:00.000Z"
}
```

#### `GET /api/review-agent/sentiment/trends`

**Descrição:** Obter tendências de sentimento para um aplicativo específico.

**Parâmetros de Requisição (Query):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.
*   `days` (inteiro, opcional): Número de dias para considerar nas tendências. Padrão: `30`.

**Exemplo de Requisição:**

```
GET /api/review-agent/sentiment/trends?package_name=com.mycompany.myapp&days=60
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": [
        {"date": "2025-05-25", "positive": 70, "negative": 20, "neutral": 10},
        {"date": "2025-06-24", "positive": 75, "negative": 15, "neutral": 10},
        {"date": "2025-07-24", "positive": 80, "negative": 10, "neutral": 10}
    ],
    "timestamp": "2025-07-24T12:00:00.000Z"
}
```

#### `POST /api/review-agent/query`

**Descrição:** Processar uma consulta do usuário relacionada a reviews ou dados de aplicativos.

**Parâmetros de Requisição (JSON):**

*   `query` (string, obrigatório): A consulta do usuário.
*   `user_id` (string, opcional): O ID do usuário que fez a consulta. Padrão: `anonymous`.

**Exemplo de Requisição:**

```json
{
    "query": "Quais são os principais problemas do aplicativo 'Meu Aplicativo' na última semana?",
    "user_id": "analyst456"
}
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "result": "Os principais problemas relatados na última semana para 'Meu Aplicativo' são: travamentos frequentes e lentidão ao carregar imagens.",
    "query": "Quais são os principais problemas do aplicativo 'Meu Aplicativo' na última semana?",
    "timestamp": "2025-07-24T12:05:00.000Z"
}
```

#### `GET /api/review-agent/reports/comprehensive`

**Descrição:** Gerar um relatório abrangente do sistema ou de um aplicativo específico.

**Parâmetros de Requisição (Query, opcional):**

*   `package_name` (string, opcional): O nome do pacote do aplicativo para gerar um relatório específico.
*   `days` (inteiro, opcional): Número de dias para considerar no relatório. Padrão: `30`.

**Exemplo de Requisição (Relatório geral):**

```
GET /api/review-agent/reports/comprehensive
```

**Exemplo de Requisição (Relatório por aplicativo):**

```
GET /api/review-agent/reports/comprehensive?package_name=com.mycompany.myapp&days=7
```

**Exemplo de Resposta (Sucesso - 200 OK, relatório geral):**

```json
{
    "success": true,
    "report": {
        "type": "system_wide",
        "period_days": 30,
        "sentiment_analysis": {
            "overall_sentiment": "positive",
            "positive_percentage": 70
        },
        "backlog_analysis": {
            "total_items": 100,
            "high_priority": 20
        },
        "system_status": {
            "database_connection": "OK"
        }
    },
    "generated_at": "2025-07-24T12:10:00.000Z"
}
```

#### `GET /api/review-agent/memory/patterns`

**Descrição:** Obter padrões aprendidos pela memória de longo prazo do agente de reviews.

**Parâmetros de Requisição (Query):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.
*   `pattern_type` (string, opcional): Tipo de padrão a ser recuperado (e.g., `sentiment`, `topic`).

**Exemplo de Requisição:**

```
GET /api/review-agent/memory/patterns?package_name=com.mycompany.myapp&pattern_type=sentiment
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "patterns": [
        {"pattern": "Problemas de bateria após atualização", "sentiment": "negative"},
        {"pattern": "Interface de usuário intuitiva", "sentiment": "positive"}
    ],
    "package_name": "com.mycompany.myapp",
    "pattern_type": "sentiment",
    "timestamp": "2025-07-24T12:15:00.000Z"
}
```

#### `GET /api/review-agent/optimization/suggestions`

**Descrição:** Obter sugestões de otimização baseadas na análise de backlog e memória.

**Parâmetros de Requisição (Query):**

*   `package_name` (string, obrigatório): O nome do pacote do aplicativo.

**Exemplo de Requisição:**

```
GET /api/review-agent/optimization/suggestions?package_name=com.mycompany.myapp
```

**Exemplo de Resposta (Sucesso - 200 OK):**

```json
{
    "success": true,
    "suggestions": [
        "Priorizar correção do bug de login devido ao alto impacto nos usuários.",
        "Melhorar o desempenho da rolagem em listas longas."
    ],
    "package_name": "com.mycompany.myapp",
    "timestamp": "2025-07-24T12:20:00.000Z"
}
```

## Tratamento de Erros

A API Iara Flow BFF utiliza códigos de status HTTP padrão para indicar o sucesso ou falha de uma requisição. Além disso, as respostas de erro incluem um objeto JSON com detalhes sobre o erro.

*   **400 Bad Request:** A requisição não pôde ser entendida ou processada devido a sintaxe inválida ou parâmetros ausentes/inválidos.
*   **404 Not Found:** O recurso solicitado não foi encontrado.
*   **405 Method Not Allowed:** O método HTTP utilizado na requisição não é permitido para o recurso.
*   **500 Internal Server Error:** Um erro inesperado ocorreu no servidor.

**Exemplo de Resposta de Erro:**

```json
{
    "success": false,
    "error": "Mensagem é obrigatória",
    "timestamp": "2025-07-24T10:40:00.000Z"
}
```

## Conclusão

A API Iara Flow BFF oferece um conjunto abrangente de funcionalidades para integrar agentes de IA e gerenciar a análise de reviews de aplicativos. Sua arquitetura modular baseada em Flask facilita a extensão e manutenção. Para implantação em produção, a implementação de autenticação e monitoramento robustos é crucial.

---

**Autor:** Cledson Alves
**Data:** 24 de julho de 2025


