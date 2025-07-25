import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import google.generativeai as genai

from app.services.memory_service import MemoryService
from app.config.settings import Config

class GeminiAgentService:
    def __init__(self):
        self.memory_service = MemoryService()

    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o agente Gemini"""
        try:
            # Usar chave padrão do sistema
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Gerar session_id se não fornecido
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Recuperar histórico de conversa e perfil do usuário
            chat_history = self.memory_service.get_conversation_history(user_id, session_id)
            user_profile = self.memory_service.get_user_profile(user_id)
            
            # Construir contexto da conversa
            context = self._build_context(chat_history, user_message, user_profile.get("profile_data", {}))
            
            # Gerar resposta com Gemini
            response = model.generate_content(context)
            
            # Extrair texto da resposta
            response_text = response.text if response.text else "Desculpe, não consegui gerar uma resposta."
            
            # Salvar a conversa na memória
            self.memory_service.save_conversation(
                user_id=user_id,
                session_id=session_id,
                message=user_message,
                response=response_text,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "gemini-1.5-flash",
                    "session_id": session_id
                }
            )
            
            return {
                "message": response_text,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao processar mensagem com Gemini: {str(e)}")
    
    def _build_context(self, chat_history: List[Dict], current_message: str, user_profile: Dict) -> str:
        """Construir contexto da conversa para o Gemini"""
        context = "Você é um assistente de IA conversacional amigável e prestativo. "
        context += "Responda de forma clara, útil e em português brasileiro.\n\n"
        
        if user_profile and user_profile.get("name"):
            context += f"O nome do usuário é {user_profile['name']}. Lembre-se disso para futuras interações.\n\n"
        
        # Adicionar histórico da conversa
        if chat_history:
            context += "Histórico da conversa:\n"
            for entry in chat_history[-20:]:  # Últimas 20 mensagens
                if entry.get("type") == "human":
                    context += f"Usuário: {entry.get('content', '')}\n"
                elif entry.get("type") == "ai":
                    context += f"Assistente: {entry.get('content', '')}\n"
            context += "\n"
        
        # Adicionar mensagem atual
        context += f"Usuário: {current_message}\n"
        context += "Assistente: "
        
        return context
    
    def get_memory(self, user_id: str, session_id: Optional[str] = None) -> List[Dict]:
        """Recuperar memória do agente"""
        try:
            return self.memory_service.get_conversation_history(user_id, session_id)
        except Exception as e:
            raise Exception(f"Erro ao recuperar memória: {str(e)}")
    
    def clear_memory(self, user_id: str, session_id: Optional[str] = None) -> None:
        """Limpar memória do agente"""
        try:
            self.memory_service.clear_conversation_history(user_id, session_id)
        except Exception as e:
            raise Exception(f"Erro ao limpar memória: {str(e)}")



