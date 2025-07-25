import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { MessageSquare, Send, Trash2, User, Bot, Brain, Clock, Sparkles } from 'lucide-react'
import '../App.css'

const API_BASE_URL = 'http://localhost:5000/api'

const ChatInterface = () => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [userId] = useState('user123') // ID fixo para demonstração
  const [sessionId, setSessionId] = useState(`session_${Date.now()}`)
  const [activeProvider, setActiveProvider] = useState('gemini')
  const [memory, setMemory] = useState([])
  const [userProfile, setUserProfile] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    loadMemory()
  }, [activeProvider, sessionId])

  const loadMemory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/${activeProvider}/memory?user_id=${userId}&session_id=${sessionId}`)
      if (response.ok) {
        const data = await response.json()
        setMemory(data.memory || [])
        
        // Carregar mensagens da memória para exibir no chat
        if (data.memory && data.memory.length > 0) {
          const memoryMessages = data.memory.map(item => [
            { type: 'user', content: item.message, timestamp: item.created_at },
            { type: 'assistant', content: item.response, timestamp: item.created_at }
          ]).flat()
          setMessages(memoryMessages)
        }
      }
    } catch (error) {
      console.error('Erro ao carregar memória:', error)
    }
  }

  const clearMemory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/${activeProvider}/memory`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId
        })
      })
      
      if (response.ok) {
        setMemory([])
        setMessages([])
      }
    } catch (error) {
      console.error('Erro ao limpar memória:', error)
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/${activeProvider}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          user_id: userId,
          session_id: sessionId
        })
      })

      if (response.ok) {
        const data = await response.json()
        const assistantMessage = {
          type: 'assistant',
          content: data.response,
          timestamp: data.timestamp,
          model: data.model,
          factSaved: data.fact_saved
        }
        
        setMessages(prev => [...prev, assistantMessage])
        
        // Recarregar memória após nova mensagem
        setTimeout(() => loadMemory(), 500)
      } else {
        const errorData = await response.json()
        const errorMessage = {
          type: 'error',
          content: `Erro: ${errorData.error}`,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      const errorMessage = {
        type: 'error',
        content: `Erro de conexão: ${error.message}`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setInputMessage('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const newSession = () => {
    const newSessionId = `session_${Date.now()}`
    setSessionId(newSessionId)
    setMessages([])
    setMemory([])
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2 flex items-center justify-center gap-3">
            <Brain className="w-10 h-10 text-blue-600" />
            Iara Flow - Chat com IA
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Sistema de chat com memória de curto e longo prazo
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Painel Principal de Chat */}
          <div className="lg:col-span-3">
            <Card className="h-[600px] flex flex-col">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <MessageSquare className="w-5 h-5" />
                    Chat
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    <Tabs value={activeProvider} onValueChange={setActiveProvider} className="w-auto">
                      <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="gemini" className="text-xs">
                          <Sparkles className="w-3 h-3 mr-1" />
                          Gemini
                        </TabsTrigger>
                        <TabsTrigger value="openai" className="text-xs">
                          <Bot className="w-3 h-3 mr-1" />
                          OpenAI
                        </TabsTrigger>
                      </TabsList>
                    </Tabs>
                    <Button variant="outline" size="sm" onClick={newSession}>
                      Nova Sessão
                    </Button>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Badge variant="secondary">Usuário: {userId}</Badge>
                  <Badge variant="outline">Sessão: {sessionId.slice(-8)}</Badge>
                  <Badge variant="outline">Provedor: {activeProvider}</Badge>
                </div>
              </CardHeader>
              
              <CardContent className="flex-1 flex flex-col p-0">
                <ScrollArea className="flex-1 p-4">
                  <div className="space-y-4">
                    {messages.length === 0 && (
                      <div className="text-center text-gray-500 py-8">
                        <MessageSquare className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>Inicie uma conversa! O sistema lembrará de tudo.</p>
                        <p className="text-sm mt-2">
                          Experimente dizer: "Lembre-se disso: eu gosto de café"
                        </p>
                      </div>
                    )}
                    
                    {messages.map((message, index) => (
                      <div
                        key={index}
                        className={`flex gap-3 ${
                          message.type === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                      >
                        <div
                          className={`max-w-[80%] rounded-lg p-3 ${
                            message.type === 'user'
                              ? 'bg-blue-600 text-white'
                              : message.type === 'error'
                              ? 'bg-red-100 text-red-800 border border-red-200'
                              : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                          }`}
                        >
                          <div className="flex items-start gap-2">
                            {message.type === 'user' ? (
                              <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
                            ) : (
                              <Bot className="w-4 h-4 mt-0.5 flex-shrink-0" />
                            )}
                            <div className="flex-1">
                              <p className="whitespace-pre-wrap">{message.content}</p>
                              {message.factSaved && (
                                <Badge className="mt-2 bg-green-100 text-green-800">
                                  ✅ Informação salva na memória!
                                </Badge>
                              )}
                              <div className="flex items-center gap-2 mt-2 text-xs opacity-70">
                                <Clock className="w-3 h-3" />
                                {formatTimestamp(message.timestamp)}
                                {message.model && (
                                  <Badge variant="outline" className="text-xs">
                                    {message.model}
                                  </Badge>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 max-w-[80%]">
                          <div className="flex items-center gap-2">
                            <Bot className="w-4 h-4" />
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  <div ref={messagesEndRef} />
                </ScrollArea>
                
                <div className="border-t p-4">
                  <div className="flex gap-2">
                    <Input
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Digite sua mensagem... (use 'lembre-se disso:' para salvar informações)"
                      disabled={isLoading}
                      className="flex-1"
                    />
                    <Button 
                      onClick={sendMessage} 
                      disabled={isLoading || !inputMessage.trim()}
                      size="icon"
                    >
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Painel de Memória */}
          <div className="lg:col-span-1">
            <Card className="h-[600px] flex flex-col">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2 text-sm">
                    <Brain className="w-4 h-4" />
                    Memória
                  </CardTitle>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={clearMemory}
                    className="text-xs"
                  >
                    <Trash2 className="w-3 h-3 mr-1" />
                    Limpar
                  </Button>
                </div>
              </CardHeader>
              
              <CardContent className="flex-1 p-0">
                <ScrollArea className="h-full p-4">
                  {memory.length === 0 ? (
                    <div className="text-center text-gray-500 py-8">
                      <Brain className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">Nenhuma memória ainda</p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {memory.slice().reverse().map((item, index) => (
                        <div key={index} className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">
                          <div className="font-medium text-blue-600 mb-1">
                            Usuário:
                          </div>
                          <p className="text-gray-700 dark:text-gray-300 mb-2 text-xs">
                            {item.message}
                          </p>
                          <div className="font-medium text-green-600 mb-1">
                            Assistente:
                          </div>
                          <p className="text-gray-700 dark:text-gray-300 text-xs">
                            {item.response}
                          </p>
                          <div className="text-xs text-gray-400 mt-2 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {formatTimestamp(item.created_at)}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface

