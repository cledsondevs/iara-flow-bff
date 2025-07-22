"""
Rotas da API para dashboards personalizados
"""
from flask import Blueprint, request, jsonify
from app.services.dashboard_service import DashboardService
from app.services.backlog_generator_service import BacklogGeneratorService
import json

dashboard_bp = Blueprint('dashboard', __name__)
dashboard_service = DashboardService()
backlog_service = BacklogGeneratorService()

@dashboard_bp.route('/generate', methods=['POST'])
def generate_dashboard():
    """Gerar dashboard personalizado baseado no backlog"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        package_name = data.get('package_name')
        if not package_name:
            return jsonify({
                "error": "package_name é obrigatório",
                "success": False
            }), 400
        
        # Parâmetros opcionais
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        days = data.get('days', 7)
        expires_hours = data.get('expires_hours', 168)  # 7 dias
        
        # Gerar ou usar backlog existente
        backlog_data = data.get('backlog_data')
        if not backlog_data:
            # Gerar novo backlog
            backlog_data = backlog_service.process_reviews_to_backlog(package_name, days)
        
        # Criar dashboard
        dashboard_result = dashboard_service.create_dashboard(
            package_name=package_name,
            backlog_data=backlog_data,
            user_id=user_id,
            session_id=session_id,
            expires_hours=expires_hours
        )
        
        return jsonify({
            "success": True,
            "dashboard": dashboard_result,
            "message": "Dashboard criado com sucesso"
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/<custom_url>', methods=['GET'])
def view_dashboard(custom_url):
    """Visualizar dashboard pela URL personalizada"""
    try:
        dashboard = dashboard_service.get_dashboard_by_url(custom_url)
        
        if not dashboard:
            return jsonify({
                "error": "Dashboard não encontrado ou expirado",
                "success": False
            }), 404
        
        return jsonify({
            "success": True,
            "dashboard": dashboard
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/list', methods=['GET'])
def list_dashboards():
    """Listar dashboards criados"""
    try:
        # Parâmetros de filtro
        package_name = request.args.get('package_name')
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 50))
        
        dashboards = dashboard_service.list_dashboards(
            package_name=package_name,
            user_id=user_id,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "dashboards": dashboards,
            "count": len(dashboards)
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/<dashboard_id>', methods=['DELETE'])
def delete_dashboard(dashboard_id):
    """Deletar dashboard"""
    try:
        success = dashboard_service.delete_dashboard(dashboard_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Dashboard deletado com sucesso"
            }), 200
        else:
            return jsonify({
                "error": "Dashboard não encontrado",
                "success": False
            }), 404
            
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/cleanup', methods=['POST'])
def cleanup_expired():
    """Limpar dashboards expirados"""
    try:
        cleaned_count = dashboard_service.cleanup_expired_dashboards()
        
        return jsonify({
            "success": True,
            "cleaned_count": cleaned_count,
            "message": f"{cleaned_count} dashboards expirados foram removidos"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/preview', methods=['POST'])
def preview_dashboard():
    """Gerar preview do dashboard sem salvar"""
    try:
        data = request.get_json()
        
        package_name = data.get('package_name')
        if not package_name:
            return jsonify({
                "error": "package_name é obrigatório",
                "success": False
            }), 400
        
        days = data.get('days', 7)
        
        # Gerar backlog para preview
        backlog_data = backlog_service.process_reviews_to_backlog(package_name, days)
        
        # Analisar dados
        analysis = dashboard_service.analyze_backlog_for_dashboard(backlog_data)
        
        # Gerar configuração
        dashboard_config = dashboard_service.generate_dashboard_config(analysis, package_name)
        
        return jsonify({
            "success": True,
            "preview": {
                "config": dashboard_config,
                "analysis": analysis,
                "backlog_summary": backlog_data.get('summary', {})
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@dashboard_bp.route('/stats', methods=['GET'])
def dashboard_stats():
    """Estatísticas gerais dos dashboards"""
    try:
        with dashboard_service._get_connection() as conn:
            cur = conn.cursor()
            
            # Total de dashboards
            cur.execute("SELECT COUNT(*) as total FROM custom_dashboards WHERE is_active = 1")
            total_dashboards = cur.fetchone()['total']
            
            # Dashboards por package
            cur.execute("""
                SELECT package_name, COUNT(*) as count 
                FROM custom_dashboards 
                WHERE is_active = 1 
                GROUP BY package_name 
                ORDER BY count DESC 
                LIMIT 10
            """)
            by_package = [dict(row) for row in cur.fetchall()]
            
            # Dashboards mais acessados
            cur.execute("""
                SELECT title, custom_url, access_count, package_name
                FROM custom_dashboards 
                WHERE is_active = 1 
                ORDER BY access_count DESC 
                LIMIT 10
            """)
            most_accessed = [dict(row) for row in cur.fetchall()]
            
            # Dashboards criados por dia (últimos 7 dias)
            cur.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM custom_dashboards 
                WHERE is_active = 1 
                AND created_at >= datetime('now', '-7 days')
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            """)
            daily_creation = [dict(row) for row in cur.fetchall()]
            
            return jsonify({
                "success": True,
                "stats": {
                    "total_dashboards": total_dashboards,
                    "by_package": by_package,
                    "most_accessed": most_accessed,
                    "daily_creation": daily_creation
                }
            }), 200
            
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

