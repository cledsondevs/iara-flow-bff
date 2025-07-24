import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Overview from './components/sections/Overview'
import Quickstart from './components/sections/Quickstart'
import Chat from './components/sections/Chat'
import Frontend from './components/sections/Frontend'
import { Moon, Sun } from 'lucide-react'
import './App.css'

function App() {
  const [activeSection, setActiveSection] = useState('overview')
  const [darkMode, setDarkMode] = useState(false)

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    document.documentElement.classList.toggle('dark')
  }

  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return <Overview />
      case 'quickstart':
        return <Quickstart />
      case 'frontend':
        return <Frontend />
      case 'chat':
        return <Chat />
      case 'memory':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Gerenciamento de Memória</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'health':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Verificação de Saúde</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'autonomous-mode':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Modo Autônomo</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'app-management':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Gerenciar Apps</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'collection':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Coleta de Reviews</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'analysis':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Análise de Sentimento</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'backlog':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Geração de Backlog</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'dashboard':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Dashboard</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'reports':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Relatórios</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'authentication':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Autenticação</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      case 'errors':
        return <div className="max-w-4xl"><h1 className="text-4xl font-bold mb-4">Tratamento de Erros</h1><p className="text-muted-foreground">Documentação em desenvolvimento...</p></div>
      default:
        return <Overview />
    }
  }

  return (
    <div className={`min-h-screen bg-background ${darkMode ? 'dark' : ''}`}>
      <div className="flex">
        <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
        
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="bg-background border-b border-border px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold text-foreground">Documentação</h2>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span>API Reference</span>
                </div>
              </div>
              
              <button
                onClick={toggleDarkMode}
                className="p-2 bg-muted hover:bg-accent rounded-lg transition-colors"
                title={darkMode ? 'Modo claro' : 'Modo escuro'}
              >
                {darkMode ? (
                  <Sun className="w-4 h-4 text-foreground" />
                ) : (
                  <Moon className="w-4 h-4 text-foreground" />
                )}
              </button>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1 p-6 overflow-y-auto">
            {renderContent()}
          </main>
        </div>
      </div>
    </div>
  )
}

export default App

