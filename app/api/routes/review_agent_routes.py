"""
Rotas da API para o agente de análise de reviews
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json

from app.services.review_agent_service import ReviewAgentService
from app.services.email_service import EmailSenderService

# Criar blueprint para as rotas do agente de reviews
review_agent_bp = Blueprint('review_agent', __name__, url_prefix='/api/review-agent')

# Instância global do serviço
review_agent = ReviewAgentService()

def get_logs_from_request():
    """Extrair logs da requisição se disponíveis"""
    return []

def add_log(logs, message):
    """Adicionar log à lista"""
    logs.append(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {message}")
    return logs

@review_agent_bp.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API do agente de reviews"""
    try:
        logs = []
        add_log(logs, "Verificando status do sistema")
        
        status = review_agent.get_system_status()
        add_log(logs, "Status do sistema obtido com sucesso")
        
        return jsonify({
            "success": True,
            "status": "healthy",
            "system_status": status,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao verificar status: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/autonomous/start', methods=['POST'])
def start_autonomous_mode():
    """Iniciar modo autônomo do agente"""
    try:
        logs = []
        add_log(logs, "Iniciando modo autônomo")
        
        result = review_agent.start_autonomous_mode()
        add_log(logs, "Modo autônomo iniciado com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao iniciar modo autônomo: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/autonomous/stop', methods=['POST'])
def stop_autonomous_mode():
    """Parar modo autônomo do agente"""
    try:
        logs = []
        add_log(logs, "Parando modo autônomo")
        
        result = review_agent.stop_autonomous_mode()
        add_log(logs, "Modo autônomo parado com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao parar modo autônomo: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps', methods=['POST'])
def add_app():
    """Adicionar aplicativo para monitoramento"""
    try:
        logs = []
        data = request.get_json()
        
        if not data or 'package_name' not in data or 'app_name' not in data:
            return jsonify({
                "success": False,
                "error": "package_name e app_name são obrigatórios",
                "logs": ["Dados obrigatórios não fornecidos"]
            }), 400
        
        add_log(logs, f"Adicionando app {data['app_name']} para monitoramento")
        
        result = review_agent.add_app_for_monitoring(
            package_name=data['package_name'],
            app_name=data['app_name'],
            stores=data.get('stores', ['google_play']),
            collection_frequency=data.get('collection_frequency', 6)
        )
        
        add_log(logs, "App adicionado com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao adicionar app: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/collect', methods=['POST'])
def collect_reviews(package_name):
    """Coletar reviews para um aplicativo específico"""
    try:
        logs = []
        add_log(logs, f"Iniciando coleta de reviews para {package_name}")
        
        result = review_agent.collect_reviews_for_app(package_name)
        add_log(logs, f"Coleta concluída: {result.get('reviews_collected', 0)} reviews coletados")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro na coleta de reviews: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/analyze', methods=['POST'])
def analyze_sentiment(package_name):
    """Analisar sentimento para um aplicativo específico"""
    try:
        logs = []
        add_log(logs, f"Iniciando análise de sentimento para {package_name}")
        
        result = review_agent.analyze_app_sentiment(package_name)
        add_log(logs, f"Análise concluída: {result.get('reviews_analyzed', 0)} reviews analisados")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro na análise de sentimento: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/backlog', methods=['POST'])
def generate_backlog(package_name):
    """Gerar backlog para um aplicativo específico"""
    try:
        logs = []
        data = request.get_json() or {}
        days = data.get('days', 7)
        
        add_log(logs, f"Gerando backlog para {package_name} (últimos {days} dias)")
        
        result = review_agent.generate_backlog_for_app(package_name, days)
        add_log(logs, f"Backlog gerado: {result.get('total_items', 0)} itens criados")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro na geração de backlog: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/apps/<package_name>/dashboard', methods=['GET'])
def get_app_dashboard(package_name):
    """Obter dashboard completo de um aplicativo"""
    try:
        logs = []
        add_log(logs, f"Obtendo dashboard para {package_name}")
        
        result = review_agent.get_app_dashboard(package_name)
        add_log(logs, "Dashboard obtido com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter dashboard: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/collect-all', methods=['POST'])
def collect_all_reviews():
    """Coletar reviews de todos os aplicativos configurados"""
    try:
        logs = []
        add_log(logs, "Iniciando coleta de todos os reviews")
        
        result = review_agent.collector.collect_all_pending()
        add_log(logs, f"Coleta concluída para todos os apps")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro na coleta geral: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/analyze-all', methods=['POST'])
def analyze_all_reviews():
    """Analisar sentimento de todos os reviews pendentes"""
    try:
        logs = []
        add_log(logs, "Iniciando análise de todos os reviews pendentes")
        
        result = review_agent.analyzer.analyze_pending_reviews()
        add_log(logs, "Análise concluída para todos os reviews pendentes")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro na análise geral: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/backlog/summary', methods=['GET'])
def get_backlog_summary():
    """Obter resumo geral do backlog"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        add_log(logs, f"Obtendo resumo do backlog{' para ' + package_name if package_name else ''}")
        
        result = review_agent.backlog_generator.get_backlog_summary(package_name)
        add_log(logs, "Resumo do backlog obtido com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter resumo do backlog: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/sentiment/summary', methods=['GET'])
def get_sentiment_summary():
    """Obter resumo de sentimentos"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        add_log(logs, f"Obtendo resumo de sentimentos{' para ' + package_name if package_name else ''} (últimos {days} dias)")
        
        result = review_agent.analyzer.get_sentiment_summary(package_name, days)
        add_log(logs, "Resumo de sentimentos obtido com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter resumo de sentimentos: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/sentiment/trends', methods=['GET'])
def get_sentiment_trends():
    """Obter tendências de sentimento"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório",
                "logs": ["package_name não fornecido"]
            }), 400
        
        add_log(logs, f"Obtendo tendências de sentimento para {package_name} (últimos {days} dias)")
        
        result = review_agent.memory.get_sentiment_trends(package_name, days)
        add_log(logs, "Tendências de sentimento obtidas com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter tendências: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/query', methods=['POST'])
def process_query():
    """Processar consulta do usuário"""
    try:
        logs = []
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "error": "query é obrigatório",
                "logs": ["Query não fornecida"]
            }), 400
        
        user_id = data.get('user_id', 'anonymous')
        query = data['query']
        
        add_log(logs, f"Processando consulta do usuário {user_id}: {query[:50]}...")
        
        result = review_agent.process_user_query(query, user_id)
        add_log(logs, "Consulta processada com sucesso")
        
        return jsonify({
            "success": True,
            "result": result,
            "query": query,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao processar consulta: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/reports/comprehensive', methods=['GET'])
def get_comprehensive_report():
    """Gerar relatório abrangente do sistema"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        days = int(request.args.get('days', 30))
        
        add_log(logs, f"Gerando relatório abrangente{' para ' + package_name if package_name else ''}")
        
        # Status do sistema
        system_status = review_agent.get_system_status()
        add_log(logs, "Status do sistema obtido")
        
        # Se package_name especificado, focar nele
        if package_name:
            dashboard = review_agent.get_app_dashboard(package_name)
            sentiment_summary = review_agent.analyzer.get_sentiment_summary(package_name, days)
            backlog_summary = review_agent.backlog_generator.get_backlog_summary(package_name)
            
            add_log(logs, f"Dados específicos do app {package_name} coletados")
            
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
            
            add_log(logs, "Dados gerais do sistema coletados")
            
            report = {
                "type": "system_wide",
                "period_days": days,
                "sentiment_analysis": sentiment_summary,
                "backlog_analysis": backlog_summary,
                "system_status": system_status
            }
        
        add_log(logs, "Relatório abrangente gerado com sucesso")
        
        return jsonify({
            "success": True,
            "report": report,
            "logs": logs,
            "generated_at": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao gerar relatório: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/memory/patterns', methods=['GET'])
def get_memory_patterns():
    """Obter padrões aprendidos pela memória de longo prazo"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        pattern_type = request.args.get('pattern_type')
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório",
                "logs": ["package_name não fornecido"]
            }), 400
        
        add_log(logs, f"Obtendo padrões de memória para {package_name}")
        
        patterns = review_agent.memory.get_sentiment_patterns(package_name, pattern_type)
        add_log(logs, "Padrões de memória obtidos com sucesso")
        
        return jsonify({
            "success": True,
            "patterns": patterns,
            "package_name": package_name,
            "pattern_type": pattern_type,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter padrões: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route('/optimization/suggestions', methods=['GET'])
def get_optimization_suggestions():
    """Obter sugestões de otimização baseadas na memória"""
    try:
        logs = []
        package_name = request.args.get('package_name')
        
        if not package_name:
            return jsonify({
                "success": False,
                "error": "package_name é obrigatório",
                "logs": ["package_name não fornecido"]
            }), 400
        
        add_log(logs, f"Obtendo sugestões de otimização para {package_name}")
        
        # Obter backlog atual para análise
        backlog_summary = review_agent.backlog_generator.get_backlog_summary(package_name)
        current_backlog = backlog_summary.get('high_priority_items', [])
        
        suggestions = review_agent.memory.get_backlog_optimization_suggestions(current_backlog)
        add_log(logs, "Sugestões de otimização obtidas com sucesso")
        
        return jsonify({
            "success": True,
            "suggestions": suggestions,
            "package_name": package_name,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"Erro ao obter sugestões: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@review_agent_bp.route("/send-report-email", methods=["POST"])
def send_report_email():
    """Envia um e-mail de relatório executivo."""
    try:
        logs = []
        data = request.get_json()
        
        if not data or "recipient_email" not in data or "report_data" not in data:
            return jsonify({
                "success": False,
                "error": "recipient_email e report_data são obrigatórios",
                "logs": ["Dados obrigatórios não fornecidos"]
            }), 400

        recipient_email = data["recipient_email"]
        report_data = data["report_data"]
        
        add_log(logs, f"Enviando e-mail de relatório para {recipient_email}")
        
        # Usar configurações dinâmicas do header se disponíveis
        email_service = EmailSenderService.from_request_headers()
        
        result = email_service.send_executive_report_email(recipient_email, report_data)
        add_log(logs, "E-mail enviado com sucesso")
        
        return jsonify({
            "success": True, 
            "result": result,
            "logs": logs,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e),
            "logs": [f"Erro ao enviar e-mail: {str(e)}"],
            "timestamp": datetime.utcnow().isoformat()
        }), 500

# Tratamento de erros
@review_agent_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint não encontrado",
        "logs": ["Endpoint não encontrado"],
        "timestamp": datetime.utcnow().isoformat()
    }), 404

@review_agent_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Método não permitido",
        "logs": ["Método HTTP não permitido"],
        "timestamp": datetime.utcnow().isoformat()
    }), 405

@review_agent_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Erro interno do servidor",
        "logs": ["Erro interno do servidor"],
        "timestamp": datetime.utcnow().isoformat()
    }), 500

