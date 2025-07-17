# IARA Flow BFF - Orquestrador de Agentes de IA

Backend Flask que atua como um orquestrador para agentes de IA autônomos. Sua principal função é receber requisições de um frontend (React) e invocar um agente de IA autônomo baseado em LangChain para processar prompts de usuários.

## Características

- **Orquestrador de Agentes**: Gerencia agentes de IA autônomos baseados em LangChain
- **Memória de Longo Prazo**: Utiliza PostgreSQL com pgvector para armazenar e recuperar memórias
- **Ferramentas Autônomas**: Agente tem acesso a ferramentas de busca web, leitura/escrita de arquivos
- **API RESTful**: Interface simples para comunicação com frontend
- **Embeddings**: Busca semântica usando OpenAI Embeddings

## Tecnologias

- **Backend**: Flask + Python
- **Banco de Dados**: PostgreSQL com extensão pgvector
- **IA**: LangChain + OpenAI GPT-4
- **Embeddings**: OpenAI Embeddings para busca semântica
- **Ferramentas**: DuckDuckGo Search, File Management

## Estrutura do Projeto

```
src/
├── main.py                           # Aplicação Flask principal
├── routes/
│   └── agent_routes.py              # Rotas da API do agente
└── services/
    ├── langchain_agent_service.py   # Serviço principal do agente
    └── memory_service.py            # Gerenciamento de memória com pgvector
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do banco de dados PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@54.162.170.1:5432/iara_db

# Configurações do OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Configurações do LangChain (opcional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

### Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente
4. Execute a aplicação:
   ```bash
   python src/main.py
   ```

## API Endpoints

### POST /api/agent/chat
Conversar com o agente de IA

**Request:**
```json
{
  "message": "Olá, como você pode me ajudar?",
  "user_id": "user123",
  "session_id": "session456" // opcional
}
```

**Response:**
```json
{
  "success": true,
  "response": "Olá! Sou um assistente de IA...",
  "session_id": "session456",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### GET /api/agent/memory
Recuperar memória do agente

**Query Parameters:**
- `user_id` (obrigatório)
- `session_id` (opcional)

### DELETE /api/agent/memory
Limpar memória do agente

**Request:**
```json
{
  "user_id": "user123",
  "session_id": "session456" // opcional
}
```

### GET /api/agent/health
Verificação de saúde da API

## Funcionalidades do Agente

O agente LangChain tem acesso às seguintes ferramentas:

1. **Busca Web**: Pesquisar informações atualizadas na internet
2. **Leitura de Arquivos**: Ler conteúdo de arquivos
3. **Escrita de Arquivos**: Criar e editar arquivos
4. **Listagem de Diretórios**: Explorar estrutura de pastas

## Memória

O sistema implementa dois tipos de memória:

1. **Memória de Conversa**: Histórico de mensagens por sessão
2. **Memória de Longo Prazo**: Informações importantes extraídas automaticamente

A busca semântica permite recuperar informações relevantes baseadas no contexto da conversa.

## Deploy

O projeto está configurado para deploy automático no EC2. Após fazer commit das alterações, o deploy é executado automaticamente.

## Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas alterações
4. Push para a branch
5. Abra um Pull Request

