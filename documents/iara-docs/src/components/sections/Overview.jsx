import { MessageSquare, BarChart3, Shield, Zap } from 'lucide-react'

const Overview = () => {
  const features = [
    {
      icon: MessageSquare,
      title: 'Agente de IA',
      description: 'Interaja com agentes inteligentes para chat e processamento de linguagem natural.'
    },
    {
      icon: BarChart3,
      title: 'Análise de Reviews',
      description: 'Colete e analise reviews de aplicativos com análise de sentimento avançada.'
    },
    {
      icon: Shield,
      title: 'Seguro e Confiável',
      description: 'API robusta com tratamento de erros e verificações de saúde integradas.'
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
          Uma API Backend for Frontend (BFF) poderosa para integração com agentes de IA e análise de dados.
        </p>
        <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="text-blue-800 dark:text-blue-200">
            <strong>Versão atual:</strong> 1.0.0 | <strong>Base URL:</strong> <code className="bg-blue-100 dark:bg-blue-900 px-2 py-1 rounded">https://sua-api.com</code>
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
        <h2 className="text-2xl font-semibold text-foreground mb-6">Arquitetura</h2>
        <div className="bg-card border border-border rounded-lg p-6">
          <p className="text-card-foreground mb-4">
            A API Iara Flow BFF é construída com Flask e Python, fornecendo uma interface robusta e escalável para interagir com diversos agentes de IA. Ela serve como uma camada intermediária entre o frontend e os serviços de backend, garantindo uma experiência de usuário fluida e eficiente.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <div className="text-center p-4 bg-muted rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Frontend</h4>
              <p className="text-sm text-muted-foreground">React, Vue, Angular ou qualquer cliente HTTP</p>
            </div>
            <div className="text-center p-4 bg-primary/10 rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Iara Flow BFF</h4>
              <p className="text-sm text-muted-foreground">Flask + Python</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <h4 className="font-semibold text-foreground mb-2">Serviços</h4>
              <p className="text-sm text-muted-foreground">IA, Banco de Dados, APIs Externas</p>
            </div>
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
            <h3 className="font-semibold text-card-foreground mb-2">2. Explore a API do Agente</h3>
            <p className="text-muted-foreground">Descubra como interagir com nossos agentes de IA para chat e processamento.</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
            <h3 className="font-semibold text-card-foreground mb-2">3. Análise de Reviews</h3>
            <p className="text-muted-foreground">Aprenda a coletar e analisar reviews de aplicativos com nossa API especializada.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Overview

