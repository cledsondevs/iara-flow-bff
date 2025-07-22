# Deploy do Iara Flow BFF

Este documento contém instruções para fazer o deploy do back-end do Iara Flow.

## Pré-requisitos

- Docker
- Docker Compose
- Git

## Configuração

1. **Clone o repositório** (se ainda não foi feito):
```bash
git clone https://github.com/cledsondevs/iara-flow-bff.git
cd iara-flow-bff
```

2. **Configure as variáveis de ambiente**:
```bash
cp .env.example .env
nano .env
```

Configure as seguintes variáveis no arquivo `.env`:

### Variáveis Obrigatórias:
```env
# OpenAI API
OPENAI_API_KEY=sua_openai_api_key

# Gemini API (opcional)
GEMINI_API_KEY=sua_gemini_api_key

# Configurações de E-mail (para relatórios)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
SENDER_EMAIL=seu_email@gmail.com
MANAGER_EMAIL=gerente@empresa.com

# Banco de dados
DB_PATH=/app/data/iara_flow.db
```

### Configuração de E-mail (Exemplos):

**Gmail:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
```

**SendGrid:**
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=sua_sendgrid_api_key
```

**Mailgun:**
```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@seu_dominio.mailgun.org
SMTP_PASSWORD=sua_mailgun_password
```

## Deploy

### Opção 1: Script Automático
```bash
./deploy.sh
```

### Opção 2: Manual
```bash
# Parar containers existentes
docker-compose down

# Construir e iniciar
docker-compose up -d --build

# Verificar logs
docker-compose logs -f
```

## Verificação

Após o deploy, verifique se a aplicação está funcionando:

```bash
curl http://localhost:5000/
```

Resposta esperada:
```json
{
  "status": "ok",
  "message": "Iara Flow BFF is running"
}
```

## Endpoints Principais

- `GET /` - Health check
- `POST /api/review-agent/apps/{package_name}/collect` - Coletar reviews
- `POST /api/review-agent/apps/{package_name}/analyze` - Analisar sentimento
- `POST /api/review-agent/apps/{package_name}/backlog` - Gerar backlog
- `POST /api/review-agent/send-report-email` - Enviar relatório por e-mail

## Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar aplicação
docker-compose down

# Reiniciar aplicação
docker-compose restart

# Acessar container
docker-compose exec iara-flow-bff bash

# Ver status dos containers
docker-compose ps
```

## Troubleshooting

### Erro de permissão no banco de dados
```bash
# Criar diretório de dados com permissões corretas
mkdir -p data
chmod 755 data
```

### Erro de conexão com APIs externas
- Verifique se as APIs externas estão acessíveis:
  - `http://200.98.64.133:5000/api/scraping/google-play/com.itau.investimentos`
  - `http://200.98.64.133:5000/api/scraping/apple-store/1531733746`

### Erro de envio de e-mail
- Verifique as configurações SMTP no arquivo `.env`
- Para Gmail, use senha de app em vez da senha normal
- Teste a conexão SMTP manualmente

## Monitoramento

### Health Check
O container possui um health check automático que verifica se a aplicação está respondendo.

### Logs
Os logs são salvos automaticamente pelo Docker. Use `docker-compose logs` para visualizá-los.

## Backup

### Banco de Dados
```bash
# Fazer backup do banco
docker-compose exec iara-flow-bff cp /app/data/iara_flow.db /app/data/backup_$(date +%Y%m%d_%H%M%S).db

# Copiar backup para o host
docker cp $(docker-compose ps -q iara-flow-bff):/app/data/backup_*.db ./
```

## Atualizações

Para atualizar a aplicação:

```bash
# Fazer backup
./backup.sh

# Atualizar código
git pull origin main

# Reconstruir e reiniciar
docker-compose down
docker-compose up -d --build
```

