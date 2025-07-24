import os
import uuid
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.services.memory_service import MemoryService


class GeminiChatService:
    def __init__(self):
        self.memory_service = MemoryService()
        
        # Configurar API do Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente")
        
        genai.configure(api_key=api_key)
        
        # Configurar modelo
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o Gemini"""
        try:
            # Gerar session_id se não fornecido
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Recuperar histórico de conversa
            history_data = self.memory_service.get_conversation_history(user_id, session_id, limit=20)
            
            # Construir contexto da conversa
            conversation_context = self._build_conversation_context(history_data, user_message)
            
            # Gerar resposta com o Gemini
            response = self.model.generate_content(conversation_context)
            
            if not response.text:
                raise Exception("Gemini não retornou uma resposta válida")
            
            # Salvar a conversa na memória
            self.memory_service.save_message(
                user_id=user_id,
                session_id=session_id,
                message=user_message,
                response=response.text,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "gemini-1.5-flash",
                    "provider": "google"
                }
            )
            
            return {
                "message": response.text,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model": "gemini-1.5-flash"
            }
            
        except Exception as e:
            raise Exception(f"Erro ao processar mensagem com Gemini: {str(e)}")
    
    def _build_conversation_context(self, history_data: List[Dict], current_message: str) -> str:
        """Construir contexto da conversa para o Gemini"""
        context = "Você é um assistente de IA útil e inteligente. Mantenha o contexto da conversa anterior.\n\n"
        
        # Adicionar histórico (em ordem cronológica)
        if history_data:
            context += "Histórico da conversa:\n"
            # Reverter a ordem para mostrar do mais antigo para o mais recente
            for item in reversed(history_data):
                context += f"Usuário: {item['message']}\n"
                context += f"Assistente: {item['response']}\n\n"
        
        # Adicionar mensagem atual
        context += f"Usuário: {current_message}\n"
        context += "Assistente: "
        
        return context
    
    def get_memory(self, user_id: str, session_id: Optional[str] = None) -> List[Dict]:
        """Recuperar memória do chat"""
        try:
            if session_id:
                return self.memory_service.get_conversation_history(user_id, session_id)
            else:
                return []
        except Exception as e:
            raise Exception(f"Erro ao recuperar memória: {str(e)}")
    
    def clear_memory(self, user_id: str, session_id: Optional[str] = None) -> None:
        """Limpar memória do chat"""
        try:
            if session_id:
                self.memory_service.clear_conversation_history(user_id, session_id)
            else:
                self.memory_service.clear_user_memory(user_id)
        except Exception as e:
            raise Exception(f"Erro ao limpar memória: {str(e)}")

