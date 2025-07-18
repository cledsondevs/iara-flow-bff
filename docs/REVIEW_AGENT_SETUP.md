# Agente de Análise de Reviews - Configuração e Uso

## Visão Geral

O agente de análise de reviews é uma extensão do IARA Flow BFF que adiciona funcionalidades autônomas para:

1. **Coleta de Reviews**: Coleta automática de reviews de lojas de aplicativos
2. **Análise de Sentimento**: Análise automática de sentimento e extração de tópicos
3. **Geração de Backlog**: Criação automática de itens de backlog baseados nos reviews
4. **Memória de Longo Prazo**: Aprendizado contínuo e otimização baseada em padrões históricos

## Configuração

### Pré-requisitos

1. PostgreSQL com extensão pgvector configurado
2. Chave da API OpenAI configurada
3. Dependências Python instaladas

### Instalação

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente no arquivo `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@54.162.170.1:5432/iara_db
OPENAI_API_KEY=your_openai_api_key_here
```

3. Executar a aplicação:
```bash
python src/main.py
```

### Inicialização Automática

O agente criará automaticamente as tabelas necessárias no banco de dados:
- `app_configs`: Configurações de aplicativos para monitoramento
- `reviews`: Reviews coletados das lojas
- `backlog_items`: Itens de backlog gerados automaticamente
- `sentiment_patterns`: Padrões de sentimento aprendidos
- `review_sentiment_patterns`: Padrões específicos de reviews
- `problem_solution_correlations`: Correlações entre problemas e soluções
- `sentiment_evolution`: Evolução do sentimento ao longo do tempo
- `backlog_optimization_patterns`: Padrões de otimização de backlog

## API Endpoints

### Controle do Agente Autônomo

#### Iniciar Modo Autônomo
```http
POST /api/review-agent/autonomous/start
```

Inicia o agente autônomo com agendamento automático:
- Coleta de reviews: a cada 6 horas
- Análise de sentimento: a cada 2 horas
- Geração de backlog: diariamente às 09:00
- Atualização de memória: diariamente às 23:00

#### Parar Modo Autônomo
```http
POST /api/review-agent/autonomous/stop
```

### Gerenciamento de Aplicativos

#### Adicionar Aplicativo para Monitoramento
```http
POST /api/review-agent/apps
Content-Type: application/json

{
  "package_name": "com.example.app",
  "app_name": "Meu App",
  "stores": ["google_play", "app_store"],
  "collection_frequency": 6
}
```

### Coleta de Reviews

#### Coletar Reviews de um App Específico
```http
POST /api/review-agent/apps/{package_name}/collect
```

#### Coletar Reviews de Todos os Apps
```http
POST /api/review-agent/collect-all
```

### Análise de Sentimento

#### Analisar Sentimento de um App
```http
POST /api/review-agent/apps/{package_name}/analyze
```

#### Analisar Todos os Reviews Pendentes
```http
POST /api/review-agent/analyze-all
```

### Geração de Backlog

#### Gerar Backlog para um App
```http
POST /api/review-agent/apps/{package_name}/backlog
Content-Type: application/json

{
  "days": 7
}
```

### Relatórios e Dashboards

#### Dashboard de um Aplicativo
```http
GET /api/review-agent/apps/{package_name}/dashboard
```

#### Resumo de Sentimentos
```http
GET /api/review-agent/sentiment/summary?package_name={package_name}&days=30
```

#### Tendências de Sentimento
```http
GET /api/review-agent/sentiment/trends?package_name={package_name}&days=30
```

#### Resumo do Backlog
```http
GET /api/review-agent/backlog/summary?package_name={package_name}
```

#### Relatório Abrangente
```http
GET /api/review-agent/reports/comprehensive?package_name={package_name}&days=30
```

### Memória e Otimização

#### Padrões Aprendidos
```http
GET /api/review-agent/memory/patterns?package_name={package_name}&pattern_type={type}
```

#### Sugestões de Otimização
```http
GET /api/review-agent/optimization/suggestions?package_name={package_name}
```

### Consultas Inteligentes

#### Processar Consulta em Linguagem Natural
```http
POST /api/review-agent/query
Content-Type: application/json

{
  "query": "Como está o sentimento do meu app?",
  "user_id": "user123"
}
```

Exemplos de consultas suportadas:
- "status" ou "resumo" - Status geral do sistema
- "dashboard [app]" - Dashboard de um app específico
- "coletar [app]" - Coletar reviews de um app
- "backlog [app]" - Gerar backlog para um app

## Uso Prático

### 1. Configuração Inicial

```bash
# 1. Adicionar um aplicativo para monitoramento
curl -X POST http://localhost:5000/api/review-agent/apps \
  -H "Content-Type: application/json" \
  -d '{
    "package_name": "com.meuapp.exemplo",
    "app_name": "Meu App Exemplo",
    "stores": ["google_play"],
    "collection_frequency": 6
  }'

# 2. Iniciar modo autônomo
curl -X POST http://localhost:5000/api/review-agent/autonomous/start
```

### 2. Coleta Manual (Opcional)

```bash
# Coletar reviews imediatamente
curl -X POST http://localhost:5000/api/review-agent/apps/com.meuapp.exemplo/collect
```

### 3. Análise Manual (Opcional)

```bash
# Analisar sentimento
curl -X POST http://localhost:5000/api/review-agent/apps/com.meuapp.exemplo/analyze
```

### 4. Geração de Backlog

```bash
# Gerar backlog baseado nos últimos 7 dias
curl -X POST http://localhost:5000/api/review-agent/apps/com.meuapp.exemplo/backlog \
  -H "Content-Type: application/json" \
  -d '{"days": 7}'
```

### 5. Visualizar Resultados

```bash
# Dashboard completo
curl http://localhost:5000/api/review-agent/apps/com.meuapp.exemplo/dashboard

# Relatório abrangente
curl http://localhost:5000/api/review-agent/reports/comprehensive?package_name=com.meuapp.exemplo&days=30
```

## Estrutura dos Dados

### Review
```json
{
  "id": "uuid",
  "package_name": "com.example.app",
  "store": "google_play",
  "review_id": "review123",
  "user_name": "Usuario",
  "rating": 4,
  "content": "Texto do review",
  "sentiment": "positive",
  "topics": ["performance", "ui"],
  "keywords": ["rápido", "bonito"]
}
```

### Backlog Item
```json
{
  "id": "uuid",
  "title": "Corrigir problema de login",
  "description": "Usuários relatam dificuldade no login...",
  "priority": 5,
  "category": "bug",
  "frequency": 15,
  "sentiment_score": -0.8,
  "status": "pending",
  "source_reviews": ["review1", "review2"]
}
```

## Monitoramento

### Status do Sistema
```bash
curl http://localhost:5000/api/review-agent/health
```

### Verificar Modo Autônomo
O status do modo autônomo é incluído na resposta de health check.

## Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco de dados**
   - Verificar se PostgreSQL está rodando
   - Verificar credenciais no DATABASE_URL

2. **Erro na API OpenAI**
   - Verificar se OPENAI_API_KEY está configurada
   - Verificar se há créditos disponíveis na conta

3. **Reviews não sendo coletados**
   - Verificar se a API externa está acessível
   - Verificar se o package_name está correto

4. **Agendamento não funcionando**
   - Verificar se o modo autônomo foi iniciado
   - Verificar logs da aplicação

### Logs

Os logs da aplicação mostrarão:
- Execução de tarefas agendadas
- Erros de coleta ou análise
- Status das operações

## Integração com Frontend

O agente pode ser integrado com qualquer frontend que consuma APIs REST. Exemplos de integração:

### React/JavaScript
```javascript
// Iniciar modo autônomo
const startAgent = async () => {
  const response = await fetch('/api/review-agent/autonomous/start', {
    method: 'POST'
  });
  const result = await response.json();
  console.log(result);
};

// Obter dashboard
const getDashboard = async (packageName) => {
  const response = await fetch(`/api/review-agent/apps/${packageName}/dashboard`);
  const result = await response.json();
  return result.result;
};
```

## Extensibilidade

O agente foi projetado para ser extensível:

1. **Novos tipos de análise**: Adicionar em `SentimentAnalysisService`
2. **Novas fontes de reviews**: Estender `ReviewCollectorService`
3. **Novos tipos de backlog**: Modificar `BacklogGeneratorService`
4. **Novos padrões de memória**: Estender `EnhancedMemoryService`

## Considerações de Performance

- O agente processa reviews em lotes para otimizar performance
- A memória de longo prazo usa embeddings para busca eficiente
- O agendamento evita sobrecarga do sistema
- Conexões de banco são gerenciadas eficientemente

## Segurança

- Todas as APIs requerem autenticação (implementar conforme necessário)
- Dados sensíveis são armazenados de forma segura
- Logs não expõem informações confidenciais

