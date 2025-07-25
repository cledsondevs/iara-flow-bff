# Configuração de Chaves de API

Este projeto agora utiliza um sistema de gerenciamento de chaves de API armazenadas no banco de dados SQLite, proporcionando maior segurança e flexibilidade.

## Como Configurar

### 1. Configurar suas chaves de API

Edite o arquivo `setup_api_keys.py` e substitua os placeholders pelas suas chaves reais:

```python
api_keys = {
    "gemini": "SUA_CHAVE_GEMINI_AQUI",
    "openai": "SUA_CHAVE_OPENAI_AQUI", 
    "groq": "SUA_CHAVE_GROQ_AQUI"
}
```

### 2. Executar o script de configuração

```bash
python setup_api_keys.py
```

### 3. Verificar se as chaves foram salvas

O script mostrará o status de cada chave configurada:

```
✅ openai: Configurada
✅ gemini: Configurada  
✅ groq: Configurada
```

## Como Funciona

### APIKeyService

O `APIKeyService` é responsável por:
- Salvar chaves de API no banco SQLite
- Recuperar chaves por usuário e serviço
- Criptografar as chaves (implementação futura)

### Integração com Serviços

Todos os serviços de IA foram atualizados para usar o APIKeyService:

- **GeminiAgentService**: Busca a chave do Gemini no banco
- **OpenAIAgentService**: Busca a chave do OpenAI no banco  
- **GroqChatService**: Busca a chave do Groq no banco
- **LangChainAgentService**: Busca a chave do OpenAI no banco

### Endpoints de API Keys

- `POST /api/api/keys` - Salvar uma chave de API
- `GET /api/api/keys/{user_id}/{service}` - Recuperar uma chave específica

## Exemplo de Uso via API

### Salvar uma chave:

```bash
curl -X POST http://localhost:5000/api/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "1",
    "service_name": "openai",
    "api_key": "sua-chave-aqui"
  }'
```

### Recuperar uma chave:

```bash
curl -X GET http://localhost:5000/api/api/keys/1/openai
```

## Segurança

- As chaves são armazenadas no banco SQLite local
- Cada usuário tem suas próprias chaves
- Sistema preparado para implementar criptografia das chaves
- Chaves não ficam mais expostas em variáveis de ambiente

## Migração

Se você tinha chaves configuradas em variáveis de ambiente (.env), agora precisa:

1. Executar o `setup_api_keys.py` com suas chaves
2. Remover as chaves do arquivo .env (opcional)
3. As APIs continuarão funcionando normalmente

## Troubleshooting

### "API key não encontrada para este usuário"

Execute o script de configuração:
```bash
python setup_api_keys.py
```

### Testar se as APIs estão funcionando

Execute o script de testes:
```bash
python test_api_endpoints.py
```

