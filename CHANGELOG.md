# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Memória de Longo Prazo para Chats**: Implementação de sistema de memória persistente para os endpoints de chat Gemini e OpenAI
  - Novo endpoint `/api/gemini/chat` com memória de longo prazo
  - Novo endpoint `/api/openai/chat` com memória de longo prazo
  - Endpoints para gerenciar memória: GET e DELETE para `/api/gemini/memory` e `/api/openai/memory`
  - Endpoint de verificação de saúde: `/api/chat/health`
  - Sistema de sessões para isolar conversas por usuário e sessão
  - Armazenamento persistente de conversas no banco SQLite
  - Contexto de conversa mantido entre sessões diferentes

### Changed
- Estrutura do projeto expandida com novos serviços de chat
- Sistema de memória aprimorado para suportar múltiplos provedores de IA

### Technical Details
- **Novos arquivos criados**:
  - `src/services/gemini_chat_service.py` - Serviço para integração com Google Gemini
  - `src/services/openai_chat_service.py` - Serviço para integração com OpenAI
  - `src/routes/chat_routes.py` - Rotas para endpoints de chat
  - `test_gemini_chat.py` - Script de teste para validação do chat Gemini

- **Dependências adicionadas**:
  - `google-generativeai` - SDK oficial do Google Gemini
  - Configuração de variáveis de ambiente para `GEMINI_API_KEY`

- **Funcionalidades implementadas**:
  - Recuperação automática do histórico de conversas
  - Construção de contexto para manter continuidade das conversas
  - Isolamento de sessões por `user_id` e `session_id`
  - Metadados de uso e estatísticas para cada interação
  - Tratamento de erros robusto
  - Suporte a diferentes modelos OpenAI via parâmetro opcional

### Notes
- O sistema mantém compatibilidade com a estrutura existente do projeto
- As conversas são armazenadas de forma segura no banco SQLite local
- Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário
- O histórico é limitado às últimas 20 interações por sessão para otimização de performance

