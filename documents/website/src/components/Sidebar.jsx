import { useState } from 'react'
import { ChevronDown, ChevronRight, Search, Book, Zap, Settings, MessageSquare, BarChart3, Shield } from 'lucide-react'

const Sidebar = ({ activeSection, onSectionChange }) => {
  const [expandedSections, setExpandedSections] = useState({
    'getting-started': true,
    'agent-api': true,
    'review-agent': true
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const menuItems = [
    {
      id: 'overview',
      title: 'Visão Geral',
      icon: Book,
      type: 'item'
    },
    {
      id: 'getting-started',
      title: 'Primeiros Passos',
      icon: Zap,
      type: 'section',
      items: [
        { id: 'quickstart', title: 'Início Rápido' },
        { id: 'authentication', title: 'Autenticação' },
        { id: 'errors', title: 'Tratamento de Erros' }
      ]
    },
    {
      id: 'agent-api',
      title: 'API do Agente de IA',
      icon: MessageSquare,
      type: 'section',
      items: [
        { id: 'chat', title: 'Chat com Agente' },
        { id: 'memory', title: 'Gerenciamento de Memória' },
        { id: 'health', title: 'Verificação de Saúde' }
      ]
    },
    {
      id: 'review-agent',
      title: 'Agente de Reviews',
      icon: BarChart3,
      type: 'section',
      items: [
        { id: 'autonomous-mode', title: 'Modo Autônomo' },
        { id: 'app-management', title: 'Gerenciar Apps' },
        { id: 'collection', title: 'Coleta de Reviews' },
        { id: 'analysis', title: 'Análise de Sentimento' },
        { id: 'backlog', title: 'Geração de Backlog' },
        { id: 'dashboard', title: 'Dashboard' },
        { id: 'reports', title: 'Relatórios' }
      ]
    },
    {
      id: 'changelog',
      title: 'Histórico de Mudanças',
      icon: Settings,
      type: 'item'
    },
    {
      id: 'api-reference',
      title: 'API Reference',
      icon: Book,
      type: 'item'
    }
  ]

  return (
    <div className="w-64 bg-sidebar border-r border-sidebar-border h-screen overflow-y-auto">
      <div className="p-4">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-sidebar-foreground">Iara Flow</h1>
            <p className="text-xs text-sidebar-foreground/60">API Documentation</p>
          </div>
        </div>

        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-sidebar-foreground/40" />
          <input
            type="text"
            placeholder="Buscar..."
            className="w-full pl-10 pr-4 py-2 bg-sidebar-accent border border-sidebar-border rounded-lg text-sm text-sidebar-foreground placeholder-sidebar-foreground/40 focus:outline-none focus:ring-2 focus:ring-sidebar-ring"
          />
        </div>

        <nav className="space-y-1">
          {menuItems.map((item) => (
            <div key={item.id}>
              {item.type === 'item' ? (
                <button
                  onClick={() => onSectionChange(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                    activeSection === item.id
                      ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                      : 'text-sidebar-foreground hover:bg-sidebar-accent/50'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  {item.title}
                </button>
              ) : (
                <div>
                  <button
                    onClick={() => toggleSection(item.id)}
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors text-sidebar-foreground hover:bg-sidebar-accent/50"
                  >
                    <item.icon className="w-4 h-4" />
                    {item.title}
                    {expandedSections[item.id] ? (
                      <ChevronDown className="w-4 h-4 ml-auto" />
                    ) : (
                      <ChevronRight className="w-4 h-4 ml-auto" />
                    )}
                  </button>
                  {expandedSections[item.id] && (
                    <div className="ml-7 mt-1 space-y-1">
                      {item.items.map((subItem) => (
                        <button
                          key={subItem.id}
                          onClick={() => onSectionChange(subItem.id)}
                          className={`w-full text-left px-3 py-1.5 text-sm rounded-lg transition-colors ${
                            activeSection === subItem.id
                              ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                              : 'text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground'
                          }`}
                        >
                          {subItem.title}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </nav>
      </div>
    </div>
  )
}

export default Sidebar

