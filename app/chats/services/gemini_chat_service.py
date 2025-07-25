import os
import uuid
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Optional, Any
from app.services.memory_service import MemoryService
from app.config.settings import Config


class GeminiChatService:
    def __init__(self):
        self.memory_service = MemoryService()
        
        # Configurar API do Gemini
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas configurações")
        
        genai.configure(api_key=api_key)
        
        # Configurar modelo
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o Gemini"""
        try:
            # Gerar session_id se não fornecido
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Detectar e processar comando "Lembre-se disso"
            processed_message, fact_saved = self.memory_service.detect_and_save_user_fact(user_message, user_id)
            
            # Recuperar histórico de conversa
            history_data = self.memory_service.get_conversation_history(user_id, session_id, limit=20)
            
            # Recuperar contexto global do usuário
            user_context = self.memory_service.get_user_context_for_chat(user_id)
            
            # Construir contexto da conversa
            conversation_context = self._build_conversation_context(history_data, processed_message, user_context)
            
            # Gerar resposta com o Gemini
            response = self.model.generate_content(conversation_context)
            
            if not response.text:
                raise Exception("Gemini não retornou uma resposta válida")
            
            # Se um fato foi salvo, mencionar isso na resposta
            final_response = response.text
            if fact_saved:
                final_response = f"✅ Informação salva na memória! {response.text}"
            
            # Salvar a conversa na memória com atualização de perfil
            self.memory_service.save_message_with_profile_update(
                user_id=user_id,
                session_id=session_id,
                message=user_message,  # Salvar mensagem original
                response=final_response,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "gemini-1.5-flash",
                    "provider": "google",
                    "fact_saved": fact_saved
                }
            )
            
            return {
                "message": final_response,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model": "gemini-1.5-flash",
                "fact_saved": fact_saved
            }
            
        except Exception as e:
            raise Exception(f"Erro ao processar mensagem com Gemini: {str(e)}")
    
    def _build_conversation_context(self, history_data: List[Dict], current_message: str, user_context: str = "") -> str:
        """Construir contexto da conversa para o Gemini"""
        context = "Você é um assistente de IA útil e inteligente. Mantenha o contexto da conversa anterior.\n\n"
        
        # Adicionar contexto do usuário se disponível
        if user_context:
            context += f"{user_context}\n\n"
        
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

