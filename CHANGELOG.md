# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **APIs de Login**: Corrigidas rotas de autenticação que estavam com prefixos incorretos
  - Rota `/api/auth/register` corrigida para `/register` (com blueprint prefix `/api/auth`)
  - Rota `/api/auth/login` corrigida para `/login` (com blueprint prefix `/api/auth`)
  - Rota `/api/auth/logout` corrigida para `/logout` (com blueprint prefix `/api/auth`)
  - Rota `/api/auth/verify` corrigida para `/verify` (com blueprint prefix `/api/auth`)
  - Rota `/api/auth/user/<id>` corrigida para `/user/<id>` (com blueprint prefix `/api/auth`)
  - Problema de "405 METHOD NOT ALLOWED" resolvido

- **Tabela de Memória de Longo Prazo**: Corrigidos problemas na criação e inicialização das tabelas
  - MemoryService agora usa configuração centralizada do banco de dados
  - Criação automática do diretório `data/` se não existir
  - Tabelas `conversations` e `user_profiles` criadas corretamente na inicialização
  - Sincronização entre `init_database()` e `MemoryService._init_sqlite_tables()`

- **Configuração de Banco de Dados**: Unificada configuração de caminho do banco
  - Todos os serviços agora usam `Config.DATABASE_PATH` ao invés de caminhos hardcoded
  - Criação automática do diretório do banco em todos os pontos de acesso
  - Consistência entre `auth_routes.py`, `memory_service.py` e `database.py`

### Added
- **Usuário Padrão**: Criação automática de usuário administrador na inicialização
  - Username: `admin`
  - Password: `admin`
  - Email: `admin@iaraflow.com`
  - Criado automaticamente se não existir durante a inicialização da aplicação
  - Script independente `create_default_user.py` para criação manual

### Changed
- **Inicialização da Aplicação**: Melhorada sequência de inicialização
  - Banco de dados inicializado primeiro
  - MemoryService inicializado em seguida
  - Usuário padrão criado automaticamente
  - Logs informativos para cada etapa da inicialização

### Technical Details
- **Arquivos modificados**:
  - `app/auth/auth_routes.py` - Corrigidas rotas e configuração de banco
  - `app/services/memory_service.py` - Unificada configuração de banco e criação de diretório
  - `app/main.py` - Adicionada criação automática de usuário padrão
  - `app/utils/database.py` - Mantida consistência na configuração

- **Arquivos criados**:
  - `create_default_user.py` - Script para criação manual de usuário padrão

### Notes
- As APIs de autenticação agora funcionam corretamente com os endpoints esperados
- O sistema de memória de longo prazo está totalmente funcional
- Usuário padrão permite acesso imediato ao sistema após instalação
- Todas as configurações de banco de dados estão centralizadas em `Config.DATABASE_PATH`

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

- **Memória Global por Usuário**: Sistema de perfil persistente que transcende sessões individuais
  - Nova tabela `user_profiles` para armazenar informações globais do usuário
  - Extração automática de informações pessoais das mensagens (nome, profissão, idade)
  - Contexto do usuário incluído automaticamente em todas as conversas
  - Funciona em todos os provedores: Gemini, OpenAI, Groq e LangChain
  - Permite que o assistente "lembre" do usuário mesmo em sessões diferentes

- **Funcionalidade "Lembre-se disso"**: Sistema de salvamento explícito de informações pelo usuário
  - Palavras-chave para salvar fatos: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:"
  - Detecção automática e extração de fatos das mensagens do usuário
  - Fatos salvos são incluídos automaticamente no contexto de futuras conversas
  - Funciona em todos os provedores de IA (Gemini, OpenAI, Groq, LangChain)
  - Limite de 10 fatos por usuário para otimização de performance
  - Confirmação visual quando um fato é salvo (✅ Informação salva na memória!)

### Changed
- Estrutura do projeto expandida com novos serviços de chat
- **LangChain Agent Service**: Refatorado para usar memória persistente ao invés de memória em tempo de execução
  - Modelo atualizado para `gpt-4o-mini` (compatibilidade com API)
  - Histórico de conversa limitado a 20 mensagens para otimização
  - Ordem cronológica corrigida para manter contexto adequado
- **Sistema de Chat**: Expandido para suportar quatro provedores de IA (Gemini, OpenAI, Groq, LangChain)
- **Endpoint de Health Check**: Atualizado para incluir todos os serviços disponíveis
- **MemoryService**: Expandido com funcionalidades de perfil global por usuário e salvamento explícito
  - Método `save_message_with_profile_update()` para extração automática de informações
  - Método `get_user_context_for_chat()` para incluir contexto em conversas
  - Método `extract_user_info_from_message()` para análise de mensagens
  - Método `detect_and_save_user_fact()` para processamento de comandos "Lembre-se disso"
  - Método `save_user_fact()` para salvamento de fatos específicos
  - Método `get_user_facts()` para recuperação de fatos salvos
  - Método `remove_user_fact()` para remoção de fatos específicos
- **Todos os Serviços de Chat**: Atualizados para usar memória global por usuário e funcionalidade "Lembre-se disso"
  - Processamento automático de palavras-chave para salvamento de fatos
  - Confirmação visual quando informações são salvas
  - Metadados aprimorados incluindo flag `fact_saved`
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
  - `test_global_memory.py` - Script de teste para validação da memória global por usuário
  - `test_remember_this.py` - Script de teste para validação da funcionalidade "Lembre-se disso"
  - `README_MEMORY_IMPLEMENTATION.md` - Documentação técnica da implementação

- **Arquivos modificados**:
  - `src/services/memory_service.py` - Adicionada funcionalidade de perfil global por usuário e "Lembre-se disso"
  - `src/services/langchain_agent_service.py` - Integração com memória de longo prazo, global e "Lembre-se disso"
  - `src/services/gemini_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
  - `src/services/openai_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
  - `src/services/groq_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso"
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
  - **Memória global por usuário**: Perfil persistente que transcende sessões
  - **Extração automática**: Detecção de nome, profissão e idade nas mensagens
  - **Contexto inteligente**: Informações do usuário incluídas automaticamente em conversas
  - **Sistema "Lembre-se disso"**: Salvamento explícito de fatos pelo usuário
  - **Palavras-chave inteligentes**: Detecção automática de comandos de salvamento
  - **Confirmação visual**: Feedback imediato quando informações são salvas
  - **Gestão de fatos**: Limite automático e prevenção de duplicatas

### Notes
- O sistema mantém compatibilidade com a estrutura existente do projeto
- As conversas são armazenadas de forma segura no banco SQLite local
- Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário
- O histórico é limitado às últimas 20 interações por sessão para otimização de performance
- **LangChain Agent**: Mantém todas as funcionalidades originais (ferramentas, busca web, operações de arquivo) com memória persistente
- **Groq**: Oferece modelos rápidos e eficientes, incluindo Llama 3 e Mixtral
- **Memória Global**: Permite que o assistente "lembre" do usuário mesmo em diferentes sessões
  - Funciona automaticamente: quando o usuário diz seu nome, é salvo no perfil
  - Contexto é incluído em todas as conversas futuras daquele `user_id`
  - Informações persistem mesmo após reinicialização do servidor
- **Sistema "Lembre-se disso"**: Controle total do usuário sobre o que é salvo
  - Palavras-chave: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:"
  - Funciona em qualquer provedor (Gemini, OpenAI, Groq, LangChain)
  - Fatos são incluídos automaticamente em futuras conversas
  - Exemplo: "lembre-se disso: eu andei de bicicleta no sábado" → salvo permanentemente
- Todos os quatro provedores (Gemini, OpenAI, Groq, LangChain) agora compartilham o mesmo sistema de memória unificado
- Sistema escalável para adição de novos provedores de IA no futuro
- **Exemplo de uso completo**: 
  - Sessão 1: "Meu nome é João" + "lembre-se disso: gosto de café"
  - Sessão 2 (semana depois): Assistente sabe que é João e que ele gosta de café

