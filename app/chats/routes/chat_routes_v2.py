"""
Rotas de Chat V2 - Integradas com Sistema de Memória Isolado
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from app.chats.services.gemini_chat_service_v2 import GeminiChatServiceV2
import logging

logger = logging.getLogger(__name__)

# Blueprint para as novas rotas
chat_v2_bp = Blueprint("chat_v2", __name__, url_prefix="/api/v2/chat")

# Inicializar serviço
gemini_service_v2 = GeminiChatServiceV2()

@chat_v2_bp.route("/gemini", methods=["POST"])
@cross_origin()
def gemini_chat_v2():
    """Endpoint V2 para conversar com Gemini usando memória isolada"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_message = data.get("message")
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Nova mensagem - User: {user_id}, Session: {session_id}")
        logger.info(f"[CHAT_V2] Mensagem: {user_message[:100]}...")
        
        # Processar mensagem com Gemini V2
        response = gemini_service_v2.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id
        )
        
        logger.info(f"[CHAT_V2] Resposta gerada - Conversation ID: {response.get('conversation_id')}")
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "timestamp": response["timestamp"],
            "memory_command_executed": response.get("memory_command_executed", False),
            "conversation_id": response.get("conversation_id"),
            "context_used": response.get("context_used", False),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao processar mensagem: {str(e)}")
        return jsonify({
            "error": f"Erro ao processar mensagem: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/memory", methods=["GET"])
@cross_origin()
def get_gemini_memory_v2():
    """Recuperar memória do chat Gemini V2"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Recuperando memória - User: {user_id}, Session: {session_id}")
        
        memory = gemini_service_v2.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao recuperar memória: {str(e)}")
        return jsonify({
            "error": f"Erro ao recuperar memória: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/memory", methods=["DELETE"])
@cross_origin()
def clear_gemini_memory_v2():
    """Limpar memória do chat Gemini V2"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Limpando memória - User: {user_id}, Session: {session_id}")
        
        gemini_service_v2.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao limpar memória: {str(e)}")
        return jsonify({
            "error": f"Erro ao limpar memória: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/stats", methods=["GET"])
@cross_origin()
def get_user_stats_v2():
    """Obter estatísticas do usuário"""
    try:
        user_id = request.args.get("user_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Obtendo estatísticas - User: {user_id}")
        
        stats = gemini_service_v2.get_user_stats(user_id)
        
        return jsonify({
            "success": True,
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            "error": f"Erro ao obter estatísticas: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/profile", methods=["PUT"])
@cross_origin()
def update_user_profile_v2():
    """Atualizar perfil do usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        profile_updates = data.get("profile_updates")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        if not profile_updates:
            return jsonify({"error": "profile_updates é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Atualizando perfil - User: {user_id}")
        
        success = gemini_service_v2.update_user_profile(user_id, profile_updates)
        
        return jsonify({
            "success": success,
            "message": "Perfil atualizado com sucesso" if success else "Falha ao atualizar perfil",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200 if success else 500
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao atualizar perfil: {str(e)}")
        return jsonify({
            "error": f"Erro ao atualizar perfil: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/fact", methods=["POST"])
@cross_origin()
def save_user_fact_v2():
    """Salvar fato específico sobre o usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        fact_content = data.get("fact_content")
        fact_type = data.get("fact_type", "manual")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        if not fact_content:
            return jsonify({"error": "fact_content é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Salvando fato - User: {user_id}")
        
        fact_id = gemini_service_v2.save_user_fact(user_id, fact_content, fact_type)
        
        return jsonify({
            "success": True,
            "fact_id": fact_id,
            "message": "Fato salvo com sucesso",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao salvar fato: {str(e)}")
        return jsonify({
            "error": f"Erro ao salvar fato: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/gemini/context", methods=["GET"])
@cross_origin()
def get_conversation_context_v2():
    """Obter contexto completo da conversa"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        if not session_id:
            return jsonify({"error": "session_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Obtendo contexto - User: {user_id}, Session: {session_id}")
        
        context = gemini_service_v2.get_conversation_context(user_id, session_id)
        
        return jsonify({
            "success": True,
            "context": context,
            "context_length": len(context),
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro ao obter contexto: {str(e)}")
        return jsonify({
            "error": f"Erro ao obter contexto: {str(e)}",
            "version": "v2_isolated"
        }), 500

@chat_v2_bp.route("/health", methods=["GET"])
@cross_origin()
def health_check_v2():
    """Endpoint de verificação de saúde do Chat V2"""
    try:
        return jsonify({
            "success": True,
            "message": "Chat V2 com memória isolada funcionando!",
            "version": "v2_isolated",
            "features": [
                "isolated_memory",
                "conversation_history",
                "user_profiles",
                "user_facts",
                "memory_commands",
                "context_awareness"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro no health check: {str(e)}")
        return jsonify({
            "error": f"Erro no health check: {str(e)}",
            "version": "v2_isolated"
        }), 500

# Endpoint para migração de dados (opcional)
@chat_v2_bp.route("/migrate", methods=["POST"])
@cross_origin()
def migrate_user_data():
    """Migrar dados do usuário do sistema antigo para o isolado"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        logger.info(f"[CHAT_V2] Iniciando migração - User: {user_id}")
        
        # Aqui você pode implementar a lógica de migração se necessário
        # Por enquanto, apenas retornamos sucesso
        
        return jsonify({
            "success": True,
            "message": "Migração não implementada - sistema isolado é independente",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "v2_isolated"
        }), 200
        
    except Exception as e:
        logger.error(f"[CHAT_V2] Erro na migração: {str(e)}")
        return jsonify({
            "error": f"Erro na migração: {str(e)}",
            "version": "v2_isolated"
        }), 500

