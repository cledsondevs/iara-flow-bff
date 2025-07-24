import { Code, Palette, Zap, Shield, Globe, Layers } from 'lucide-react'

const Frontend = () => {
  const technologies = [
    {
      name: 'React',
      description: 'Biblioteca JavaScript para construção de interfaces de usuário',
      icon: '⚛️'
    },
    {
      name: 'TypeScript',
      description: 'Superset do JavaScript que adiciona tipagem estática',
      icon: '🔷'
    },
    {
      name: 'Vite',
      description: 'Ferramenta de build rápida para projetos web modernos',
      icon: '⚡'
    },
    {
      name: 'Shadcn UI',
      description: 'Coleção de componentes de UI reutilizáveis e acessíveis',
      icon: '🎨'
    },
    {
      name: 'Tailwind CSS',
      description: 'Framework CSS utilitário para estilização rápida',
      icon: '💨'
    },
    {
      name: 'React Query',
      description: 'Gerenciamento de estado assíncrono e cache de dados',
      icon: '🔄'
    }
  ]

  const routes = [
    {
      path: '/',
      name: 'Landing Page',
      description: 'Página inicial apresentando as funcionalidades do Iara Flow',
      protected: false
    },
    {
      path: '/prototyper',
      name: 'Prototyper',
      description: 'Interface principal para interação com agentes de IA',
      protected: true
    },
    {
      path: '/dashboard/:customUrl',
      name: 'Dashboard',
      description: 'Dashboards dinâmicos para análise de reviews e métricas',
      protected: false
    },
    {
      path: '/auth',
      name: 'Autenticação',
      description: 'Página de login e registro de usuários',
      protected: false
    }
  ]

  const features = [
    {
      icon: Code,
      title: 'TypeScript',
      description: 'Código mais seguro e manutenível com tipagem estática.'
    },
    {
      icon: Palette,
      title: 'Design System',
      description: 'Interface consistente usando Shadcn UI e Tailwind CSS.'
    },
    {
      icon: Zap,
      title: 'Performance',
      description: 'Build otimizado com Vite e gerenciamento eficiente de estado.'
    },
    {
      icon: Shield,
      title: 'Rotas Protegidas',
      description: 'Autenticação integrada para proteger áreas sensíveis.'
    },
    {
      icon: Globe,
      title: 'Responsivo',
      description: 'Interface adaptável para desktop, tablet e mobile.'
    },
    {
      icon: Layers,
      title: 'Componentização',
      description: 'Arquitetura modular com componentes reutilizáveis.'
    }
  ]

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-4">
          Frontend: Iara Flow Prototyper
        </h1>
        <p className="text-xl text-muted-foreground mb-6">
          Aplicação React moderna que oferece uma interface intuitiva para interação com os agentes de IA e visualização de dados.
        </p>
        <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="text-blue-800 dark:text-blue-200">
            <strong>Tecnologia:</strong> React + TypeScript + Vite | <strong>UI:</strong> Shadcn UI + Tailwind CSS
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
        <h2 className="text-2xl font-semibold text-foreground mb-6">Stack Tecnológico</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {technologies.map((tech, index) => (
            <div key={index} className="bg-card border border-border rounded-lg p-4 hover:bg-accent/50 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{tech.icon}</span>
                <h3 className="font-semibold text-card-foreground">{tech.name}</h3>
              </div>
              <p className="text-sm text-muted-foreground">{tech.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Rotas da Aplicação</h2>
        <div className="bg-card border border-border rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="text-left p-4 font-semibold text-foreground">Rota</th>
                <th className="text-left p-4 font-semibold text-foreground">Nome</th>
                <th className="text-left p-4 font-semibold text-foreground">Descrição</th>
                <th className="text-left p-4 font-semibold text-foreground">Protegida</th>
              </tr>
            </thead>
            <tbody>
              {routes.map((route, index) => (
                <tr key={index} className="border-t border-border">
                  <td className="p-4 font-mono text-sm bg-muted/30">{route.path}</td>
                  <td className="p-4 font-medium">{route.name}</td>
                  <td className="p-4 text-sm text-muted-foreground">{route.description}</td>
                  <td className="p-4">
                    {route.protected ? (
                      <span className="bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200 px-2 py-1 rounded text-xs font-medium">
                        Sim
                      </span>
                    ) : (
                      <span className="bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 px-2 py-1 rounded text-xs font-medium">
                        Não
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-foreground mb-6">Integração com a API</h2>
        <div className="bg-card border border-border rounded-lg p-6">
          <p className="text-card-foreground mb-4">
            O frontend se comunica com a API Iara Flow BFF através de requisições HTTP, utilizando React Query para gerenciamento eficiente de estado e cache. As principais integrações incluem:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-muted/50 rounded-lg p-4">
              <h4 className="font-semibold text-foreground mb-2">Chat com Agentes</h4>
              <p className="text-sm text-muted-foreground">Envio de mensagens e recebimento de respostas dos agentes de IA em tempo real.</p>
            </div>
            <div className="bg-muted/50 rounded-lg p-4">
              <h4 className="font-semibold text-foreground mb-2">Análise de Reviews</h4>
              <p className="text-sm text-muted-foreground">Visualização de dashboards com análise de sentimento e métricas de aplicativos.</p>
            </div>
            <div className="bg-muted/50 rounded-lg p-4">
              <h4 className="font-semibold text-foreground mb-2">Gerenciamento de Memória</h4>
              <p className="text-sm text-muted-foreground">Controle do histórico de conversas e contexto dos agentes.</p>
            </div>
            <div className="bg-muted/50 rounded-lg p-4">
              <h4 className="font-semibold text-foreground mb-2">Relatórios</h4>
              <p className="text-sm text-muted-foreground">Geração e visualização de relatórios abrangentes do sistema.</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-6">Desenvolvimento</h2>
        <div className="space-y-6">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-card-foreground mb-3">Instalação</h3>
            <div className="bg-gray-900 rounded-lg p-4 text-gray-300 font-mono text-sm">
              <div>npm install</div>
              <div className="text-gray-500"># ou</div>
              <div>pnpm install</div>
            </div>
          </div>
          
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-card-foreground mb-3">Desenvolvimento</h3>
            <div className="bg-gray-900 rounded-lg p-4 text-gray-300 font-mono text-sm">
              <div>npm run dev</div>
              <div className="text-gray-500"># Inicia o servidor de desenvolvimento</div>
            </div>
          </div>
          
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-card-foreground mb-3">Build para Produção</h3>
            <div className="bg-gray-900 rounded-lg p-4 text-gray-300 font-mono text-sm">
              <div>npm run build</div>
              <div className="text-gray-500"># Gera os arquivos otimizados para produção</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Frontend

