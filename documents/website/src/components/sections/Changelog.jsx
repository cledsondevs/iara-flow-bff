import React from 'react';

const Changelog = () => {
  return (
    <div className="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow-lg">
      <h1 className="text-4xl font-bold mb-6 text-foreground">Histórico de Mudanças (Changelog)</h1>
      
      <div className="space-y-8 text-muted-foreground">
        {/* Versão 1.3.0 - Memória Global e Lembre-se disso */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Versão 1.3.0 - Memória Global e Lembre-se disso</h2>
          <p className="text-sm text-gray-500 mb-4">24 de Julho de 2025</p>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Memória Global por Usuário:</strong> O assistente agora lembra de informações sobre o usuário (nome, profissão, idade) entre diferentes sessões.</li>
            <li><strong>Extração Automática de Informações:</strong> Identifica e salva automaticamente dados pessoais do usuário a partir das mensagens.</li>
            <li><strong>Contexto Inteligente:</strong> Informações do perfil do usuário são incluídas automaticamente no contexto de todas as conversas.</li>
            <li><strong>Funcionalidade "Lembre-se disso":</strong> Sistema de salvamento explícito de informações pelo usuário.</li>
            <li><strong>Palavras-chave para salvar fatos:</strong> "lembre-se disso:", "importante:", "salvar para depois:", "não esqueça:", "anotar:", "lembrar:".</li>
            <li><strong>Detecção automática e extração de fatos:</strong> Fatos são extraídos das mensagens do usuário.</li>
            <li><strong>Fatos salvos são incluídos automaticamente:</strong> No contexto de futuras conversas.</li>
            <li><strong>Funciona em todos os provedores de IA:</strong> Gemini, OpenAI, Groq, LangChain.</li>
            <li><strong>Limite de 10 fatos por usuário:</strong> Para otimização de performance.</li>
            <li><strong>Confirmação visual:</strong> Quando um fato é salvo (✅ Informação salva na memória!).</li>
          </ul>
        </div>

        {/* Versão 1.2.0 - Suporte ao Groq Chat */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Versão 1.2.0 - Suporte ao Groq Chat</h2>
          <p className="text-sm text-gray-500 mb-4">24 de Julho de 2025</p>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Novo provedor de IA:</strong> Adicionado suporte ao Groq Chat.</li>
            <li><strong>Novo endpoint:</strong> `/api/groq/chat` com memória de longo prazo.</li>
            <li><strong>Gerenciamento de memória:</strong> Endpoints GET e DELETE para `/api/groq/memory`.</li>
            <li><strong>Listagem de modelos:</strong> Endpoint `/api/groq/models` para listar modelos disponíveis.</li>
            <li><strong>Modelos suportados:</strong> `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma-7b-it`.</li>
            <li><strong>Integração completa:</strong> Com sistema de memória unificado.</li>
          </ul>
        </div>

        {/* Versão 1.1.0 - Memória de Longo Prazo para LangChain Agent */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Versão 1.1.0 - Memória de Longo Prazo para LangChain Agent</h2>
          <p className="text-sm text-gray-500 mb-4">24 de Julho de 2025</p>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Extensão da memória persistente:</strong> Para o agente LangChain.</li>
            <li><strong>Endpoint `/api/agent/chat`:</strong> Agora utiliza memória de longo prazo.</li>
            <li><strong>Histórico de conversas:</strong> Mantido entre reinicializações do servidor.</li>
            <li><strong>Integração com ferramentas:</strong> Preservada (web_search, file operations).</li>
            <li><strong>Metadados aprimorados:</strong> Incluindo ferramentas utilizadas e tipo de agente.</li>
          </ul>
        </div>

        {/* Versão 1.0.0 - Memória de Longo Prazo para Chats */}
        <div className="border-b pb-4">
          <h2 className="text-2xl font-semibold text-primary mb-2">Versão 1.0.0 - Memória de Longo Prazo para Chats</h2>
          <p className="text-sm text-gray-500 mb-4">24 de Julho de 2025</p>
          <ul className="list-disc list-inside space-y-2">
            <li><strong>Implementação de memória persistente:</strong> Para os endpoints de chat Gemini e OpenAI.</li>
            <li><strong>Novos endpoints:</strong> `/api/gemini/chat` e `/api/openai/chat` com memória de longo prazo.</li>
            <li><strong>Gerenciamento de memória:</strong> Endpoints GET e DELETE para `/api/gemini/memory` e `/api/openai/memory`.</li>
            <li><strong>Verificação de saúde:</strong> Endpoint `/api/chat/health`.</li>
            <li><strong>Sistema de sessões:</strong> Para isolar conversas por usuário e sessão.</li>
            <li><strong>Armazenamento persistente:</strong> De conversas no banco SQLite.</li>
            <li><strong>Contexto de conversa:</strong> Mantido entre sessões diferentes.</li>
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


