# Iara Flow Backend

Backend para aplicação de geração de agentes de IA que interpreta e executa fluxos JSON.

## Funcionalidades

- Interpretação e execução de fluxos JSON com nós de agentes de IA
- Integração com APIs de IA (OpenAI e Google Gemini)
- Armazenamento no DynamoDB (AWS)
- API REST para gerenciamento de fluxos e execuções
- Suporte a diferentes tipos de agentes (chatbot, analyzer, generator)
- Validação de fluxos antes da execução

## Tecnologias

- Flask (Python)
- DynamoDB (AWS)
- OpenAI API
- Google Gemini API
- Flask-CORS para integração frontend

## Estrutura da API

### Fluxos
- `POST /api/flows` - Criar fluxo
- `GET /api/flows` - Listar fluxos
- `GET /api/flows/{id}` - Obter fluxo específico
- `PUT /api/flows/{id}` - Atualizar fluxo
- `DELETE /api/flows/{id}` - Deletar fluxo
- `POST /api/flows/{id}/execute` - Executar fluxo
- `POST /api/flows/{id}/validate` - Validar fluxo

### Execuções
- `GET /api/flows/{id}/executions` - Listar execuções de um fluxo
- `GET /api/executions/{id}` - Obter execução específica

## Configuração

### Variáveis de Ambiente

```
OPENAI_API_KEY=sua_chave_openai
GEMINI_API_KEY=sua_chave_gemini
AWS_ACCESS_KEY_ID=sua_chave_aws
AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aws
AWS_REGION=us-east-1
```

### Desenvolvimento Local

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente no arquivo `.env`

3. Executar:
```bash
python src/main.py
```

### Deploy no Vercel

1. Configurar variáveis de ambiente no painel do Vercel:
   - `openai_api_key`
   - `gemini_api_key`
   - `aws_access_key_id`
   - `aws_secret_access_key`

2. Fazer deploy:
```bash
vercel --prod
```

## Estrutura do Projeto

```
├── src/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── models/              # Modelos de dados
│   ├── routes/              # Rotas da API
│   └── services/            # Serviços (IA, DynamoDB, Executor)
├── api/
│   └── index.py             # Ponto de entrada para Vercel
├── requirements.txt         # Dependências Python
├── vercel.json             # Configuração do Vercel
└── .env                    # Variáveis de ambiente (local)
```

## Formato do Fluxo JSON

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "data",
      "data": {
        "label": "User Input",
        "dataType": "input",
        "userInput": "Texto do usuário"
      }
    },
    {
      "id": "2", 
      "type": "agent",
      "data": {
        "label": "Chat Assistant",
        "agentType": "chatbot",
        "provider": "openai",
        "model": "gpt-4",
        "temperature": 0.7,
        "instructions": "Instruções para o agente"
      }
    }
  ],
  "edges": [
    {
      "source": "1",
      "target": "2"
    }
  ]
}
```

## Tipos de Nós Suportados

### Data Nodes
- `input`: Entrada do usuário
- `output`: Saída do fluxo

### Agent Nodes
- `chatbot`: Assistente conversacional
- `analyzer`: Analisador de dados
- `generator`: Gerador de conteúdo

### Logic Nodes
- `condition`: Nós de condição (if/else)

## Provedores de IA Suportados

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Google Gemini**: gemini-pro, gemini-1.5-pro

- ** - teste 52** 

