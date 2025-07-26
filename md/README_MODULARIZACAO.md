# Modularização do Iara Flow BFF

## Resumo das Alterações

Este documento descreve as alterações realizadas na modularização do backend Iara Flow BFF.

## Nova Estrutura do Projeto

```
app/
├── __init__.py
├── main.py                    # Aplicação principal modularizada
├── config/
│   ├── __init__.py
│   └── settings.py           # Configurações centralizadas
├── utils/
│   ├── __init__.py
│   └── database.py           # Utilitários de banco de dados
├── auth/
│   ├── __init__.py
│   ├── routes.py             # Rotas de autenticação
│   └── middleware.py         # Middleware de autenticação
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── agent_routes.py   # Rotas do agente
│       └── review_agent_routes.py
├── models/                   # Modelos de dados
│   ├── __init__.py
│   ├── flow.py
│   └── review_models.py
└── services/                 # Serviços de negócio
    ├── __init__.py
    ├── langchain_agent_service.py
    ├── memory_service.py
    ├── review_agent_service.py
    └── ...
```

## Principais Melhorias

### 1. Estrutura Modularizada
- Separação clara de responsabilidades
- Organização por funcionalidades
- Facilita manutenção e escalabilidade

### 2. Configurações Centralizadas
- Arquivo `app/config/settings.py` com todas as configurações
- Suporte a diferentes ambientes (desenvolvimento/produção)
- Variáveis de ambiente organizadas

### 3. Sistema de Autenticação Corrigido
- **Problema Original**: Rotas de autenticação não estavam registradas no `main.py`
- **Solução**: Criado blueprint `auth_bp` e registrado corretamente
- **Resultado**: Erro 405 resolvido

### 4. Utilitários de Banco de Dados
- Função centralizada para conexão com SQLite
- Inicialização automática de todas as tabelas
- Melhor tratamento de erros

### 5. Middleware de Autenticação
- Decorator `@require_auth` para proteger rotas
- Verificação automática de tokens de sessão
- Informações do usuário disponíveis no request

## Testes Realizados

### API de Autenticação
- ✅ Health Check: `GET /`
- ✅ Registro: `POST /api/auth/register`
- ✅ Login: `POST /api/auth/login`
- ✅ Verificação de Sessão: `POST /api/auth/verify`
- ✅ Informações do Usuário: `GET /api/auth/user/{id}`

### Usuário de Teste Criado
- **Username**: `usuario_teste`
- **Password**: `senha123`
- **Email**: `teste@exemplo.com`
- **User ID**: 1

## Como Executar

### Aplicação Principal
```bash
cd iara-flow-bff
python3 app/main.py
```

### Aplicação de Teste Simplificada
```bash
cd iara-flow-bff
python3 simple_test_app.py
```

### Testes da API
```bash
cd iara-flow-bff
python3 test_api.py
```

## Arquivos de Configuração

### `.env`
Certifique-se de que as seguintes variáveis estão configuradas:
```
SECRET_KEY=asdf#FGSgvasgf
DB_PATH=./iara_flow.db
OPENAI_API_KEY=sua_chave_aqui
DEBUG=False
PORT=5000
```

## Próximos Passos

1. **Testes Unitários**: Implementar testes automatizados
2. **Documentação da API**: Swagger/OpenAPI
3. **Logging**: Sistema de logs estruturado
4. **Validação**: Schemas de validação para requests
5. **Cache**: Implementar cache para melhor performance
6. **Monitoramento**: Métricas e health checks avançados

## Dependências

Todas as dependências estão listadas no `requirements.txt`. Para instalar:

```bash
pip3 install -r requirements.txt
```

## Problemas Conhecidos

1. **Erro nas tabelas aprimoradas**: Mensagem de erro sobre PRIMARY KEY constraints - não afeta funcionalidade
2. **Timeout em alguns testes**: Pode ser necessário ajustar timeouts dependendo do ambiente

## Contribuição

Para contribuir com o projeto:

1. Crie uma nova branch a partir de `feature/modularizacao-backend`
2. Faça suas alterações
3. Teste localmente
4. Crie um Pull Request

