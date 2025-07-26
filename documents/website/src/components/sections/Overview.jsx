import { MessageSquare, BarChart3, Shield, Zap, Brain, Database, Users, Clock } from 'lucide-react'

const Overview = () => {
  const features = [
    {
      icon: MessageSquare,
      title: 'Chat Multi-Provedor',
      description: 'Integração com Gemini, OpenAI, Groq e LangChain Agent para conversas inteligentes com memória persistente.'
    },
    {
      icon: Brain,
      title: 'Sistema de Memória V2',
      description: 'Memória isolada por usuário com persistência de conversas e fatos, independente da sessão.'
    },
    {
      icon: Database,
      title: 'Persistência Avançada',
      description: 'Armazenamento seguro no SQLite com histórico de conversas e perfis de usuário.'
    },
    {
      icon: Users,
      title: 'Memória Global por Usuário',
      description: 'O assistente lembra informações pessoais (nome, profissão, idade) entre diferentes sessões.'
    },
    {
      icon: Clock,
      title: 'Funcionalidade "Lembre-se disso"',
      description: 'Salvamento explícito de fatos importantes pelo usuário com palavras-chave inteligentes.'
    },
    {
      icon: BarChart3,
      title: 'Análise de Reviews',
      description: 'Colete e analise reviews de aplicativos com análise de sentimento avançada.'
    },
    {
      icon: Shield,
      title: 'Seguro e Confiável',
      description: 'API robusta com autenticação, tratamento de erros e verificações de saúde integradas.'
    },
    {
      icon: Zap,
      title: 'Fácil Integração',
      description: 'Endpoints RESTful simples e documentação completa para integração rápida.'
    }
  ]

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-4">
          Iara Flow API
        </h1>
        <p className="text-xl text-muted-foreground mb-6">
          Uma API Backend for Frontend (BFF) poderosa para integração com agentes de IA, sistema de memória avançado e análise de dados.
        </p>
        <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="text-blue-800 dark:text-blue-200">
            <strong>Versão atual:</strong> 2.0.0 | <strong>Base URL:</strong> <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">https://sua-api.com</code>
          </p>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Principais Funcionalidades</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start gap-4">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-card-foreground mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Sistema de Memória V2</h2>
        <div className="bg-card border border-border rounded-lg p-6">
          <p className="text-card-foreground mb-4">
            O Sistema de Memória V2 representa uma evolução completa na forma como a API gerencia conversas e informações do usuário. Com persistência por `user_id` independente da `session_id`, o sistema garante continuidade das conversas mesmo em diferentes dispositivos ou sessões.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div className="bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <h4 className="font-semibold text-green-800 dark:text-green-200 mb-2">✅ Memória Persistente</h4>
              <p className="text-sm text-green-700 dark:text-green-300">Conversas e fatos salvos por usuário, não por sessão</p>
            </div>
            <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">🧠 Memória Global</h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">Extração automática de informações pessoais</p>
            </div>
            <div className="bg-purple-50 dark:bg-purple-950/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
              <h4 className="font-semibold text-purple-800 dark:text-purple-200 mb-2">💾 "Lembre-se disso"</h4>
              <p className="text-sm text-purple-700 dark:text-purple-300">Salvamento explícito com palavras-chave</p>
            </div>
            <div className="bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
              <h4 className="font-semibold text-orange-800 dark:text-orange-200 mb-2">🔄 Multi-Provedor</h4>
              <p className="text-sm text-orange-700 dark:text-orange-300">Funciona com Gemini, OpenAI, Groq e LangChain</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Arquitetura</h2>
        <div className="bg-card border border-border rounded-lg p-6">
          <p className="text-card-foreground mb-4">
            A API Iara Flow BFF é construída com Flask e Python, fornecendo uma interface robusta e escalável para interagir com diversos agentes de IA. Ela serve como uma camada intermediária entre o frontend e os serviços de backend, garantindo uma experiência de usuário fluida e eficiente com sistema de memória avançado.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div className="text-center p-4 bg-muted rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Frontend</h4>
              <p className="text-sm text-muted-foreground">React, Vue, Angular ou qualquer cliente HTTP</p>
            </div>
            <div className="text-center p-4 bg-primary/10 rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Iara Flow BFF</h4>
              <p className="text-sm text-muted-foreground">Flask + Python + Memória V2</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Provedores IA</h4>
              <p className="text-sm text-muted-foreground">Gemini, OpenAI, Groq, LangChain</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Banco de Dados</h4>
              <p className="text-sm text-muted-foreground">SQLite + Memória Persistente</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Novidades da Versão 2.0</h2>
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-950/20 dark:to-blue-950/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
            <h3 className="font-semibold text-foreground mb-2">🚀 Sistema de Memória Isolado V2</h3>
            <p className="text-muted-foreground mb-3">Implementação completamente nova com persistência por usuário, independente da sessão.</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Novas rotas API V2 para Chat Gemini</li>
              <li>• Persistência de histórico por `user_id`</li>
              <li>• Comandos de memória aprimorados</li>
            </ul>
          </div>
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
            <h3 className="font-semibold text-foreground mb-2">🧠 Funcionalidade "Lembre-se disso"</h3>
            <p className="text-muted-foreground mb-3">Sistema de salvamento explícito de informações pelo usuário.</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Palavras-chave: "lembre-se disso:", "importante:", "salvar para depois:"</li>
              <li>• Detecção automática e extração de fatos</li>
              <li>• Confirmação visual quando um fato é salvo</li>
            </ul>
          </div>
          <div className="bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-950/20 dark:to-red-950/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6">
            <h3 className="font-semibold text-foreground mb-2">🔧 Correções Críticas</h3>
            <p className="text-muted-foreground mb-3">Problemas críticos de salvamento e acesso de memórias resolvidos.</p>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Bloqueio do banco de dados SQLite resolvido</li>
              <li>• APIs de Login totalmente funcionais</li>
              <li>• Sistema de configuração de chaves de API restaurado</li>
            </ul>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-6">Próximos Passos</h2>
        <div className="space-y-4">
          <div className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
            <h3 className="font-semibold text-card-foreground mb-2">1. Início Rápido</h3>
            <p className="text-muted-foreground">Faça sua primeira requisição em minutos com nosso guia de início rápido.</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
            <h3 className="font-semibold text-card-foreground mb-2">2. Explore o Chat Multi-Provedor</h3>
            <p className="text-muted-foreground">Descubra como interagir com Gemini, OpenAI, Groq e LangChain com memória persistente.</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
            <h3 className="font-semibold text-card-foreground mb-2">3. Sistema de Memória V2</h3>
            <p className="text-muted-foreground">Aprenda a usar o novo sistema de memória isolado e funcionalidade "Lembre-se disso".</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
            <h3 className="font-semibold text-card-foreground mb-2">4. Análise de Reviews</h3>
            <p className="text-muted-foreground">Aprenda a coletar e analisar reviews de aplicativos com nossa API especializada.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Overview


