from flask import Blueprint, request, jsonify
from app.services.openai_agent_service import OpenAIAgentService

openai_agent_bp = Blueprint('openai_agent', __name__)
openai_service = OpenAIAgentService()

@openai_agent_bp.route('/chat', methods=['POST'])
def chat_with_openai():
    """
    Endpoint para chat com agente OpenAI.
    
    Payload esperado:
    {
        "message": "Mensagem do usuário",
        "user_id": "ID único do usuário",
        "session_id": "ID da sessão (opcional)",
        "api_key": "Chave da API OpenAI (opcional)",
        "model": "Modelo OpenAI (opcional, padrão: gpt-3.5-turbo)"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Dados JSON não fornecidos"
            }), 400
        
        message = data.get('message')
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        api_key = data.get('api_key')
        model = data.get('model', 'gpt-3.5-turbo')
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Campo 'message' é obrigatório"
            }), 400
        
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Campo 'user_id' é obrigatório"
            }), 400
        
        # Processar mensagem com OpenAI
        result = openai_service.chat_with_openai(
            message=message,
            user_id=user_id,
            session_id=session_id,
            api_key=api_key,
            model=model
        )
        
        if result.get('success'):
            return jsonify({
                "success": True,
                "data": {
                    "response": result.get('response'),
                    "session_id": result.get('session_id'),
                    "timestamp": result.get('timestamp'),
                    "model_used": result.get('model_used')
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.get('error', 'Erro desconhecido'),
                "data": {
                    "session_id": result.get('session_id'),
                    "timestamp": result.get('timestamp')
                }
            }), 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@openai_agent_bp.route('/conversation/summary', methods=['POST'])
def get_conversation_summary():
    """
    Endpoint para obter resumo da conversa.
    
    Payload esperado:
    {
        "user_id": "ID único do usuário",
        "session_id": "ID da sessão"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Dados JSON não fornecidos"
            }), 400
        
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        
        if not user_id or not session_id:
            return jsonify({
                "success": False,
                "error": "Campos 'user_id' e 'session_id' são obrigatórios"
            }), 400
        
        summary = openai_service.get_conversation_summary(user_id, session_id)
        
        return jsonify({
            "success": True,
            "data": summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@openai_agent_bp.route('/conversation/clear', methods=['POST'])
def clear_conversation():
    """
    Endpoint para limpar histórico da conversa.
    
    Payload esperado:
    {
        "user_id": "ID único do usuário",
        "session_id": "ID da sessão"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Dados JSON não fornecidos"
            }), 400
        
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        
        if not user_id or not session_id:
            return jsonify({
                "success": False,
                "error": "Campos 'user_id' e 'session_id' são obrigatórios"
            }), 400
        
        result = openai_service.clear_conversation(user_id, session_id)
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno do servidor: {str(e)}"
        }), 500

@openai_agent_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check do agente OpenAI.
    """
    return jsonify({
        "success": True,
        "message": "OpenAI Agent Service está funcionando",
        "service": "openai_agent",
        "status": "healthy"
    }), 200

