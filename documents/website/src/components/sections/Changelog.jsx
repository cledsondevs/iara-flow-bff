import React from 'react';

const Changelog = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow-lg">
      <h1 className="text-4xl font-bold mb-6 text-foreground">Histórico de Mudanças (Changelog)</h1>
      
      <div className="space-y-8 text-muted-foreground">
        {/* Unreleased Section */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">[Unreleased]</h2>
          <p className="text-sm text-gray-500 mb-4">26 de Julho de 2025</p>
          
          <h3 className="text-xl font-semibold text-primary mb-2">Adicionado</h3>
          <ul className="list-disc list-inside space-y-2">
            <li>
              <strong>Sistema de Memória Isolado V2 (Persistência por Usuário):</strong>
              <ul>
                <li>Implementação de um sistema de memória completamente novo e isolado, garantindo persistência de conversas por `user_id` (independente da `session_id`).</li>
                <li>
                  <strong>Novas Rotas API V2 para Chat Gemini:</strong>
                  <ul className="list-disc list-inside ml-5 space-y-1">
                    <li>`POST /api/v2/chat/gemini` - Chat principal com memória persistente.</li>
                    <li>`GET /api/v2/chat/gemini/memory` - Recupera todo o histórico de memória do usuário.</li>
                    <li>`DELETE /api/v2/chat/gemini/memory` - Limpa toda a memória do usuário.</li>
                    <li>`GET /api/v2/chat/gemini/stats` - Obtém estatísticas de uso da memória do usuário.</li>
                    <li>`PUT /api/v2/chat/gemini/profile` - Atualiza o perfil do usuário.</li>
                    <li>`POST /api/v2/chat/gemini/fact` - Salva fatos específicos sobre o usuário.</li>
                    <li>`GET /api/v2/chat/gemini/context` - Obtém o contexto completo da conversa do usuário.</li>
                    <li>`GET /api/v2/chat/health` - Health check para o serviço V2.</li>
                    <li>`POST /api/v2/chat/migrate` - Endpoint para futuras migrações de dados.</li>
                  </ul>
                </li>
                <li>
                  <strong>Persistência de Histórico por `user_id`:</strong>
                  <ul className="list-disc list-inside ml-5 space-y-1">
                    <li>A função `get_conversation_history_isolated` no `IsolatedMemoryService` agora busca o histórico apenas por `user_id`, ignorando a `session_id`.</li>
                    <li>O `GeminiChatServiceV2` foi ajustado para utilizar este histórico expandido para construir o contexto da conversa.</li>
                  </ul>
                </li>
                <li>
                  <strong>Comandos de Memória Aprimorados:</strong>
                  <ul className="list-disc list-inside ml-5 space-y-1">
                    <li>A funcionalidade "Lembre-se disso:" agora utiliza o novo sistema de memória isolado, garantindo que os fatos sejam persistidos por `user_id`.</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>

          <h3 className="text-xl font-semibold text-primary mb-2">Removido</h3>
          <ul className="list-disc list-inside space-y-2">
            <li>
              <strong>Código da Versão 1 (V1) do Sistema de Memória e Chat:</strong>
              <ul>
                <li>`app/chats/routes/chat_routes.py` (Rotas de chat V1).</li>
                <li>`app/services/memory_service.py` (Serviço de memória V1).</li>
                <li>`app/services/enhanced_memory_service.py` (Serviço de memória aprimorado V1).</li>
                <li>`app/chats/services/gemini_chat_service.py` (Serviço de chat Gemini V1).</li>
                <li>Todas as importações e registros relacionados à V1 foram removidos do `app/main.py`.</li>
              </ul>
            </li>
          </ul>

          <h3 className="text-xl font-semibold text-primary mb-2">Corrigido</h3>
          <ul className="list-disc list-inside space-y-2">
            <li>
              <strong>Problemas críticos de salvamento e acesso de memórias resolvidos:</strong>
              <ul>
                <li>Corrigidos problemas de DEFAULT (lower(hex(randomblob(16)))) em todas as tabelas.</li>
                <li>Removidas expressões SQL incompatíveis que causavam erros de criação de tabelas.</li>
                <li>Corrigidos arquivos: `backlog_generator_service.py`, `dashboard_service.py`, `review_collector_service.py`.</li>
                <li>Sistema de memória de curto e longo prazo agora funciona corretamente.</li>
                <li>Conversas são salvas e recuperadas adequadamente.</li>
              </ul>
            </li>
            <li>
              <strong>Dados padrão implementados no banco de dados:</strong>
              <ul>
                <li>Criado script `create_sample_data.py` para popular o banco com dados de exemplo.</li>
                <li>Inseridos 3 usuários padrão: admin, demo_user, test_user.</li>
                <li>Criadas 3 conversas de exemplo com sistema de memória funcionando.</li>
                <li>Inseridos 3 reviews de exemplo para testes.</li>
                <li>Banco de dados não fica mais vazio após inicialização.</li>
              </ul>
            </li>
            <li>
              <strong>Problema crítico de bloqueio do banco de dados SQLite resolvido:</strong>
              <ul>
                <li>Implementado gerenciamento adequado de conexões usando context managers.</li>
                <li>Corrigidas todas as funções de autenticação para usar `with get_db_connection()`.</li>
                <li>Eliminados vazamentos de conexão que causavam bloqueios.</li>
                <li>Adicionado script `fix_database_lock.py` para diagnóstico e correção de bloqueios.</li>
              </ul>
            </li>
            <li>
              <strong>APIs de Login totalmente funcionais:</strong>
              <ul>
                <li>Corrigidas rotas de autenticação com prefixos incorretos.</li>
                <li>Resolvido erro "405 METHOD NOT ALLOWED".</li>
                <li>Todas as rotas de autenticação agora funcionam corretamente:</li>
                <ul className="list-disc list-inside ml-5 space-y-1">
                  <li>`POST /api/auth/register` - Registro de usuários.</li>
                  <li>`POST /api/auth/login` - Login de usuários.</li>
                  <li>`POST /api/auth/logout` - Logout de usuários.</li>
                  <li>`POST /api/auth/verify` - Verificação de sessão.</li>
                  <li>`GET /api/auth/user/<id>` - Obter dados do usuário.</li>
                </ul>
              </ul>
            </li>
            <li>
              <strong>Sistema de configuração de chaves de API restaurado:</strong>
              <ul>
                <li>Corrigidas rotas de API keys: `POST /api/keys` e `GET /api/keys/<user_id>/<service_name>`.</li>
                <li>Adicionados imports necessários no arquivo `api_key_routes.py`.</li>
                <li>Sistema de armazenamento e recuperação de chaves funcionando.</li>
              </ul>
            </li>
            <li>
              <strong>Tabelas de memória de longo prazo criadas corretamente:</strong>
              <ul>
                <li>Corrigida criação automática das tabelas `conversations` e `user_profiles`.</li>
                <li>MemoryService agora usa configuração centralizada do banco.</li>
                <li>Criação automática do diretório `data/` se não existir.</li>
                <li>Sincronização entre todos os serviços de banco de dados.</li>
              </ul>
            </li>
            <li>
              <strong>Configuração de banco de dados unificada:</strong>
              <ul>
                <li>Unificada configuração em `Config.DATABASE_PATH`.</li>
                <li>Consistência entre todos os arquivos (`auth_routes.py`, `memory_service.py`, `database.py`).</li>
                <li>Criação automática de diretórios em todos os pontos de acesso.</li>
              </ul>
            </li>
            <li>
              <strong>Usuário padrão criado automaticamente:</strong>
              <ul>
                <li>Criação automática de usuário administrador na inicialização.</li>
                <li>**Credenciais:** `admin` / `admin` (email: `admin@iaraflow.com`).</li>
                <li>Script independente `create_default_user.py` para criação manual.</li>
              </ul>
            </li>
            <li>
              <strong>Dependências instaladas e configuradas:</strong>
              <ul>
                <li>Instaladas todas as dependências necessárias: Flask, LangChain, Google AI, etc.</li>
                <li>Aplicação Flask inicializa corretamente sem erros de módulos.</li>
                <li>Todas as funcionalidades principais testadas e funcionando.</li>
              </ul>
            </li>
          </ul>
        </div>

        {/* Changed Section */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Mudanças</h2>
          <ul className="list-disc list-inside space-y-2">
            <li>Estrutura do projeto expandida com novos serviços de chat.</li>
            <li><strong>LangChain Agent Service:</strong> Refatorado para usar memória persistente ao invés de memória em tempo de execução.</li>
            <li>Modelo atualizado para `gpt-4o-mini` (compatibilidade com API).</li>
            <li>Histórico de conversa limitado a 20 mensagens para otimização.</li>
            <li>Ordem cronológica corrigida para manter contexto adequado.</li>
            <li><strong>Sistema de Chat:</strong> Expandido para suportar quatro provedores de IA (Gemini, OpenAI, Groq, LangChain).</li>
            <li><strong>Endpoint de Health Check:</strong> Atualizado para incluir todos os serviços disponíveis.</li>
            <li><strong>MemoryService:</strong> Expandido com funcionalidades de perfil global por usuário e salvamento explícito.</li>
            <li>Método `save_message_with_profile_update()` para extração automática de informações.</li>
            <li>Método `get_user_context_for_chat()` para incluir contexto em conversas.</li>
            <li>Método `extract_user_info_from_message()` para análise de mensagens.</li>
            <li>Método `detect_and_save_user_fact()` para processamento de comandos "Lembre-se disso".</li>
            <li>Método `save_user_fact()` para salvamento de fatos específicos.</li>
            <li>Método `get_user_facts()` para recuperação de fatos salvos.</li>
            <li>Método `remove_user_fact()` para remoção de fatos específicos.</li>
            <li><strong>Todos os Serviços de Chat:</strong> Atualizados para usar memória global por usuário e funcionalidade "Lembre-se disso".</li>
            <li>Processamento automático de palavras-chave para salvamento de fatos.</li>
            <li>Confirmação visual quando informações são salvas.</li>
            <li>Metadados aprimorados incluindo flag `fact_saved`.</li>
            <li>Sistema de memória aprimorado para suportar múltiplos provedores de IA.</li>
          </ul>
        </div>

        {/* Technical Details Section */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Detalhes Técnicos</h2>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Novos arquivos criados:</strong>
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>`src/services/gemini_chat_service.py` - Serviço para integração com Google Gemini.</li>
                <li>`src/services/openai_chat_service.py` - Serviço para integração com OpenAI.</li>
                <li>`src/services/groq_chat_service.py` - Serviço para integração com Groq.</li>
                <li>`src/routes/chat_routes.py` - Rotas para endpoints de chat.</li>
                <li>`test_gemini_chat.py` - Script de teste para validação do chat Gemini.</li>
                <li>`test_langchain_memory.py` - Script de teste para validação da memória do LangChain.</li>
                <li>`test_groq_chat.py` - Script de teste para validação do chat Groq.</li>
                <li>`test_global_memory.py` - Script de teste para validação da memória global por usuário.</li>
                <li>`test_remember_this.py` - Script de teste para validação da funcionalidade "Lembre-se disso".</li>
                <li>`README_MEMORY_IMPLEMENTATION.md` - Documentação técnica da implementação.</li>
              </ul>
            </li>
            <li><strong>Arquivos modificados:</strong>
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>`src/services/memory_service.py` - Adicionada funcionalidade de perfil global por usuário e "Lembre-se disso".</li>
                <li>`src/services/langchain_agent_service.py` - Integração com memória de longo prazo, global e "Lembre-se disso".</li>
                <li>`src/services/gemini_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso".</li>
                <li>`src/services/openai_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso".</li>
                <li>`src/services/groq_chat_service.py` - Integração com memória global por usuário e "Lembre-se disso".</li>
                <li>`src/main.py` - Registro das novas rotas de chat.</li>
                <li>`.env` - Configuração das chaves de API.</li>
              </ul>
            </li>
            <li><strong>Dependências adicionadas:</strong>
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>`google-generativeai` - SDK oficial do Google Gemini.</li>
                <li>`groq` - SDK oficial do Groq.</li>
                <li>Configuração de variáveis de ambiente para `GEMINI_API_KEY` e `GROQ_API_KEY`.</li>
              </ul>
            </li>
            <li><strong>Funcionalidades implementadas:</strong>
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>Recuperação automática do histórico de conversas para todos os provedores.</li>
                <li>Construção de contexto para manter continuidade das conversas.</li>
                <li>Isolamento de sessões por `user_id` e `session_id`.</li>
                <li>Metadados de uso e estatísticas para cada interação.</li>
                <li>Tratamento de erros robusto em todos os serviços.</li>
                <li>Suporte a diferentes modelos OpenAI e Groq via parâmetro opcional.</li>
                <li>Integração transparente do LangChain com ferramentas e memória persistente.</li>
                <li>Endpoint para listar modelos disponíveis do Groq.</li>
                <li><strong>Memória global por usuário:</strong> Perfil persistente que transcende sessões.</li>
                <li><strong>Extração automática:</strong> Detecção de nome, profissão e idade nas mensagens.</li>
                <li><strong>Contexto inteligente:</strong> Informações do usuário incluídas automaticamente em conversas.</li>
                <li><strong>Sistema "Lembre-se disso":</strong> Salvamento explícito de fatos pelo usuário.</li>
                <li><strong>Palavras-chave inteligentes:</strong> Detecção automática de comandos de salvamento.</li>
                <li><strong>Confirmação visual:</strong> Feedback imediato quando informações são salvas.</li>
                <li><strong>Gestão de fatos:</strong> Limite automático e prevenção de duplicatas.</li>
              </ul>
            </li>
          </ul>
        </div>

        {/* Notes Section */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Notas</h2>
          <ul className="list-disc list-inside space-y-2">
            <li>O sistema mantém compatibilidade com a estrutura existente do projeto.</li>
            <li>As conversas são armazenadas de forma segura no banco SQLite local.</li>
            <li>Cada sessão é isolada, permitindo múltiplas conversas simultâneas por usuário.</li>
            <li>O histórico é limitado às últimas 20 interações por sessão para otimização de performance.</li>
            <li><strong>LangChain Agent:</strong> Mantém todas as funcionalidades originais (ferramentas, busca web, operações de arquivo) com memória persistente.</li>
            <li><strong>Groq:</strong> Oferece modelos rápidos e eficientes, incluindo Llama 3 e Mixtral.</li>
            <li><strong>Memória Global:</strong> Permite que o assistente "lembre" do usuário mesmo em diferentes sessões.
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>Funciona automaticamente: quando o usuário diz seu nome, é salvo no perfil.</li>
                <li>Contexto é incluído em todas as conversas futuras daquele `user_id`.</li>
                <li>Informações persistem mesmo após reinicialização do servidor.</li>
              </ul>
            </li>
            <li><strong>Sistema "Lembre-se disso":</strong> Controle total do usuário sobre o que é salvo.
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>Palavras-chave: "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:".</li>
                <li>Funciona em qualquer provedor (Gemini, OpenAI, Groq, LangChain).</li>
                <li>Fatos são incluídos automaticamente em futuras conversas.</li>
                <li>Exemplo: "lembre-se disso: eu andei de bicicleta no sábado" → salvo permanentemente.</li>
              </ul>
            </li>
            <li>Todos os quatro provedores (Gemini, OpenAI, Groq, LangChain) agora compartilham o mesmo sistema de memória unificado.</li>
            <li>Sistema escalável para adição de novos provedores de IA no futuro.</li>
            <li><strong>Exemplo de uso completo:</strong>
              <ul className="list-disc list-inside ml-5 space-y-1">
                <li>Sessão 1: "Meu nome é João" + "lembre-se disso: gosto de café".</li>
                <li>Sessão 2 (semana depois): Assistente sabe que é João e que ele gosta de café.</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Changelog;



