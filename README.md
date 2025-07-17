# Iara Flow Backend

Backend para aplicação de geração de agentes de IA que interpreta e executa fluxos JSON.

## Funcionalidades

- Interpretação e execução de fluxos JSON com nós de agentes de IA
- Integração com APIs de IA (OpenAI e Google Gemini)
- Armazenamento no PostgreSQL
- API REST para gerenciamento de fluxos e execuções
- Suporte a diferentes tipos de agentes (chatbot, analyzer, generator)
- Validação de fluxos antes da execução

## Tecnologias

- Flask (Python)
- PostgreSQL
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
DATABASE_URL=postgresql://iara_user:iara_password@localhost:5432/iara_flow_db
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

### Deploy na AWS EC2

O backend foi configurado e está rodando em uma instância AWS EC2 t2.micro.

**Detalhes da Instância EC2:**
- **IP Público:** `54.162.170.1`
- **Porta do Backend:** `5000`

**Acesso SSH à Instância EC2:**
Para acessar a instância via SSH, utilize o par de chaves (`iara-flow-key.pem`) e o usuário `ubuntu`:
```bash
ssh -i iara-flow-key.pem ubuntu@54.162.170.1
```

**Detalhes do Banco de Dados PostgreSQL:**
- **Host:** `localhost` (acessível da própria instância EC2)
- **Porta:** `5432`
- **Nome do Banco de Dados:** `iara_flow_db`
- **Usuário:** `iara_user`
- **Senha:** `iara_password`

**Acesso ao Backend:**
O backend está rodando na porta `5000`. Você pode acessá-lo através do IP público da instância:
`http://54.162.170.1:5000`

**Observação de Segurança:** As portas 22 (SSH), 80 (HTTP) e 5000 (Backend) estão abertas no grupo de segurança. Para um ambiente de produção, é altamente recomendável restringir o acesso a essas portas apenas aos IPs necessários.

## Estrutura do Projeto

```
├── src/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── models/              # Modelos de dados
│   ├── routes/              # Rotas da API
│   └── services/            # Serviços (IA, PostgreSQL, Executor)
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


