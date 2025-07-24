import CodeBlock from '../CodeBlock'
import { Play, Clock } from 'lucide-react'

const Quickstart = () => {
  const curlExample = `curl -X POST https://sua-api.com/api/agent/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Olá, como você pode me ajudar?",
    "user_id": "user123",
    "session_id": "chat_session_abc"
  }'`

  const responseExample = `{
  "success": true,
  "response": "Olá! Eu sou o assistente da Iara Flow. Posso ajudar você com análise de dados, processamento de linguagem natural e muito mais. Como posso ajudar hoje?",
  "session_id": "chat_session_abc",
  "timestamp": "2025-07-24T10:30:00.000Z"
}`

  const jsExample = `// Usando fetch API
const response = await fetch('https://sua-api.com/api/agent/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Olá, como você pode me ajudar?',
    user_id: 'user123',
    session_id: 'chat_session_abc'
  })
});

const data = await response.json();
console.log(data.response);`

  const pythonExample = `import requests

url = "https://sua-api.com/api/agent/chat"
payload = {
    "message": "Olá, como você pode me ajudar?",
    "user_id": "user123",
    "session_id": "chat_session_abc"
}

response = requests.post(url, json=payload)
data = response.json()
print(data["response"])`

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-4">Início Rápido</h1>
        <p className="text-xl text-muted-foreground mb-6">
          Faça sua primeira requisição para a API Iara Flow em minutos.
        </p>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>5 minutos</span>
          </div>
          <div className="flex items-center gap-2">
            <Play className="w-4 h-4" />
            <span>Nível: Iniciante</span>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Sua Primeira Requisição</h2>
        <p className="text-muted-foreground mb-6">
          Vamos começar com uma simples requisição de chat para o agente de IA. Este exemplo mostra como enviar uma mensagem e receber uma resposta.
        </p>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">1. Fazer a Requisição</h3>
            <CodeBlock 
              code={curlExample}
              language="bash"
              title="cURL"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">2. Resposta da API</h3>
            <CodeBlock 
              code={responseExample}
              language="json"
              title="Resposta JSON"
            />
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Exemplos em Diferentes Linguagens</h2>
        
        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">JavaScript</h3>
            <CodeBlock 
              code={jsExample}
              language="javascript"
              title="JavaScript (Fetch API)"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-foreground mb-3">Python</h3>
            <CodeBlock 
              code={pythonExample}
              language="python"
              title="Python (Requests)"
            />
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Parâmetros Obrigatórios</h2>
        <div className="bg-card border border-border rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="text-left p-4 font-semibold text-foreground">Parâmetro</th>
                <th className="text-left p-4 font-semibold text-foreground">Tipo</th>
                <th className="text-left p-4 font-semibold text-foreground">Descrição</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">message</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4 text-sm text-muted-foreground">A mensagem que você quer enviar para o agente</td>
              </tr>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">user_id</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4 text-sm text-muted-foreground">Identificador único do usuário</td>
              </tr>
              <tr className="border-t border-border">
                <td className="p-4 font-mono text-sm bg-muted/30">session_id</td>
                <td className="p-4 text-sm">string</td>
                <td className="p-4 text-sm text-muted-foreground">Identificador da sessão de chat (opcional)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-6">Próximos Passos</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow">
            <h3 className="text-lg font-semibold text-card-foreground mb-2">Explore Mais Endpoints</h3>
            <p className="text-muted-foreground mb-4">Descubra todos os endpoints disponíveis na API do Agente de IA.</p>
            <button className="text-primary hover:underline">Ver API do Agente →</button>
          </div>
          <div className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow">
            <h3 className="text-lg font-semibold text-card-foreground mb-2">Análise de Reviews</h3>
            <p className="text-muted-foreground mb-4">Aprenda a usar nossa API para análise de reviews de aplicativos.</p>
            <button className="text-primary hover:underline">Ver Agente de Reviews →</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Quickstart

