"""
Serviço de Chat Gemini V2 - Integrado com Sistema de Memória Isolado
"""

import uuid
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Optional, Any
from app.services.isolated_memory_service import IsolatedMemoryService
from app.config.settings import Config
import logging

logger = logging.getLogger(__name__)

class GeminiChatServiceV2:
    """
    Serviço de chat Gemini integrado com sistema de memória isolado
    """
    
    def __init__(self):
        self.memory_service = IsolatedMemoryService()
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("[GEMINI_V2] Serviço inicializado com memória isolada")
        
    def process_message(self, user_message: str, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Processar mensagem do usuário com o Gemini usando memória isolada"""
        try:
            # Garantir session_id
            if session_id is None or session_id == "":
                session_id = str(uuid.uuid4())
            
            logger.info(f"[GEMINI_V2] Processando mensagem - User: {user_id}, Session: {session_id}")
            
            # Configurar API key
            default_key = "AIzaSyBPHQNceQTWTQ15D5TJlu_L2Gcd5uNODUk"
            genai.configure(api_key=default_key)
            
            # Detectar e processar comandos de memória
            processed_message, memory_command_executed = self.memory_service.detect_and_save_memory_command(
                user_id, user_message
            )
            
            # Se foi um comando de memória, usar a mensagem processada
            message_for_ai = processed_message if memory_command_executed else user_message
            
            # Obter contexto completo do usuário
            user_context = self.memory_service.get_user_context_isolated(user_id)
            # Construir prompt com contexto
            full_prompt = self._build_conversation_prompt(message_for_ai, user_context)
            
            logger.info(f"[GEMINI_V2] Gerando resposta com contexto de {len(user_context)} caracteres")
            
            # Gerar resposta com Gemini
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                raise Exception("Gemini não retornou uma resposta válida")
            
            # Preparar resposta final
            final_response = response.text
            if memory_command_executed:
                final_response = f"✅ {processed_message}\n\n{response.text}"
            
            # Salvar conversa no sistema isolado
            conversation_id = self.memory_service.save_conversation_isolated(
                user_id=user_id,
                session_id=session_id,
                user_message=user_message,  # Salvar mensagem original
                assistant_response=final_response,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "gemini-1.5-flash",
                    "provider": "google",
                    "memory_command": memory_command_executed,
                    "conversation_id": conversation_id if 'conversation_id' in locals() else None,
                    "context_length": len(user_context)
                }
            )
            
            logger.info(f"[GEMINI_V2] Resposta gerada e salva - Conversation ID: {conversation_id}")
            
            return {
                "message": final_response,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
                "model": "gemini-1.5-flash",
                "memory_command_executed": memory_command_executed,
                "conversation_id": conversation_id,
                "context_used": len(user_context) > 0
            }
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao processar mensagem: {str(e)}")
            raise Exception(f"Erro ao processar mensagem com Gemini V2: {str(e)}")
    
    def _build_conversation_prompt(self, current_message: str, user_context: str = "") -> str:
        """Construir prompt completo para o Gemini"""
        
        base_prompt = """Você é um assistente de IA útil e inteligente. Você tem acesso ao contexto e histórico do usuário para fornecer respostas personalizadas e relevantes.

INSTRUÇÕES IMPORTANTES:
- Use o contexto fornecido para personalizar suas respostas
- Lembre-se de informações importantes sobre o usuário
- Seja natural e conversacional
- Se o usuário mencionar algo que já foi discutido antes, demonstre que você lembra
- Mantenha consistência com conversas anteriores

"""
        
        # Adicionar contexto do usuário se disponível
        if user_context:
            base_prompt += f"CONTEXTO DO USUÁRIO:\n{user_context}\n\n"
        
        # Adicionar mensagem atual
        base_prompt += f"MENSAGEM ATUAL DO USUÁRIO:\n{current_message}\n\n"
        base_prompt += "RESPOSTA DO ASSISTENTE:"
        
        return base_prompt
    
    def get_memory(self, user_id: str, session_id: Optional[str] = None) -> List[Dict]:
        """Recuperar memória do chat usando sistema isolado"""
        try:
            logger.info(f"[GEMINI_V2] Recuperando memória - User: {user_id}")
            
            # Sempre recuperar histórico global
            history = self.memory_service.get_conversation_history_isolated(user_id, limit=20)
            
            # Recuperar informações gerais do usuário
            profile = self.memory_service.get_user_profile_isolated(user_id)
            facts = self.memory_service.get_user_facts_isolated(user_id)
            stats = self.memory_service.get_memory_stats_isolated(user_id)
            
            return {
                "history": history,
                "profile": profile,
                "facts": facts,
                "stats": stats
            }
                
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao recuperar memória: {str(e)}")
            raise Exception(f"Erro ao recuperar memória: {str(e)}")
    
    def clear_memory(self, user_id: str, session_id: Optional[str] = None):
        """Limpar memória do chat usando sistema isolado"""
        try:
            logger.info(f"[GEMINI_V2] Limpando memória - User: {user_id}")
            
            if session_id:
                # Limpar apenas conversas da sessão específica
                # (implementar se necessário)
                logger.warning("[GEMINI_V2] Limpeza por sessão não implementada, limpando tudo")
            
            # Limpar toda a memória do usuário
            success = self.memory_service.clear_user_memory_isolated(user_id)
            
            if not success:
                raise Exception("Falha ao limpar memória do usuário")
                
            logger.info(f"[GEMINI_V2] Memória limpa com sucesso - User: {user_id}")
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao limpar memória: {str(e)}")
            raise Exception(f"Erro ao limpar memória: {str(e)}")
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Obter estatísticas do usuário"""
        try:
            logger.info(f"[GEMINI_V2] Obtendo estatísticas - User: {user_id}")
            
            stats = self.memory_service.get_memory_stats_isolated(user_id)
            profile = self.memory_service.get_user_profile_isolated(user_id)
            facts = self.memory_service.get_user_facts_isolated(user_id)
            
            return {
                "stats": stats,
                "profile_summary": {
                    "has_profile": bool(profile["profile_data"]),
                    "profile_version": profile.get("version", 0),
                    "last_updated": profile.get("updated_at", ""),
                    "total_facts": len(facts)
                },
                "service_version": "gemini_v2_isolated"
            }
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao obter estatísticas: {str(e)}")
            return {"error": str(e)}
    
    def save_user_fact(self, user_id: str, fact_content: str, fact_type: str = "manual") -> str:
        """Salvar fato específico sobre o usuário"""
        try:
            logger.info(f"[GEMINI_V2] Salvando fato manual - User: {user_id}")
            
            fact_id = self.memory_service.save_user_fact_isolated(user_id, fact_content, fact_type)
            
            logger.info(f"[GEMINI_V2] Fato salvo - ID: {fact_id}")
            return fact_id
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao salvar fato: {str(e)}")
            raise Exception(f"Erro ao salvar fato: {str(e)}")
    
    def update_user_profile(self, user_id: str, profile_updates: Dict) -> bool:
        """Atualizar perfil do usuário"""
        try:
            logger.info(f"[GEMINI_V2] Atualizando perfil - User: {user_id}")
            
            success = self.memory_service.update_user_profile_isolated(user_id, profile_updates)
            
            logger.info(f"[GEMINI_V2] Perfil atualizado - Success: {success}")
            return success
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao atualizar perfil: {str(e)}")
            raise Exception(f"Erro ao atualizar perfil: {str(e)}")
    
    def get_conversation_context(self, user_id: str, session_id: str) -> str:
        """Obter contexto completo da conversa"""
        try:
            logger.info(f"[GEMINI_V2] Obtendo contexto - User: {user_id}, Session: {session_id}")
            
            context = self.memory_service.get_user_context_isolated(user_id, session_id)
            
            logger.info(f"[GEMINI_V2] Contexto obtido - {len(context)} caracteres")
            return context
            
        except Exception as e:
            logger.error(f"[GEMINI_V2] Erro ao obter contexto: {str(e)}")
            return ""

