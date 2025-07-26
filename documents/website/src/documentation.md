# Documentação da API Iara Flow

Esta documentação detalha as funcionalidades e endpoints da API Iara Flow, um backend robusto e escalável projetado para gerenciar interações com modelos de linguagem avançados, como Gemini, OpenAI e Groq, além de integrar um agente LangChain para tarefas complexas. A API foi desenvolvida com foco em persistência de memória, autenticação segura e flexibilidade para futuras expansões.

## Visão Geral do Sistema

A API Iara Flow atua como um intermediário entre aplicações cliente e diversos provedores de IA, oferecendo uma camada unificada para interações de chat e gerenciamento de memória. O sistema é modular, permitindo fácil adição de novos provedores e funcionalidades. A persistência de memória é um pilar central, garantindo que as conversas e informações do usuário sejam mantidas ao longo do tempo, independentemente da sessão.

## Changelog Recente

As seguintes mudanças significativas foram implementadas recentemente, conforme detalhado no `CHANGELOG.md` do projeto:

### Adicionado

#### Sistema de Memória Isolado V2 (Persistência por Usuário)

Uma reformulação completa do sistema de memória foi implementada para garantir a persistência de conversas e informações por `user_id`, desvinculando-se da `session_id`. Isso permite que o histórico de conversas e os fatos salvos sejam mantidos para um usuário específico, mesmo que ele inicie novas sessões ou utilize diferentes dispositivos.

**Novas Rotas API V2 para Chat Gemini:**

| Método | Endpoint                     | Descrição                                                              |
|--------|------------------------------|------------------------------------------------------------------------|
| `POST` | `/api/v2/chat/gemini`        | Chat principal com memória persistente.                                |
| `GET`  | `/api/v2/chat/gemini/memory` | Recupera todo o histórico de memória do usuário.                       |
| `DELETE`| `/api/v2/chat/gemini/memory` | Limpa toda a memória do usuário.                                       |
| `GET`  | `/api/v2/chat/gemini/stats`  | Obtém estatísticas de uso da memória do usuário.                       |
| `PUT`  | `/api/v2/chat/gemini/profile`| Atualiza o perfil do usuário.                                          |
| `POST` | `/api/v2/chat/gemini/fact`   | Salva fatos específicos sobre o usuário.                               |
| `GET`  | `/api/v2/chat/gemini/context`| Obtém o contexto completo da conversa do usuário.                      |
| `GET`  | `/api/v2/chat/health`        | Health check para o serviço V2.                                        |
| `POST` | `/api/v2/chat/migrate`       | Endpoint para futuras migrações de dados.                              |

**Persistência de Histórico por `user_id`:**

- A função `get_conversation_history_isolated` no `IsolatedMemoryService` agora busca o histórico apenas por `user_id`, ignorando a `session_id`.
- O `GeminiChatServiceV2` foi ajustado para utilizar este histórico expandido para construir o contexto da conversa.

**Comandos de Memória Aprimorados:**

- A funcionalidade "Lembre-se disso:" agora utiliza o novo sistema de memória isolado, garantindo que os fatos sejam persistidos por `user_id`.

#### Memória de Longo Prazo para Chats

Implementação de um sistema de memória persistente para os endpoints de chat Gemini e OpenAI, permitindo que as conversas sejam mantidas e recuperadas em diferentes sessões. Isso inclui:

- Novos endpoints `/api/gemini/chat` e `/api/openai/chat` com memória de longo prazo.
- Endpoints para gerenciar memória: `GET` e `DELETE` para `/api/gemini/memory` e `/api/openai/memory`.
- Endpoint de verificação de saúde: `/api/chat/health`.
- Sistema de sessões para isolar conversas por usuário e sessão.
- Armazenamento persistente de conversas no banco SQLite.
- Contexto de conversa mantido entre sessões diferentes.

#### Memória de Longo Prazo para LangChain Agent

Extensão da funcionalidade de memória persistente para o agente LangChain, garantindo que o histórico de conversas seja mantido entre reinicializações do servidor. A integração com ferramentas (web_search, file operations) é preservada, e metadados aprimorados, incluindo ferramentas utilizadas e tipo de agente, são registrados.

#### Suporte ao Groq Chat

Um novo provedor de IA, Groq, foi adicionado ao sistema de chat, oferecendo modelos rápidos e eficientes. Isso inclui:

- Novo endpoint `/api/groq/chat` com memória de longo prazo.
- Endpoints para gerenciar memória: `GET` e `DELETE` para `/api/groq/memory`.
- Endpoint para listar modelos disponíveis: `/api/groq/models`.
- Suporte a múltiplos modelos Groq (llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it).
- Integração completa com o sistema de memória unificado.

#### Memória Global por Usuário

Um sistema de perfil persistente que transcende sessões individuais foi implementado, utilizando uma nova tabela `user_profiles` para armazenar informações globais do usuário. Isso permite:

- Extração automática de informações pessoais das mensagens (nome, profissão, idade).
- Contexto do usuário incluído automaticamente em todas as conversas.
- Funcionamento em todos os provedores: Gemini, OpenAI, Groq e LangChain.
- O assistente "lembra" do usuário mesmo em sessões diferentes.

#### Funcionalidade "Lembre-se disso"

Um sistema de salvamento explícito de informações pelo usuário foi adicionado, permitindo que o usuário salve fatos importantes para serem lembrados em futuras interações. Isso inclui:

- Palavras-chave para salvar fatos: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:".
- Detecção automática e extração de fatos das mensagens do usuário.
- Fatos salvos são incluídos automaticamente no contexto de futuras conversas.
- Funcionamento em todos os provedores de IA (Gemini, OpenAI, Groq, LangChain).
- Limite de 10 fatos por usuário para otimização de performance.
- Confirmação visual quando um fato é salvo (✅ Informação salva na memória!).

### Removido

#### Código da Versão 1 (V1) do Sistema de Memória e Chat

Para otimizar e modernizar o codebase, o código da versão 1 do sistema de memória e chat foi removido. Isso inclui:

- `app/chats/routes/chat_routes.py` (Rotas de chat V1).
- `app/services/memory_service.py` (Serviço de memória V1).
- `app/services/enhanced_memory_service.py` (Serviço de memória aprimorado V1).
- `app/chats/services/gemini_chat_service.py` (Serviço de chat Gemini V1).
- Todas as importações e registros relacionados à V1 foram removidos do `app/main.py`.

### Corrigido

#### Problemas Críticos de Salvamento e Acesso de Memórias

Diversos problemas críticos relacionados ao salvamento e acesso de memórias foram resolvidos, incluindo:

- Correção de problemas de `DEFAULT (lower(hex(randomblob(16))))` em todas as tabelas.
- Remoção de expressões SQL incompatíveis que causavam erros de criação de tabelas.
- Correção dos arquivos: `backlog_generator_service.py`, `dashboard_service.py`, `review_collector_service.py`.
- O sistema de memória de curto e longo prazo agora funciona corretamente.
- Conversas são salvas e recuperadas adequadamente.

#### Dados Padrão Implementados no Banco de Dados

Um script `create_sample_data.py` foi criado para popular o banco de dados com dados de exemplo, garantindo que o banco não fique vazio após a inicialização. Isso inclui:

- Inserção de 3 usuários padrão: `admin`, `demo_user`, `test_user`.
- Criação de 3 conversas de exemplo com o sistema de memória funcionando.
- Inserção de 3 reviews de exemplo para testes.

#### Problema Crítico de Bloqueio do Banco de Dados SQLite

O problema crítico de bloqueio do banco de dados SQLite foi resolvido através da implementação de gerenciamento adequado de conexões usando context managers. Isso resultou em:

- Correção de todas as funções de autenticação para usar `with get_db_connection()`.
- Eliminação de vazamentos de conexão que causavam bloqueios.
- Adição do script `fix_database_lock.py` para diagnóstico e correção de bloqueios.

#### APIs de Login Totalmente Funcionais

As APIs de login foram corrigidas e agora estão totalmente funcionais, incluindo:

- Correção de rotas de autenticação com prefixos incorretos.
- Resolução do erro "405 METHOD NOT ALLOWED".
- Todas as rotas de autenticação agora funcionam corretamente:
  - `POST /api/auth/register` - Registro de usuários.
  - `POST /api/auth/login` - Login de usuários.
  - `POST /api/auth/logout` - Logout de usuários.
  - `POST /api/auth/verify` - Verificação de sessão.
  - `GET /api/auth/user/<id>` - Obter dados do usuário.

#### Sistema de Configuração de Chaves de API Restaurado

O sistema de configuração de chaves de API foi restaurado e agora funciona corretamente, permitindo o armazenamento e recuperação de chaves. Isso inclui:

- Correção das rotas de API keys: `POST /api/keys` e `GET /api/keys/<user_id>/<service_name>`.
- Adição de imports necessários no arquivo `api_key_routes.py`.

#### Tabelas de Memória de Longo Prazo Criadas Corretamente

A criação automática das tabelas `conversations` e `user_profiles` foi corrigida, e o `MemoryService` agora usa a configuração centralizada do banco. Isso garante:

- Criação automática do diretório `data/` se não existir.
- Sincronização entre todos os serviços de banco de dados.

#### Configuração de Banco de Dados Unificada

A configuração do banco de dados foi unificada em `Config.DATABASE_PATH`, garantindo consistência entre todos os arquivos (`auth_routes.py`, `memory_service.py`, `database.py`) e a criação automática de diretórios em todos os pontos de acesso.

#### Usuário Padrão Criado Automaticamente

A criação automática de um usuário administrador na inicialização foi implementada, com as credenciais `admin` / `admin` (email: `admin@iaraflow.com`). Um script independente `create_default_user.py` também foi fornecido para criação manual.

#### Dependências Instaladas e Configuradas

Todas as dependências necessárias (Flask, LangChain, Google AI, etc.) foram instaladas e configuradas, garantindo que a aplicação Flask inicialize corretamente sem erros de módulos e que todas as funcionalidades principais estejam operacionais.

## Detalhes Técnicos

- Implementado padrão de context manager para conexões SQLite.
- Eliminados bloqueios de banco através de gerenciamento adequado de recursos.
- Corrigidas estruturas try/except aninhadas que causavam problemas de sintaxe.
- Adicionado tratamento robusto de erros em todas as operações de banco.

## Testes

- ✅ Login com usuário padrão (admin/admin) funcionando.
- ✅ Registro de novos usuários funcionando.
- ✅ Verificação de sessão funcionando.
- ✅ Obtenção de dados de usuário funcionando.
- ✅ Configuração de chaves de API funcionando.
- ✅ Recuperação de chaves de API funcionando.
- ✅ Banco de dados sem bloqueios.
  - Criação automática do diretório `data/` se não existir.
  - Tabelas `conversations` e `user_profiles` criadas corretamente na inicialização.
  - Sincronização entre `init_database()` e `MemoryService._init_sqlite_tables()`.

## Notas

- O sistema mantém compatibilidade com a estrutura existente do projeto.
- As conversas são armazenadas de forma segura no banco SQLite local.
- Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário.
- O histórico é limitado às últimas 20 interações por sessão para otimização de performance.
- **LangChain Agent**: Mantém todas as funcionalidades originais (ferramentas, busca web, operações de arquivo) com memória persistente.
- **Groq**: Oferece modelos rápidos e eficientes, incluindo Llama 3 e Mixtral.
- **Memória Global**: Permite que o assistente "lembre" do usuário mesmo em diferentes sessões.
  - Funciona automaticamente: quando o usuário diz seu nome, é salvo no perfil.
  - Contexto é incluído em todas as conversas futuras daquele `user_id`.
  - Informações persistem mesmo após reinicialização do servidor.
- **Sistema "Lembre-se disso"**: Controle total do usuário sobre o que é salvo.
  - Palavras-chave: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:".
  - Funciona em qualquer provedor (Gemini, OpenAI, Groq, LangChain).
  - Fatos são incluídos automaticamente em futuras conversas.
  - Exemplo: "lembre-se disso: eu andei de bicicleta no sábado" → salvo permanentemente.
- Todos os quatro provedores (Gemini, OpenAI, Groq, LangChain) agora compartilham o mesmo sistema de memória unificado.
- Sistema escalável para adição de novos provedores de IA no futuro.
- **Exemplo de uso completo**: 
  - Sessão 1: "Meu nome é João" + "lembre-se disso: gosto de café"
  - Sessão 2 (semana depois): Assistente sabe.

