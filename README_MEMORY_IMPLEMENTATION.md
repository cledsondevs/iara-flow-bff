# Implementação de Memória de Longo Prazo - Chats Gemini e OpenAI

## Resumo

Esta implementação adiciona memória de longo prazo aos endpoints de chat Gemini e OpenAI, permitindo que as conversas sejam mantidas entre sessões diferentes. O sistema utiliza o banco SQLite existente para armazenar o histórico de conversas de forma persistente.

## Endpoints Implementados

### Chat Gemini
- **POST** `/api/gemini/chat` - Conversar com o Gemini
- **GET** `/api/gemini/memory` - Recuperar memória da conversa
- **DELETE** `/api/gemini/memory` - Limpar memória da conversa

### Chat OpenAI
- **POST** `/api/openai/chat` - Conversar com o OpenAI
- **GET** `/api/openai/memory` - Recuperar memória da conversa
- **DELETE** `/api/openai/memory` - Limpar memória da conversa

### Verificação de Saúde
- **GET** `/api/chat/health` - Verificar status dos serviços

## Estrutura de Requisição

### Chat (POST)
```json
{
  "message": "Sua mensagem aqui",
  "user_id": "identificador_do_usuario",
  "session_id": "identificador_da_sessao", // opcional
  "model": "gpt-4o-mini" // opcional, apenas para OpenAI
}
```

### Recuperar Memória (GET)
```
GET /api/gemini/memory?user_id=identificador_do_usuario&session_id=identificador_da_sessao
```

### Limpar Memória (DELETE)
```json
{
  "user_id": "identificador_do_usuario",
  "session_id": "identificador_da_sessao" // opcional
}
```

## Estrutura de Resposta

### Chat
```json
{
  "success": true,
  "response": "Resposta da IA",
  "session_id": "identificador_da_sessao",
  "model": "modelo_utilizado",
  "timestamp": "2025-07-24T20:26:08.492486",
  "usage": { // apenas OpenAI
    "prompt_tokens": 150,
    "completion_tokens": 75,
    "total_tokens": 225
  }
}
```

### Memória
```json
{
  "success": true,
  "memory": [
    {
      "message": "Mensagem do usuário",
      "response": "Resposta da IA",
      "created_at": "2025-07-24T20:26:08.492486",
      "metadata": "{\"model\": \"gemini-1.5-flash\", \"provider\": \"google\"}"
    }
  ],
  "timestamp": "2025-07-24T20:26:08.492486"
}
```

## Funcionalidades

### 1. Memória Persistente
- As conversas são armazenadas no banco SQLite
- Histórico mantido entre reinicializações do servidor
- Recuperação automática do contexto em novas mensagens

### 2. Sistema de Sessões
- Isolamento de conversas por `user_id` e `session_id`
- Múltiplas conversas simultâneas por usuário
- Geração automática de `session_id` se não fornecido

### 3. Contexto de Conversa
- **Gemini**: Contexto construído como string formatada
- **OpenAI**: Contexto construído como array de mensagens
- Limitado às últimas 20 interações por performance

### 4. Metadados e Estatísticas
- Informações de uso (tokens para OpenAI)
- Modelo utilizado em cada interação
- Timestamp de cada mensagem
- Provider (google/openai)

## Configuração

### Variáveis de Ambiente
```env
GEMINI_API_KEY=sua_chave_do_gemini
OPENAI_API_KEY=sua_chave_do_openai
DB_PATH=./iara_flow.db
```

### Dependências Adicionadas
- `google-generativeai` - SDK oficial do Google Gemini
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `flask-cors` - Suporte a CORS

## Arquivos Criados/Modificados

### Novos Arquivos
- `src/services/gemini_chat_service.py` - Serviço Gemini
- `src/services/openai_chat_service.py` - Serviço OpenAI
- `src/routes/chat_routes.py` - Rotas dos chats
- `test_gemini_chat.py` - Testes do Gemini
- `CHANGELOG.md` - Log de mudanças

### Arquivos Modificados
- `src/main.py` - Registro das novas rotas
- `.env` - Configuração das APIs

## Exemplo de Uso

### 1. Iniciar Conversa
```bash
curl -X POST http://localhost:5000/api/gemini/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá! Meu nome é João.",
    "user_id": "user123"
  }'
```

### 2. Continuar Conversa (mesma sessão)
```bash
curl -X POST http://localhost:5000/api/gemini/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Você lembra qual é o meu nome?",
    "user_id": "user123",
    "session_id": "session_id_retornado"
  }'
```

### 3. Verificar Memória
```bash
curl "http://localhost:5000/api/gemini/memory?user_id=user123&session_id=session_id"
```

## Observações Técnicas

### Limitações
- Histórico limitado a 20 mensagens por sessão para otimização
- Modelo Gemini configurado para `gemini-1.5-flash`
- Modelo OpenAI padrão: `gpt-4o-mini`

### Segurança
- Validação de parâmetros obrigatórios
- Tratamento de erros robusto
- Isolamento de dados por usuário/sessão

### Performance
- Conexões SQLite com context manager
- Limitação de histórico para reduzir latência
- Índices automáticos por user_id e session_id

## Próximos Passos

1. **Testes de Integração**: Validar com chaves de API reais
2. **Otimizações**: Implementar cache em memória para sessões ativas
3. **Monitoramento**: Adicionar logs e métricas de uso
4. **Backup**: Implementar estratégia de backup do banco de dados

