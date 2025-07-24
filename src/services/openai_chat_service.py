import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from openai import OpenAI
from src.services.memory_service import MemoryService


class OpenAIChatService:
    def __init__(self):
        self.memory_service = MemoryService()
        
        # Configurar cliente OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Modelo padrão
        
    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o OpenAI"""
        try:
            # Gerar session_id se não fornecido
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Usar modelo especificado ou padrão
            selected_model = model or self.model
            
            # Recuperar histórico de conversa
            history_data = self.memory_service.get_conversation_history(user_id, session_id, limit=20)
            
            # Recuperar contexto global do usuário
            user_context = self.memory_service.get_user_context_for_chat(user_id)
            
            # Construir mensagens para o OpenAI
            messages = self._build_messages(history_data, user_message, user_context)
            
            # Gerar resposta com o OpenAI
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise Exception("OpenAI não retornou uma resposta válida")
            
            assistant_response = response.choices[0].message.content
            
            # Salvar a conversa na memória com atualização de perfil
            self.memory_service.save_message_with_profile_update(
                user_id=user_id,
                session_id=session_id,
                message=user_message,
                response=assistant_response,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": selected_model,
                    "provider": "openai",
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                        "total_tokens": response.usage.total_tokens if response.usage else 0
                    }
                }
            )
            
            return {
                "message": assistant_response,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model": selected_model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                }
            }
            
        except Exception as e:
            raise Exception(f"Erro ao processar mensagem com OpenAI: {str(e)}")
    
    def _build_messages(self, history_data: List[Dict], current_message: str, user_context: str = "") -> List[Dict]:
        """Construir mensagens para o OpenAI Chat API"""
        system_content = "Você é um assistente de IA útil e inteligente. Mantenha o contexto da conversa anterior e forneça respostas precisas e úteis."
        if user_context:
            system_content += f" {user_context}"
        
        messages = [
            {
                "role": "system",
                "content": system_content
            }
        ]
        
        # Adicionar histórico (em ordem cronológica)
        if history_data:
            # Reverter a ordem para mostrar do mais antigo para o mais recente
            for item in reversed(history_data):
                messages.append({
                    "role": "user",
                    "content": item['message']
                })
                messages.append({
                    "role": "assistant",
                    "content": item['response']
                })
        
        # Adicionar mensagem atual
        messages.append({
            "role": "user",
            "content": current_message
        })
        
        return messages
    
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

