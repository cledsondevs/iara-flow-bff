import React from 'react';
import { Copy, Check } from 'lucide-react';

const ApiReference = () => {
  const [copiedEndpoint, setCopiedEndpoint] = React.useState(null);

  const copyToClipboard = (text, endpoint) => {
    navigator.clipboard.writeText(text);
    setCopiedEndpoint(endpoint);
    setTimeout(() => setCopiedEndpoint(null), 2000);
  };

  const CodeBlock = ({ children, language = 'json' }) => (
    <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
      <code className="text-foreground">{children}</code>
    </pre>
  );

  const EndpointCard = ({ method, endpoint, title, description, requestBody, responseBody, queryParams }) => (
    <div className="border border-border rounded-lg p-6 mb-6 bg-card">
      <div className="flex items-center gap-3 mb-4">
        <span className={`px-3 py-1 rounded-md text-xs font-semibold ${
          method === 'GET' ? 'bg-green-100 text-green-800' :
          method === 'POST' ? 'bg-blue-100 text-blue-800' :
          method === 'DELETE' ? 'bg-red-100 text-red-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {method}
        </span>
        <code className="text-sm bg-muted px-2 py-1 rounded font-mono">{endpoint}</code>
        <button
          onClick={() => copyToClipboard(endpoint, endpoint)}
          className="p-1 hover:bg-muted rounded"
          title="Copiar endpoint"
        >
          {copiedEndpoint === endpoint ? (
            <Check className="w-4 h-4 text-green-600" />
          ) : (
            <Copy className="w-4 h-4 text-muted-foreground" />
          )}
        </button>
      </div>
      
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground mb-4">{description}</p>
      
      {queryParams && (
        <div className="mb-4">
          <h4 className="font-semibold mb-2">Query Parameters:</h4>
          <div className="space-y-2">
            {queryParams.map((param, index) => (
              <div key={index} className="flex items-start gap-2">
                <code className="text-sm bg-muted px-2 py-1 rounded">{param.name}</code>
                <span className="text-sm text-muted-foreground">
                  {param.required ? '(obrigatório)' : '(opcional)'} - {param.description}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {requestBody && (
        <div className="mb-4">
          <h4 className="font-semibold mb-2">Request Body:</h4>
          <CodeBlock>{requestBody}</CodeBlock>
        </div>
      )}
      
      <div>
        <h4 className="font-semibold mb-2">Response:</h4>
        <CodeBlock>{responseBody}</CodeBlock>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6 text-foreground">API Reference</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Documentação completa de todos os endpoints disponíveis na API do Iara Flow.
      </p>

      {/* Base URL */}
      <div className="bg-muted p-4 rounded-lg mb-8">
        <h2 className="text-lg font-semibold mb-2">Base URL</h2>
        <code className="text-sm">https://your-api-domain.com/api</code>
      </div>

      {/* Chat Endpoints */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-primary">Chat Endpoints</h2>
        <p className="text-muted-foreground mb-6">
          Endpoints para conversar com diferentes provedores de IA com memória de longo prazo.
        </p>

        {/* Gemini Chat V2 */}
        <EndpointCard
          method="POST"
          endpoint="/api/v2/chat/gemini"
          title="Chat com Gemini (V2)"
          description="Conversar com o Google Gemini com o novo sistema de memória isolado por usuário."
          requestBody={`{
  "message": "Olá! Meu nome é João e sou desenvolvedor.",
  "user_id": "user123"
}`}
          responseBody={`{
  "success": true,
  "response": "Olá João! Prazer em conhecê-lo. Como desenvolvedor, em que área você trabalha?",
  "model": "gemini-1.5-flash",
  "timestamp": "2025-01-24T10:30:00Z"
}`}
        />

        {/* OpenAI Chat */}
        <EndpointCard
          method="POST"
          endpoint="/api/openai/chat"
          title="Chat com OpenAI"
          description="Conversar com modelos OpenAI (GPT) com memória de longo prazo e memória global por usuário."
          requestBody={`{
  "message": "lembre-se disso: gosto de café sem açúcar",
  "user_id": "user123",
  "session_id": "session456",
  "model": "gpt-4o-mini"
}`}
          responseBody={`{
  "success": true,
  "response": "✅ Informação salva na memória! Entendi, você gosta de café sem açúcar. Vou lembrar disso!",
  "session_id": "session456",
  "model": "gpt-4o-mini",
  "usage": {
    "prompt_tokens": 45,
    "completion_tokens": 23,
    "total_tokens": 68
  },
  "timestamp": "2025-01-24T10:30:00Z"
}`}
        />

        {/* Groq Chat */}
        <EndpointCard
          method="POST"
          endpoint="/api/groq/chat"
          title="Chat com Groq"
          description="Conversar com modelos Groq (Llama 3, Mixtral, Gemma) com memória de longo prazo."
          requestBody={`{
  "message": "Explique machine learning",
  "user_id": "user123",
  "session_id": "session456",
  "model": "llama3-8b-8192"
}`}
          responseBody={`{
  "success": true,
  "response": "Machine Learning é uma área da inteligência artificial...",
  "session_id": "session456",
  "model": "llama3-8b-8192",
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 156,
    "total_tokens": 188
  },
  "timestamp": "2025-01-24T10:30:00Z"
}`}
        />

        {/* LangChain Agent */}
        <EndpointCard
          method="POST"
          endpoint="/api/agent/chat"
          title="Chat com LangChain Agent"
          description="Conversar com agente LangChain que possui ferramentas (busca web, operações de arquivo) e memória de longo prazo."
          requestBody={`{
  "message": "Pesquise sobre as últimas novidades em IA",
  "user_id": "user123",
  "session_id": "session456"
}`}
          responseBody={`{
  "success": true,
  "response": "Realizei uma busca sobre as últimas novidades em IA. Aqui estão os principais desenvolvimentos...",
  "session_id": "session456",
  "timestamp": "2025-01-24T10:30:00Z"
}`}
        />
      </section>

      {/* Memory Management */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-primary">Gerenciamento de Memória</h2>
        <p className="text-muted-foreground mb-6">
          Endpoints para gerenciar a memória de conversas dos usuários.
        </p>

        {/* Get Memory V2 */}
        <EndpointCard
          method="GET"
          endpoint="/api/v2/chat/gemini/memory"
          title="Recuperar Memória Gemini (V2)"
          description="Recupera todo o histórico de memória do usuário para o serviço Gemini V2."
          queryParams={[
            { name: 'user_id', required: true, description: 'ID único do usuário' }
          ]}
          responseBody={`{
  "success": true,
  "memory": [
    {
      "id": 1,
      "user_message": "Olá!",
      "assistant_message": "Olá! Como posso ajudá-lo?",
      "timestamp": "2025-01-24T10:30:00Z"
    }
  ],
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Clear Memory V2 */}
        <EndpointCard
          method="DELETE"
          endpoint="/api/v2/chat/gemini/memory"
          title="Limpar Memória Gemini (V2)"
          description="Limpa toda a memória do usuário para o serviço Gemini V2."
          requestBody={`{
  "user_id": "user123"
}`}
          responseBody={`{
  "success": true,
  "message": "Memória limpa com sucesso",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Get Memory (Other Providers) */}
        <EndpointCard
          method="GET"
          endpoint="/api/{provider}/memory"
          title="Recuperar Memória (Outros Provedores)"
          description="Recuperar histórico de conversas para um usuário específico. Substitua {provider} por: openai, groq ou agent."
          queryParams={[
            { name: 'user_id', required: true, description: 'ID único do usuário' },
            { name: 'session_id', required: false, description: 'ID da sessão específica (opcional)' }
          ]}
          responseBody={`{
  "success": true,
  "memory": [
    {
      "id": 1,
      "user_message": "Olá!",
      "assistant_message": "Olá! Como posso ajudá-lo?",
      "timestamp": "2025-01-24T10:30:00Z"
    }
  ],
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Clear Memory (Other Providers) */}
        <EndpointCard
          method="DELETE"
          endpoint="/api/{provider}/memory"
          title="Limpar Memória (Outros Provedores)"
          description="Limpar histórico de conversas para um usuário específico. Substitua {provider} por: openai, groq ou agent."
          requestBody={`{
  "user_id": "user123",
  "session_id": "session456"
}`}
          responseBody={`{
  "success": true,
  "message": "Memória limpa com sucesso",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Update User Profile */}
        <EndpointCard
          method="PUT"
          endpoint="/api/v2/chat/gemini/profile"
          title="Atualizar Perfil do Usuário (Gemini V2)"
          description="Atualiza o perfil do usuário no sistema de memória isolado."
          requestBody={`{
  "user_id": "user123",
  "profile_data": {
    "name": "João Silva",
    "profession": "Engenheiro de Software"
  }
}`}
          responseBody={`{
  "success": true,
  "message": "Perfil atualizado com sucesso",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Save User Fact */}
        <EndpointCard
          method="POST"
          endpoint="/api/v2/chat/gemini/fact"
          title="Salvar Fato do Usuário (Gemini V2)"
          description="Salva um fato específico sobre o usuário no sistema de memória isolado."
          requestBody={`{
  "user_id": "user123",
  "fact": "Gosto de café sem açúcar."
}`}
          responseBody={`{
  "success": true,
  "message": "Fato salvo com sucesso",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Get User Context */}
        <EndpointCard
          method="GET"
          endpoint="/api/v2/chat/gemini/context"
          title="Obter Contexto do Usuário (Gemini V2)"
          description="Obtém o contexto completo da conversa do usuário, incluindo perfil e fatos salvos."
          queryParams={[
            { name: 'user_id', required: true, description: 'ID único do usuário' }
          ]}
          responseBody={`{
  "success": true,
  "context": {
    "profile": {
      "name": "João Silva",
      "profession": "Engenheiro de Software"
    },
    "facts": [
      "Gosto de café sem açúcar."
    ],
    "conversation_history": [
      {
        "role": "user",
        "content": "Olá! Meu nome é João."
      },
      {
        "role": "assistant",
        "content": "Olá João! Como posso ajudar?"
      }
    ]
  },
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />
      </section>

      {/* Utility Endpoints */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-primary">Endpoints Utilitários</h2>
        <p className="text-muted-foreground mb-6">
          Endpoints para verificação de saúde e listagem de modelos disponíveis.
        </p>

        {/* Health Check V2 */}
        <EndpointCard
          method="GET"
          endpoint="/api/v2/chat/health"
          title="Verificação de Saúde Gemini (V2)"
          description="Verificar se o serviço Gemini V2 está funcionando corretamente."
          responseBody={`{
  "success": true,
  "message": "Serviço Gemini V2 está funcionando!",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Health Check (Other Providers) */}
        <EndpointCard
          method="GET"
          endpoint="/api/chat/health"
          title="Verificação de Saúde dos Chats (Outros Provedores)"
          description="Verificar se os serviços de chat (OpenAI e Groq) estão funcionando corretamente."
          responseBody={`{
  "success": true,
  "message": "Serviços de chat OpenAI e Groq estão funcionando!",
  "services": ["openai", "groq"],
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Agent Health Check */}
        <EndpointCard
          method="GET"
          endpoint="/api/agent/health"
          title="Verificação de Saúde do Agent"
          description="Verificar se o serviço do LangChain Agent está funcionando corretamente."
          responseBody={`{
  "success": true,
  "message": "Agente de IA está funcionando!",
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />

        {/* Groq Models */}
        <EndpointCard
          method="GET"
          endpoint="/api/groq/models"
          title="Modelos Disponíveis do Groq"
          description="Listar todos os modelos disponíveis no provedor Groq."
          responseBody={`{
  "success": true,
  "models": [
    {
      "id": "llama3-8b-8192",
      "name": "Llama 3 8B",
      "context_window": 8192
    },
    {
      "id": "llama3-70b-8192",
      "name": "Llama 3 70B",
      "context_window": 8192
    },
    {
      "id": "mixtral-8x7b-32768",
      "name": "Mixtral 8x7B",
      "context_window": 32768
    },
    {
      "id": "gemma-7b-it",
      "name": "Gemma 7B IT",
      "context_window": 8192
    }
  ],
  "timestamp": "2025-01-24T10:35:00Z"
}`}
        />
      </section>

      {/* Features Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-primary">Funcionalidades Especiais</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="border border-border rounded-lg p-6 bg-card">
            <h3 className="text-xl font-semibold mb-3">Memória Global por Usuário</h3>
            <p className="text-muted-foreground mb-3">
              O sistema automaticamente extrai e salva informações pessoais do usuário (nome, profissão, idade) 
              que são lembradas em todas as sessões futuras.
            </p>
            <div className="bg-muted p-3 rounded text-sm">
              <strong>Exemplo:</strong> Se o usuário disser "Meu nome é João", essa informação será 
              automaticamente salva e incluída no contexto de futuras conversas.
            </div>
          </div>

          <div className="border border-border rounded-lg p-6 bg-card">
            <h3 className="text-xl font-semibold mb-3">Sistema "Lembre-se disso"</h3>
            <p className="text-muted-foreground mb-3">
              Usuários podem explicitamente salvar informações usando palavras-chave específicas.
            </p>
            <div className="bg-muted p-3 rounded text-sm">
              <strong>Palavras-chave:</strong> "lembre-se disso:", "importante:", "salvar para depois:", 
              "não esqueça:", "anotar:", "lembrar:"
            </div>
          </div>

          <div className="border border-border rounded-lg p-6 bg-card">
            <h3 className="text-xl font-semibold mb-3">Isolamento de Sessões</h3>
            <p className="text-muted-foreground mb-3">
              Cada combinação de user_id e session_id mantém um histórico independente, 
              permitindo múltiplas conversas simultâneas.
            </p>
          </div>

          <div className="border border-border rounded-lg p-6 bg-card">
            <h3 className="text-xl font-semibold mb-3">Ferramentas do LangChain</h3>
            <p className="text-muted-foreground mb-3">
              O agente LangChain possui acesso a ferramentas como busca web e operações de arquivo, 
              mantendo todas as funcionalidades com memória persistente.
            </p>
          </div>
        </div>
      </section>

      {/* Error Handling */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6 text-primary">Tratamento de Erros</h2>
        <p className="text-muted-foreground mb-6">
          Todos os endpoints retornam códigos de status HTTP apropriados e mensagens de erro descritivas.
        </p>

        <div className="space-y-4">
          <div className="border border-border rounded-lg p-4 bg-card">
            <h4 className="font-semibold mb-2">400 - Bad Request</h4>
            <CodeBlock>{`{
  "error": "Mensagem é obrigatória"
}`}</CodeBlock>
          </div>

          <div className="border border-border rounded-lg p-4 bg-card">
            <h4 className="font-semibold mb-2">500 - Internal Server Error</h4>
            <CodeBlock>{`{
  "error": "Erro ao processar mensagem com Gemini: Connection timeout"
}`}</CodeBlock>
          </div>
        </div>
      </section>

      {/* Authentication Note */}
      <section className="mb-12">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2 text-yellow-800">Nota sobre Autenticação</h3>
          <p className="text-yellow-700">
            Atualmente, a API não requer autenticação. Em um ambiente de produção, 
            recomenda-se implementar autenticação adequada (API keys, JWT tokens, etc.) 
            para proteger os endpoints.
          </p>
        </div>
      </section>
    </div>
  );
};

export default ApiReference;


