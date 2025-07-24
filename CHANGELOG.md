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

- **Memória de Longo Prazo para LangChain Agent**: Extensão da funcionalidade de memória persistente para o agente LangChain
  - Endpoint `/api/agent/chat` agora utiliza memória de longo prazo
  - Histórico de conversas mantido entre reinicializações do servidor
  - Integração com ferramentas (web_search, file operations) preservada
  - Metadados aprimorados incluindo ferramentas utilizadas e tipo de agente

- **Suporte ao Groq Chat**: Novo provedor de IA adicionado ao sistema de chat
  - Novo endpoint `/api/groq/chat` com memória de longo prazo
  - Endpoints para gerenciar memória: GET e DELETE para `/api/groq/memory`
  - Endpoint para listar modelos disponíveis: `/api/groq/models`
  - Suporte a múltiplos modelos Groq (llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it)
  - Integração completa com sistema de memória unificado

### Changed
- Estrutura do projeto expandida com novos serviços de chat
- **LangChain Agent Service**: Refatorado para usar memória persistente ao invés de memória em tempo de execução
  - Modelo atualizado para `gpt-4.1-mini` (compatibilidade com API)
  - Histórico de conversa limitado a 20 mensagens para otimização
  - Ordem cronológica corrigida para manter contexto adequado
- **Sistema de Chat**: Expandido para suportar quatro provedores de IA (Gemini, OpenAI, Groq, LangChain)
- **Endpoint de Health Check**: Atualizado para incluir todos os serviços disponíveis
- Sistema de memória aprimorado para suportar múltiplos provedores de IA

### Technical Details
- **Novos arquivos criados**:
  - `src/services/gemini_chat_service.py` - Serviço para integração com Google Gemini
  - `src/services/openai_chat_service.py` - Serviço para integração com OpenAI
  - `src/services/groq_chat_service.py` - Serviço para integração com Groq
  - `src/routes/chat_routes.py` - Rotas para endpoints de chat
  - `test_gemini_chat.py` - Script de teste para validação do chat Gemini
  - `test_langchain_memory.py` - Script de teste para validação da memória do LangChain
  - `test_groq_chat.py` - Script de teste para validação do chat Groq
  - `README_MEMORY_IMPLEMENTATION.md` - Documentação técnica da implementação

- **Arquivos modificados**:
  - `src/services/langchain_agent_service.py` - Integração com memória de longo prazo
  - `src/main.py` - Registro das novas rotas de chat
  - `.env` - Configuração das chaves de API

- **Dependências adicionadas**:
  - `google-generativeai` - SDK oficial do Google Gemini
  - `groq` - SDK oficial do Groq
  - Configuração de variáveis de ambiente para `GEMINI_API_KEY` e `GROQ_API_KEY`

- **Funcionalidades implementadas**:
  - Recuperação automática do histórico de conversas para todos os provedores
  - Construção de contexto para manter continuidade das conversas
  - Isolamento de sessões por `user_id` e `session_id`
  - Metadados de uso e estatísticas para cada interação
  - Tratamento de erros robusto em todos os serviços
  - Suporte a diferentes modelos OpenAI e Groq via parâmetro opcional
  - Integração transparente do LangChain com ferramentas e memória persistente
  - Endpoint para listar modelos disponíveis do Groq

### Notes
- O sistema mantém compatibilidade com a estrutura existente do projeto
- As conversas são armazenadas de forma segura no banco SQLite local
- Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário
- O histórico é limitado às últimas 20 interações por sessão para otimização de performance
- **LangChain Agent**: Mantém todas as funcionalidades originais (ferramentas, busca web, operações de arquivo) com memória persistente
- **Groq**: Oferece modelos rápidos e eficientes, incluindo Llama 3 e Mixtral
- Todos os quatro provedores (Gemini, OpenAI, Groq, LangChain) agora compartilham o mesmo sistema de memória unificado
- Sistema escalável para adição de novos provedores de IA no futuro

