import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.file_management import (
    ReadFileTool,
    WriteFileTool,
    ListDirectoryTool,
)

from app.services.isolated_memory_service import IsolatedMemoryService
from app.services.api_key_service import APIKeyService

class LangChainAgentService:
    def __init__(self):
        self.memory_service = IsolatedMemoryService()
        
        # Configurar ferramentas disponíveis para o agente
        self.tools = self._setup_tools()
        
    def _setup_tools(self) -> List:
        """Configurar ferramentas disponíveis para o agente"""
        tools = [
            DuckDuckGoSearchRun(name="web_search"),
            ReadFileTool(),
            WriteFileTool(),
            ListDirectoryTool(),
        ]
        return tools
    
    def _setup_prompt(self, user_context: str = "") -> ChatPromptTemplate:
        """Configurar o prompt do agente"""
        system_message = """Você é um assistente de IA autônomo e inteligente. Você tem acesso a várias ferramentas que podem ajudá-lo a responder perguntas e realizar tarefas.

Ferramentas disponíveis:
- web_search: Para buscar informações na web
- read_file: Para ler arquivos
- write_file: Para escrever arquivos
- list_directory: Para listar conteúdo de diretórios

Você deve:
1. Analisar a solicitação do usuário
2. Determinar quais ferramentas usar (se necessário)
3. Executar as ferramentas de forma autônoma
4. Fornecer uma resposta completa e útil

Seja proativo e use as ferramentas quando apropriado para fornecer informações precisas e atualizadas."""

        if user_context:
            system_message += f"\n\n{user_context}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        return prompt
    
    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o agente"""
        try:
            api_key_service = APIKeyService()
            openai_api_key = api_key_service.get_api_key(user_id, "openai")
            if not openai_api_key:
                raise ValueError("API key do OpenAI não encontrada para este usuário.")

            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=openai_api_key
            )
            
            # Gerar session_id se não fornecido
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Detectar e processar comando "Lembre-se disso"
            processed_message, fact_saved = self.memory_service.detect_and_save_user_fact(user_message, user_id)
            
            # Recuperar contexto global do usuário
            user_context = self.memory_service.get_user_context_for_chat(user_id)
            
            # Reconfigurar prompt com contexto do usuário
            prompt = self._setup_prompt(user_context)
            
            # Recriar agente com novo prompt
            agent = create_openai_tools_agent(llm, self.tools, prompt)
            
            # Recuperar histórico de conversa e converter para formato LangChain
            history_data = self.memory_service.get_conversation_history(user_id, session_id, limit=20)
            chat_history = []
            
            # Reverter a ordem para mostrar do mais antigo para o mais recente
            for item in reversed(history_data):
                chat_history.append(HumanMessage(content=item["message"]))
                chat_history.append(AIMessage(content=item['response']))
            
            # Criar executor do agente com memória
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5
            )
            
            # Executar o agente
            response = agent_executor.invoke({
                "input": processed_message,
                "chat_history": chat_history
            })
            
            # Se um fato foi salvo, mencionar isso na resposta
            final_response = response["output"]
            if fact_saved:
                final_response = f"✅ Informação salva na memória! {response['output']}"
            
            # Salvar a conversa na memória com atualização de perfil
            self.memory_service.save_message_with_profile_update(
                user_id=user_id,
                session_id=session_id,
                message=user_message,  # Salvar mensagem original
                response=final_response,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "gpt-4o-mini",
                    "provider": "langchain",
                    "fact_saved": fact_saved,
                    "tools_used": response.get("intermediate_steps", []),
                    "agent_type": "openai_tools"
                }
            )
            
            return {
                "message": final_response,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model": "gpt-4o-mini",
                "fact_saved": fact_saved,
                "tools_used": len(response.get("intermediate_steps", []))
            }
            
        except Exception as e:
            raise Exception(f"Erro ao processar mensagem: {str(e)}")
    
    def get_memory(self, user_id: str, session_id: Optional[str] = None) -> List[Dict]:
        """Recuperar memória do agente"""
        try:
            if session_id:
                return self.memory_service.get_conversation_history(user_id, session_id)
            else:
                # Se não há session_id, retorna lista vazia ou histórico geral
                return []
        except Exception as e:
            raise Exception(f"Erro ao recuperar memória: {str(e)}")
    
    def clear_memory(self, user_id: str, session_id: Optional[str] = None) -> None:
        """Limpar memória do agente"""
        try:
            if session_id:
                self.memory_service.clear_conversation_history(user_id, session_id)
            else:
                self.memory_service.clear_user_memory(user_id)
        except Exception as e:
            raise Exception(f"Erro ao limpar memória: {str(e)}")

