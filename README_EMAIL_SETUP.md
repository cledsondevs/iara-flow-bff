# Configuração de E-mail para Iara Flow

Este documento explica como configurar o envio de e-mails no sistema Iara Flow para relatórios de backlog e análises de reviews.

## 📧 Funcionalidades de E-mail

O sistema agora envia automaticamente e-mails quando:
1. **Backlog é gerado**: Relatório detalhado com itens de alta prioridade
2. **Reviews negativos são detectados**: Relatório executivo para gerentes

## ⚙️ Configuração

### 1. Copiar arquivo de configuração
```bash
cp .env.example .env
```

### 2. Configurar variáveis de ambiente no arquivo `.env`

#### Para Gmail:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_aplicativo
SENDER_EMAIL=seu_email@gmail.com
```

**⚠️ Importante para Gmail:**
- Use uma "Senha de Aplicativo" em vez da senha normal
- Ative a verificação em duas etapas
- Gere uma senha de aplicativo em: https://myaccount.google.com/apppasswords

#### Para SendGrid:
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=sua_api_key_sendgrid
SENDER_EMAIL=remetente_verificado@seudominio.com
```

#### Para Mailgun:
```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=seu_usuario_mailgun
SMTP_PASSWORD=sua_senha_mailgun
SENDER_EMAIL=remetente_verificado@seudominio.com
```

#### Para Outlook/Hotmail:
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@outlook.com
SMTP_PASSWORD=sua_senha
SENDER_EMAIL=seu_email@outlook.com
```

### 3. Configurar e-mail de teste (opcional)
```env
TEST_EMAIL=seu_email_teste@exemplo.com
```

## 🧪 Testando a Configuração

Execute o script de teste para verificar se tudo está funcionando:

```bash
cd iara-flow-bff
python test_email_functionality.py
```

O script irá:
- ✅ Verificar se todas as variáveis estão configuradas
- 📧 Enviar um e-mail de teste de backlog
- 📊 Enviar um e-mail de teste de relatório executivo

## 🚀 Como Usar

### 1. Via API - Gerar Backlog com E-mail

```bash
curl -X POST http://localhost:5000/api/review-agent/apps/com.exemplo.app/backlog \
  -H "Content-Type: application/json" \
  -d 
```

### 2. Via Código Python

```python
from app.services.backlog_generator_service import BacklogGeneratorService

# Instanciar serviço
backlog_service = BacklogGeneratorService()

# Gerar backlog e enviar e-mail
result = backlog_service.process_reviews_to_backlog(
    package_name="com.exemplo.app",
    days=7,
    recipient_email="gerente@empresa.com"
)

# Verificar resultado do e-mail
if result.get(\'email_result\'):
    print(f"E-mail: {result[\'email_result\'][\'status\']}")
```

## 📋 Estrutura dos E-mails

### Relatório de Backlog
- **Assunto**: "Relatório de Backlog Gerado - [Nome do App]"
- **Conteúdo**:
  - Resumo executivo com métricas
  - Itens de alta prioridade (≥4)
  - Resumo por categoria
  - Detalhes dos itens por categoria
  - Próximos passos recomendados

### Relatório Executivo de Reviews
- **Assunto**: "Relatório Executivo de Reviews Negativos - [Nome do App]"
- **Conteúdo**:
  - Resumo geral de reviews negativos
  - Reviews mais críticos
  - Principais temas identificados
  - Sugestões de ações

## 🔧 Solução de Problemas

### Erro: "Configurações de SMTP incompletas"
- Verifique se todas as variáveis obrigatórias estão no `.env`
- Variáveis obrigatórias: `SMTP_SERVER`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SENDER_EMAIL`

### Erro de autenticação SMTP
- **Gmail**: Use senha de aplicativo, não a senha normal
- **Outlook**: Verifique se a conta permite SMTP
- **SendGrid/Mailgun**: Verifique se a API key está correta

### E-mails não chegam
- Verifique a pasta de spam
- Confirme se o e-mail remetente está verificado no provedor
- Teste com um e-mail real definindo TEST_EMAIL no .env

### Erro de conexão
- Verifique se a porta SMTP está correta (587 para TLS, 465 para SSL)
- Confirme se o servidor SMTP está acessível

## 📝 Logs e Debugging

Para ver logs detalhados, execute com debug:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Seu código aqui
```

## 🔒 Segurança

- **Nunca** commite o arquivo `.env` no repositório
- Use senhas de aplicativo quando disponível
- Mantenha as credenciais seguras
- Considere usar variáveis de ambiente do sistema em produção

## 📞 Suporte

Se encontrar problemas:
1. Execute o script de teste: `python test_email_functionality.py`
2. Verifique os logs de erro
3. Consulte a documentação do seu provedor de e-mail
4. Teste com configurações mínimas primeiro

