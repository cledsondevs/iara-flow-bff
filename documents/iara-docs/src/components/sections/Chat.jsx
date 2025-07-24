import CodeBlock from '../CodeBlock'
import { MessageSquare, Send, AlertCircle } from 'lucide-react'

const Chat = () => {
  const requestExample = `{
  "message": "Qual é a previsão do tempo para hoje?",
  "user_id": "user123",
  "session_id": "chat_session_abc"
}`

  const responseExample = `{
  "success": true,
  "response": "A previsão do tempo para hoje é de sol com algumas nuvens.",
  "session_id": "chat_session_abc",
  "timestamp": "2025-07-24T10:30:00.000Z"
}`

  const errorExample = `{
  "error": "Mensagem é obrigatória"
}`

  const curlExample = `curl -X POST https://sua-api.com/api/agent/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Olá, como você está?",
    "user_id": "user123",
    "session_id": "chat_session_abc"
  }'`

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-green-100 dark:bg-green-900/20 p-2 rounded-lg">
            <MessageSquare className="w-6 h-6 text-green-600 dark:text-green-400" />
          </div>
          <div>
            <h1 className="text-4xl font-bold text-foreground">Chat com Agente</h1>
            <div className="flex items-center gap-2 mt-1">
              <span className="bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 px-2 py-1 rounded text-sm font-medium">POST</span>
              <code className="bg-muted px-2 py-1 rounded text-sm">/api/agent/chat</code>
            </div>
          </div>
        </div>
        <p className="text-xl text-muted-foreground">
          Endpoint principal para conversar com o agente de IA. Permite enviar mensagens e receber respostas inteligentes.
        </p>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Parâmetros da Requisição</h2>
        <div className="bg-card border border-border rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="text-left p-4 font-semibold text-foreground">Campo</th>
                <th className="text-left p-4 font-semibold text-foreground">Tipo</th>
                <th className="text-left p-4 font-semibold text-foreground">Obrigatório</th>
                <th className="text-left p-4 font-semibold text-foreground">Descrição</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">message</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4">
                  <span className="bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200 px-2 py-1 rounded text-xs font-medium">Sim</span>
                </td>
                <td className="p-4 text-sm text-muted-foreground">A mensagem do usuário para o agente</td>
              </tr>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">user_id</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4">
                  <span className="bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200 px-2 py-1 rounded text-xs font-medium">Sim</span>
                </td>
                <td className="p-4 text-sm text-muted-foreground">O ID único do usuário</td>
              </tr>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">session_id</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4">
                  <span className="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-2 py-1 rounded text-xs font-medium">Não</span>
                </td>
                <td className="p-4 text-sm text-muted-foreground">O ID da sessão de chat. Se não fornecido, uma nova sessão pode ser iniciada</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Exemplo de Requisição</h2>
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">Corpo da Requisição (JSON)</h3>
            <CodeBlock 
              code={requestExample}
              language="json"
              title="Request Body"
            />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">cURL</h3>
            <CodeBlock 
              code={curlExample}
              language="bash"
              title="cURL Command"
            />
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Resposta</h2>
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">Sucesso (200 OK)</h3>
            <CodeBlock 
              code={responseExample}
              language="json"
              title="Successful Response"
            />
            
            <div className="mt-4 bg-card border border-border rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-muted">
                  <tr>
                    <th className="text-left p-4 font-semibold text-foreground">Campo</th>
                    <th className="text-left p-4 font-semibold text-foreground">Tipo</th>
                    <th className="text-left p-4 font-semibold text-foreground">Descrição</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t border-border">
                    <td className="p-4 font-mono text-sm bg-muted/30">success</td>
                    <td className="p-4 text-sm">boolean</td>
                    <td className="p-4 text-sm text-muted-foreground">Indica se a requisição foi bem-sucedida</td>
                  </tr>
                  <tr className="border-t border-border">
                    <td className="p-4 font-mono text-sm bg-muted/30">response</td>
                    <td className="p-4 text-sm">string</td>
                    <td className="p-4 text-sm text-muted-foreground">A resposta do agente de IA</td>
                  </tr>
                  <tr className="border-t border-border">
                    <td className="p-4 font-mono text-sm bg-muted/30">session_id</td>
                    <td className="p-4 text-sm">string</td>
                    <td className="p-4 text-sm text-muted-foreground">ID da sessão de chat</td>
                  </tr>
                  <tr className="border-t border-border">
                    <td className="p-4 font-mono text-sm bg-muted/30">timestamp</td>
                    <td className="p-4 text-sm">string</td>
                    <td className="p-4 text-sm text-muted-foreground">Timestamp da resposta em formato ISO 8601</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">Erro (400 Bad Request)</h3>
            <CodeBlock 
              code={errorExample}
              language="json"
              title="Error Response"
            />
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Códigos de Status</h2>
        <div className="space-y-3">
          <div className="flex items-center gap-3 p-3 bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800 rounded-lg">
            <span className="bg-green-500 text-white px-2 py-1 rounded text-sm font-medium">200</span>
            <span className="text-green-800 dark:text-green-200">OK - Requisição processada com sucesso</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <span className="bg-red-500 text-white px-2 py-1 rounded text-sm font-medium">400</span>
            <span className="text-red-800 dark:text-red-200">Bad Request - Dados não fornecidos ou inválidos</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <span className="bg-red-500 text-white px-2 py-1 rounded text-sm font-medium">500</span>
            <span className="text-red-800 dark:text-red-200">Internal Server Error - Erro interno do servidor</span>
          </div>
        </div>
      </div>

      <div>
        <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">Dicas de Uso</h3>
              <ul className="text-blue-700 dark:text-blue-300 text-sm space-y-1">
                <li>• Use o mesmo <code>session_id</code> para manter o contexto da conversa</li>
                <li>• O <code>user_id</code> deve ser único para cada usuário do seu sistema</li>
                <li>• As mensagens são processadas de forma assíncrona para melhor performance</li>
                <li>• O agente mantém memória das conversas anteriores na mesma sessão</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chat

