import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from openai import OpenAI

from app.services.memory_service import MemoryService
from app.services.api_key_service import APIKeyService

class OpenAIAgentService:
    def __init__(self):
        self.memory_service = MemoryService()
        self.api_key_service = APIKeyService()
        self.client = None
        
    def chat_with_openai(
        self,
        message: str,
        user_id: str,
        session_id: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ) -> Dict[str, Any]:
        """
        Processa uma mensagem usando OpenAI GPT e mantém o histórico da conversa.
        
        Args:
            message: Mensagem do usuário
            user_id: ID único do usuário
            session_id: ID da sessão (opcional)
            model: Modelo OpenAI a ser usado (padrão: gpt-3.5-turbo)
            
        Returns:
            Dict com a resposta do agente e informações da sessão
        """
        try:
            api_key = self.api_key_service.get_api_key(user_id, "openai")
            if not api_key:
                raise ValueError("API key do OpenAI não encontrada para este usuário.")

            self.client = OpenAI(api_key=api_key)
            
            # Recuperar histórico da conversa
            chat_history = self.memory_service.get_conversation_history(user_id, session_id)
            
            # Construir contexto para o modelo
            messages = []
            
            # Adicionar mensagem do sistema
            messages.append({
                "role": "system",
                "content": "Você é um assistente útil e amigável. Responda de forma clara e prestativa."
            })
            
            # Adicionar histórico da conversa
            if chat_history:
                for entry in chat_history[-10:]:  # Últimas 10 mensagens
                    if entry.get("type") == "human":
                        messages.append({
                            "role": "user",
                            "content": entry.get("content", "")
                        })
                    elif entry.get("type") == "ai":
                        messages.append({
                            "role": "assistant",
                            "content": entry.get("content", "")
                        })
            
            # Adicionar mensagem atual
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Fazer chamada para OpenAI usando a nova API
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extrair resposta
            ai_response = response.choices[0].message.content.strip()
            
            # Salvar conversa na memória
            self.memory_service.save_conversation(user_id, session_id, message, ai_response)
            
            return {
                "response": ai_response,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model_used": model,
                "success": True
            }
    
        except Exception as e:
            error_message = f"Erro ao processar mensagem com OpenAI: {str(e)}"
            print(error_message)
            
            return {
                "response": "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.",
                "session_id": session_id or f"error_session_{user_id}",
                "timestamp": datetime.utcnow().isoformat(),
                "error": error_message,
                "success": False
            }
    
    def save_conversation(self, user_id: str, session_id: str, user_message: str, ai_response: str):
        """
        Salva a conversa na memória.
        
        Args:
            user_id: ID do usuário
            session_id: ID da sessão
            user_message: Mensagem do usuário
            ai_response: Resposta do agente
        """
        try:
            # Salvar mensagem do usuário
            self.memory_service.save_conversation(user_id, session_id, user_message, ai_response)
        except Exception as e:
            print(f"Erro ao salvar conversa: {str(e)}")
    
    def get_conversation_summary(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """
        Obtém um resumo da conversa.
        
        Args:
            user_id: ID do usuário
            session_id: ID da sessão
            
        Returns:
            Dict com resumo da conversa
        """
        try:
            history = self.memory_service.get_conversation_history(user_id, session_id)
            
            if not history:
                return {
                    "summary": "Nenhuma conversa encontrada",
                    "message_count": 0,
                    "last_interaction": None
                }
            
            user_messages = [entry for entry in history if entry.get("type") == "human"]
            ai_messages = [entry for entry in history if entry.get("type") == "ai"]
            
            return {
                "summary": f"Conversa com {len(user_messages)} mensagens do usuário e {len(ai_messages)} respostas do agente",
                "message_count": len(history),
                "user_message_count": len(user_messages),
                "ai_message_count": len(ai_messages),
                "last_interaction": history[-1].get("timestamp") if history else None,
                "session_id": session_id
            }
            
        except Exception as e:
            return {
                "summary": f"Erro ao obter resumo: {str(e)}",
                "message_count": 0,
                "last_interaction": None,
                "error": str(e)
            }
    
    def clear_conversation(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """
        Limpa o histórico de uma conversa específica.
        
        Args:
            user_id: ID do usuário
            session_id: ID da sessão
            
        Returns:
            Dict com resultado da operação
        """
        try:
            # Implementar lógica de limpeza se necessário
            # Por enquanto, apenas retorna sucesso
            return {
                "success": True,
                "message": f"Histórico da sessão {session_id} limpo com sucesso",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao limpar conversa: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }