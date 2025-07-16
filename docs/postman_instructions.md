# Testando o Backend Iara Flow no Postman

## URL Base da API
```
https://iara-flow-bff.vercel.app/api
```

## Endpoints Disponíveis

### 1. Teste de Conexão
**Endpoint:** `GET /flow/test`
**URL Completa:** `https://iara-flow-bff.vercel.app/api/flow/test`

**Configuração no Postman:**
- Método: `GET`
- Headers: Não necessário

**Resposta Esperada:**
```json
{
  "message": "API funcionando corretamente",
  "timestamp": "2025-07-16T17:39:33.000Z"
}
```

### 2. Execução Direta de Fluxo (Principal)
**Endpoint:** `POST /flow/execute`
**URL Completa:** `https://iara-flow-bff.vercel.app/api/flow/execute`

**Configuração no Postman:**
- Método: `POST`
- Headers:
  - `Content-Type: application/json`

**Body (raw JSON):**
```json
{
  "flow_data": {
    "nodes": [
      {
        "id": "1",
        "type": "agent",
        "position": {
          "x": 202.08,
          "y": 97.84
        },
        "data": {
          "label": "Chat Assistant",
          "agentType": "chatbot",
          "provider": "gemini",
          "model": "gemini-1.5-flash",
          "temperature": 0.7,
          "instructions": "Assistente conversacional para suporte ao cliente"
        }
      },
      {
        "id": "2",
        "type": "data",
        "position": {
          "x": -100.76,
          "y": 5.76
        },
        "data": {
          "label": "User Input",
          "dataType": "input",
          "format": "text/plain",
          "userInput": "me monte uma receita de bolo"
        }
      },
      {
        "id": "3",
        "type": "data",
        "position": {
          "x": 578.62,
          "y": 116.09
        },
        "data": {
          "label": "Agent Output",
          "dataType": "output",
          "format": "text/plain"
        }
      }
    ],
    "edges": [
      {
        "id": "xy-edge__2-1",
        "source": "2",
        "target": "1",
        "type": "smoothstep",
        "animated": true,
        "style": {
          "strokeWidth": 2
        }
      },
      {
        "id": "xy-edge__1-3",
        "source": "1",
        "target": "3",
        "type": "smoothstep",
        "animated": true,
        "style": {
          "strokeWidth": 2
        }
      }
    ],
    "exportedAt": "2025-07-16T17:27:22.876Z"
  },
  "input": "me monte uma receita de bolo"
}
```

**Resposta Esperada:**
```json
{
  "success": true,
  "output": "Para te ajudar a montar uma receita de bolo, preciso saber que tipo de bolo você quer! Para te dar a melhor receita possível, me diga:\n\n* **Que tipo de bolo você deseja?** (ex: chocolate, baunilha, cenoura, laranja, etc.)\n* **Qual o nível de dificuldade que você busca?** (ex: fácil, médio, difícil)\n* **Você tem alguma restrição alimentar?** (ex: sem glúten, sem lactose, vegano, etc.)\n* **Para quantas pessoas?**\n\nCom essas informações, posso criar uma receita personalizada para você!",
  "execution_path": ["2", "1", "3"],
  "node_outputs": {
    "1": "Para te ajudar a montar uma receita de bolo...",
    "2": "me monte uma receita de bolo",
    "3": "Para te ajudar a montar uma receita de bolo..."
  }
}
```

### 3. Validação de Fluxo
**Endpoint:** `POST /flow/validate`
**URL Completa:** `https://iara-flow-bff.vercel.app/api/flow/validate`

**Configuração no Postman:**
- Método: `POST`
- Headers:
  - `Content-Type: application/json`

**Body (raw JSON):**
```json
{
  "flow_data": {
    "nodes": [
      {
        "id": "1",
        "type": "agent",
        "data": {
          "label": "Chat Assistant",
          "agentType": "chatbot",
          "provider": "gemini",
          "model": "gemini-1.5-flash",
          "temperature": 0.7,
          "instructions": "Assistente conversacional"
        }
      }
    ],
    "edges": []
  }
}
```

**Resposta Esperada:**
```json
{
  "validation": {
    "valid": true,
    "errors": [],
    "warnings": []
  }
}
```

## Exemplos de Teste com Diferentes Provedores

### Teste com OpenAI (GPT-4)
```json
{
  "flow_data": {
    "nodes": [
      {
        "id": "1",
        "type": "agent",
        "data": {
          "label": "Chat Assistant",
          "agentType": "chatbot",
          "provider": "openai",
          "model": "gpt-4",
          "temperature": 0.7,
          "instructions": "Você é um assistente útil e amigável"
        }
      },
      {
        "id": "2",
        "type": "data",
        "data": {
          "label": "User Input",
          "dataType": "input",
          "format": "text/plain",
          "userInput": "Explique o que é inteligência artificial"
        }
      }
    ],
    "edges": [
      {
        "id": "edge-1",
        "source": "2",
        "target": "1"
      }
    ]
  },
  "input": "Explique o que é inteligência artificial"
}
```

### Teste com Google Gemini (Atual)
```json
{
  "flow_data": {
    "nodes": [
      {
        "id": "1",
        "type": "agent",
        "data": {
          "label": "Chat Assistant",
          "agentType": "chatbot",
          "provider": "gemini",
          "model": "gemini-1.5-flash",
          "temperature": 0.5,
          "instructions": "Responda de forma clara e objetiva"
        }
      },
      {
        "id": "2",
        "type": "data",
        "data": {
          "label": "User Input",
          "dataType": "input",
          "format": "text/plain",
          "userInput": "Como fazer um café perfeito?"
        }
      }
    ],
    "edges": [
      {
        "id": "edge-1",
        "source": "2",
        "target": "1"
      }
    ]
  },
  "input": "Como fazer um café perfeito?"
}
```

## Códigos de Status HTTP

- **200 OK**: Requisição executada com sucesso
- **400 Bad Request**: Dados inválidos no corpo da requisição
- **500 Internal Server Error**: Erro interno do servidor

## Dicas para Teste

1. **Sempre inclua o header `Content-Type: application/json`** para requisições POST
2. **Verifique se o JSON está bem formatado** antes de enviar
3. **O campo `input` deve corresponder ao `userInput` do nó de entrada**
4. **Para testar diferentes cenários**, altere o `provider`, `model` e `instructions`
5. **Monitore os logs de resposta** para identificar possíveis erros

## Estrutura de Erro

Em caso de erro, a resposta seguirá este formato:
```json
{
  "success": false,
  "error": "Descrição do erro",
  "details": "Detalhes adicionais do erro (opcional)"
}
```

