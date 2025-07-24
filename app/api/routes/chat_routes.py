from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from app.services.gemini_chat_service import GeminiChatService
from app.services.openai_chat_service import OpenAIChatService
from app.services.groq_chat_service import GroqChatService

chat_bp = Blueprint("chat", __name__)

# Inicializar serviços
gemini_service = GeminiChatService()
openai_service = OpenAIChatService()
groq_service = GroqChatService()

@chat_bp.route("/gemini/chat", methods=["POST"])
@cross_origin()
def gemini_chat():
    """Endpoint para conversar com o Gemini com memória de longo prazo"""
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
        
        # Processar mensagem com o Gemini
        response = gemini_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "timestamp": response["timestamp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem com Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/chat", methods=["POST"])
@cross_origin()
def openai_chat():
    """Endpoint para conversar com o OpenAI com memória de longo prazo"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_message = data.get("message")
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        model = data.get("model")  # Opcional: permite especificar o modelo
        
        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        # Processar mensagem com o OpenAI
        response = openai_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id,
            model=model
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "usage": response["usage"],
            "timestamp": response["timestamp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem com OpenAI: {str(e)}"}), 500

@chat_bp.route("/groq/chat", methods=["POST"])
@cross_origin()
def groq_chat():
    """Endpoint para conversar com o Groq com memória de longo prazo"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_message = data.get("message")
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        model = data.get("model")  # Opcional: permite especificar o modelo
        
        if not user_message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        # Processar mensagem com o Groq
        response = groq_service.process_message(
            user_message=user_message,
            user_id=user_id,
            session_id=session_id,
            model=model
        )
        
        return jsonify({
            "success": True,
            "response": response["message"],
            "session_id": response["session_id"],
            "model": response["model"],
            "usage": response["usage"],
            "timestamp": response["timestamp"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar mensagem com Groq: {str(e)}"}), 500

@chat_bp.route("/gemini/memory", methods=["GET"])
@cross_origin()
def get_gemini_memory():
    """Recuperar memória do chat Gemini para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = gemini_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória do Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/memory", methods=["GET"])
@cross_origin()
def get_openai_memory():
    """Recuperar memória do chat OpenAI para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = openai_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória do OpenAI: {str(e)}"}), 500

@chat_bp.route("/groq/memory", methods=["GET"])
@cross_origin()
def get_groq_memory():
    """Recuperar memória do chat Groq para um usuário específico"""
    try:
        user_id = request.args.get("user_id")
        session_id = request.args.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        memory = groq_service.get_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "memory": memory,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar memória do Groq: {str(e)}"}), 500

@chat_bp.route("/gemini/memory", methods=["DELETE"])
@cross_origin()
def clear_gemini_memory():
    """Limpar memória do chat Gemini para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        gemini_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória do Gemini limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória do Gemini: {str(e)}"}), 500

@chat_bp.route("/openai/memory", methods=["DELETE"])
@cross_origin()
def clear_openai_memory():
    """Limpar memória do chat OpenAI para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        openai_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória do OpenAI limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória do OpenAI: {str(e)}"}), 500

@chat_bp.route("/groq/memory", methods=["DELETE"])
@cross_origin()
def clear_groq_memory():
    """Limpar memória do chat Groq para um usuário específico"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        
        if not user_id:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        groq_service.clear_memory(user_id, session_id)
        
        return jsonify({
            "success": True,
            "message": "Memória do Groq limpa com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao limpar memória do Groq: {str(e)}"}), 500

@chat_bp.route("/chat/health", methods=["GET"])
@cross_origin()
def health_check():
    """Endpoint de verificação de saúde dos chats"""
    return jsonify({
        "success": True,
        "message": "Serviços de chat Gemini, OpenAI e Groq estão funcionando!",
        "services": ["gemini", "openai", "groq"],
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@chat_bp.route("/groq/models", methods=["GET"])
@cross_origin()
def get_groq_models():
    """Endpoint para listar modelos disponíveis no Groq"""
    try:
        models = groq_service.get_available_models()
        
        return jsonify({
            "success": True,
            "models": models,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao recuperar modelos do Groq: {str(e)}"}), 500

