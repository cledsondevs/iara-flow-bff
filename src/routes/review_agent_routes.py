"""
Rotas da API para o agente de análise de reviews
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json

from src.services.review_agent_service import ReviewAgentService

# Criar blueprint para as rotas do agente de reviews
review_agent_bp = Blueprint('review_agent', __name__, url_prefix='/api/review-agent')

# Instância global do serviço
review_agent = ReviewAgentService()

@review_agent_bp.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API do agente de reviews"""
    try:
        status = review_agent.get_system_status()
        return jsonify({
            "success": True,
            "status": "healthy",
            "system_status": status,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/autonomous/start', methods=['POST'])
def start_autonomous_mode():
    """Iniciar modo autônomo do agente"""
    try:
        result = review_agent.start_autonomous_mode()
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/autonomous/stop', methods=['POST'])
def stop_autonomous_mode():
    """Parar modo autônomo do agente"""
    try:
        result = review_agent.stop_autonomous_mode()
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps', methods=['POST'])
def add_app():
    """Adicionar aplicativo para monitoramento"""
    try:
        data = request.get_json()
        
        if not data or 'package_name' not in data or 'app_name' not in data:
            return jsonify({
                "success": False,
                "error": "package_name e app_name são obrigatórios"
            }), 400
        
        result = review_agent.add_app_for_monitoring(
            package_name=data['package_name'],
            app_name=data['app_name'],
            stores=data.get('stores', ['google_play']),
            collection_frequency=data.get('collection_frequency', 6)
        )
        
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/collect', methods=['POST'])
def collect_reviews(package_name):
    """Coletar reviews para um aplicativo específico"""
    try:
        result = review_agent.collect_reviews_for_app(package_name)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/analyze', methods=['POST'])
def analyze_sentiment(package_name):
    """Analisar sentimento para um aplicativo específico"""
    try:
        result = review_agent.analyze_app_sentiment(package_name)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/backlog', methods=['POST'])
def generate_backlog(package_name):
    """Gerar backlog para um aplicativo específico"""
    try:
        data = request.get_json() or {}
        days = data.get('days', 7)
        
        result = review_agent.generate_backlog_for_app(package_name, days)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/dashboard', methods=['GET'])
def get_app_dashboard(package_name):
    """Obter dashboard completo de um aplicativo"""
    try:
        result = review_agent.get_app_dashboard(package_name)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/collect-all', methods=['POST'])
def collect_all_reviews():
    """Coletar reviews de todos os aplicativos configurados"""
    try:
        result = review_agent.collector.collect_all_pending()
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/analyze-all', methods=['POST'])
def analyze_all_reviews():
    """Analisar sentimento de todos os reviews pendentes"""
    try:
        result = review_agent.analyzer.analyze_pending_reviews()
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/backlog/summary', methods=['GET'])
def get_backlog_summary():
    """Obter resumo geral do backlog"""
    try:
        package_name = request.args.get('package_name')
        result = review_agent.backlog_generator.get_backlog_summary(package_name)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/sentiment/summary', methods=['GET'])
def get_sentiment_summary():
    """Obter resumo de sentimentos"""
    try:
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        result = review_agent.analyzer.get_sentiment_summary(package_name, days)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/sentiment/trends', methods=['GET'])
def get_sentiment_trends():
    """Obter tendências de sentimento"""
    try:
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório"
            }), 400
        
        result = review_agent.memory.get_sentiment_trends(package_name, days)
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/query', methods=['POST'])
def process_query():
    """Processar consulta do usuário"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "error": "query é obrigatório"
            }), 400
        
        user_id = data.get('user_id', 'anonymous')
        query = data['query']
        
        result = review_agent.process_user_query(query, user_id)
        return jsonify({
            "success": True,
            "result": result,
            "query": query,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/reports/comprehensive', methods=['GET'])
def get_comprehensive_report():
    """Gerar relatório abrangente do sistema"""
    try:
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        # Status do sistema
        system_status = review_agent.get_system_status()
        
        # Se package_name especificado, focar nele
        if package_name:
            dashboard = review_agent.get_app_dashboard(package_name)
            sentiment_summary = review_agent.analyzer.get_sentiment_summary(package_name, days)
            backlog_summary = review_agent.backlog_generator.get_backlog_summary(package_name)
            
            report = {
                "type": "app_specific",
                "package_name": package_name,
                "period_days": days,
                "dashboard": dashboard,
                "sentiment_analysis": sentiment_summary,
                "backlog_analysis": backlog_summary,
                "system_status": system_status
            }
        else:
            # Relatório geral
            sentiment_summary = review_agent.analyzer.get_sentiment_summary(days=days)
            backlog_summary = review_agent.backlog_generator.get_backlog_summary()
            
            report = {
                "type": "system_wide",
                "period_days": days,
                "sentiment_analysis": sentiment_summary,
                "backlog_analysis": backlog_summary,
                "system_status": system_status
            }
        
        return jsonify({
            "success": True,
            "report": report,
            "generated_at": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/memory/patterns', methods=['GET'])
def get_memory_patterns():
    """Obter padrões aprendidos pela memória de longo prazo"""
    try:
        package_name = request.args.get('package_name')
        pattern_type = request.args.get('pattern_type')
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório"
            }), 400
        
        patterns = review_agent.memory.get_sentiment_patterns(package_name, pattern_type)
        return jsonify({
            "success": True,
            "patterns": patterns,
            "package_name": package_name,
            "pattern_type": pattern_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/optimization/suggestions', methods=['GET'])
def get_optimization_suggestions():
    """Obter sugestões de otimização baseadas na memória"""
    try:
        package_name = request.args.get('package_name')
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório"
            }), 400
        
        # Obter backlog atual para análise
        backlog_summary = review_agent.backlog_generator.get_backlog_summary(package_name)
        current_backlog = backlog_summary.get('high_priority_items', [])
        
        suggestions = review_agent.memory.get_backlog_optimization_suggestions(current_backlog)
        
        return jsonify({
            "success": True,
            "suggestions": suggestions,
            "package_name": package_name,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

# Tratamento de erros
@review_agent_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint não encontrado",
        "timestamp": datetime.utcnow().isoformat()
    }), 404

@review_agent_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Método não permitido",
        "timestamp": datetime.utcnow().isoformat()
    }), 405

@review_agent_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Erro interno do servidor",
        "timestamp": datetime.utcnow().isoformat()
    }), 500

