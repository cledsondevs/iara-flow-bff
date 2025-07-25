"""
Serviço para geração de dashboards personalizados baseados no backlog
"""
import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3

class DashboardService:
    def __init__(self):
        self.database_path = os.getenv("DB_PATH", "./data/iara_flow.db")
        self._init_tables()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados SQLite"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """Inicializar tabelas necessárias para dashboards"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Tabela para dashboards personalizados
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS custom_dashboards (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        session_id TEXT,
                        backlog_id TEXT,
                        package_name TEXT,
                        dashboard_config TEXT NOT NULL,
                        custom_url TEXT UNIQUE NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        access_count INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        metadata TEXT
                    )
                """)
                
                # Tabela para componentes do dashboard
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS dashboard_components (
                        id TEXT PRIMARY KEY,
                        dashboard_id TEXT NOT NULL,
                        component_type TEXT NOT NULL,
                        component_config TEXT NOT NULL,
                        position_x INTEGER DEFAULT 0,
                        position_y INTEGER DEFAULT 0,
                        width INTEGER DEFAULT 4,
                        height INTEGER DEFAULT 3,
                        order_index INTEGER DEFAULT 0,
                        is_visible BOOLEAN DEFAULT 1,
                        FOREIGN KEY (dashboard_id) REFERENCES custom_dashboards (id)
                    )
                """)
                
                # Índices para performance
                cur.execute("CREATE INDEX IF NOT EXISTS idx_custom_url ON custom_dashboards(custom_url)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_package_name ON custom_dashboards(package_name)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_dashboard_components ON dashboard_components(dashboard_id)")
                
                conn.commit()
                
        except Exception as e:
            print(f"Erro ao inicializar tabelas de dashboard: {e}")
    
    def generate_custom_url(self, package_name: str, backlog_data: Dict[str, Any]) -> str:
        """Gerar URL personalizada única para o dashboard"""
        try:
            # Criar hash baseado nos dados do backlog
            backlog_hash = hashlib.md5(json.dumps(backlog_data, sort_keys=True).encode()).hexdigest()[:8]
            
            # Timestamp para unicidade
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            
            # Random component
            random_component = str(uuid.uuid4())[:8]
            
            # Slug limpo do package name
            clean_package = package_name.replace('.', '-').replace('_', '-').lower()
            
            custom_url = f"dashboard-{clean_package}-{timestamp}-{backlog_hash}-{random_component}"
            
            # Verificar unicidade
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM custom_dashboards WHERE custom_url = ?", (custom_url,))
                if cur.fetchone():
                    # Se já existe, adicionar timestamp mais específico
                    custom_url += f"-{datetime.now().microsecond}"
            
            return custom_url
            
        except Exception as e:
            # Fallback para URL simples
            return f"dashboard-{str(uuid.uuid4())}"
    
    def analyze_backlog_for_dashboard(self, backlog_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisar dados do backlog para gerar configuração do dashboard"""
        try:
            analysis = {
                "total_items": 0,
                "priority_distribution": {},
                "category_distribution": {},
                "sentiment_metrics": {},
                "top_issues": [],
                "trends": {}
            }
            
            # Extrair dados do backlog
            backlog_items = backlog_data.get('summary', {}).get('high_priority_items', [])
            category_summary = backlog_data.get('summary', {}).get('category_summary', {})
            
            analysis["total_items"] = backlog_data.get('generated_items', 0)
            
            # Distribuição por categoria
            for category, data in category_summary.items():
                analysis["category_distribution"][category] = {
                    "count": data.get('count', 0),
                    "avg_priority": data.get('avg_priority', 0)
                }
            
            # Distribuição por prioridade
            priority_counts = {}
            for item in backlog_items:
                priority = item.get('priority', 3)
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            analysis["priority_distribution"] = priority_counts
            
            # Top issues (primeiros 10)
            analysis["top_issues"] = backlog_items[:10]
            
            # Métricas de sentimento (mock - seria extraído dos dados reais)
            analysis["sentiment_metrics"] = {
                "positive_ratio": 0.3,
                "negative_ratio": 0.5,
                "neutral_ratio": 0.2,
                "overall_score": -0.2
            }
            
            return analysis
            
        except Exception as e:
            print(f"Erro ao analisar backlog: {e}")
            return {}
    
    def generate_dashboard_config(self, analysis: Dict[str, Any], 
                                package_name: str) -> Dict[str, Any]:
        """Gerar configuração do dashboard baseada na análise"""
        try:
            config = {
                "title": f"Relatório Gerencial - {package_name}",
                "description": f"Dashboard gerado automaticamente para análise do backlog",
                "layout": {
                    "grid_columns": 12,
                    "components": []
                },
                "theme": {
                    "primary_color": "#3B82F6",
                    "secondary_color": "#10B981",
                    "background": "#F8FAFC",
                    "text_color": "#1F2937"
                },
                "filters": {
                    "date_range": True,
                    "category": True,
                    "priority": True
                },
                "refresh_interval": 300  # 5 minutos
            }
            
            components = []
            
            # 1. Métricas principais (cards)
            components.append({
                "id": "total_items_card",
                "type": "metric_card",
                "title": "Total de Itens",
                "value": analysis.get("total_items", 0),
                "icon": "list",
                "color": "blue",
                "position": {"x": 0, "y": 0, "w": 3, "h": 2}
            })
            
            components.append({
                "id": "high_priority_card",
                "type": "metric_card",
                "title": "Alta Prioridade",
                "value": len([p for p in analysis.get("priority_distribution", {}) if int(p) >= 4]),
                "icon": "alert-triangle",
                "color": "red",
                "position": {"x": 3, "y": 0, "w": 3, "h": 2}
            })
            
            components.append({
                "id": "sentiment_card",
                "type": "metric_card",
                "title": "Score Sentimento",
                "value": f"{analysis.get('sentiment_metrics', {}).get('overall_score', 0):.2f}",
                "icon": "trending-down" if analysis.get('sentiment_metrics', {}).get('overall_score', 0) < 0 else "trending-up",
                "color": "red" if analysis.get('sentiment_metrics', {}).get('overall_score', 0) < 0 else "green",
                "position": {"x": 6, "y": 0, "w": 3, "h": 2}
            })
            
            components.append({
                "id": "categories_card",
                "type": "metric_card",
                "title": "Categorias",
                "value": len(analysis.get("category_distribution", {})),
                "icon": "tag",
                "color": "purple",
                "position": {"x": 9, "y": 0, "w": 3, "h": 2}
            })
            
            # 2. Gráfico de prioridades
            if analysis.get("priority_distribution"):
                components.append({
                    "id": "priority_chart",
                    "type": "bar_chart",
                    "title": "Distribuição por Prioridade",
                    "data": {
                        "labels": [f"Prioridade {p}" for p in sorted(analysis["priority_distribution"].keys())],
                        "datasets": [{
                            "label": "Quantidade",
                            "data": [analysis["priority_distribution"][p] for p in sorted(analysis["priority_distribution"].keys())],
                            "backgroundColor": ["#EF4444", "#F97316", "#EAB308", "#22C55E", "#3B82F6"]
                        }]
                    },
                    "position": {"x": 0, "y": 2, "w": 6, "h": 4}
                })
            
            # 3. Gráfico de categorias
            if analysis.get("category_distribution"):
                components.append({
                    "id": "category_chart",
                    "type": "pie_chart",
                    "title": "Distribuição por Categoria",
                    "data": {
                        "labels": list(analysis["category_distribution"].keys()),
                        "datasets": [{
                            "data": [data["count"] for data in analysis["category_distribution"].values()],
                            "backgroundColor": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
                        }]
                    },
                    "position": {"x": 6, "y": 2, "w": 6, "h": 4}
                })
            
            # 4. Tabela de top issues
            if analysis.get("top_issues"):
                components.append({
                    "id": "top_issues_table",
                    "type": "data_table",
                    "title": "Principais Issues",
                    "data": {
                        "columns": ["Título", "Prioridade", "Categoria", "Frequência"],
                        "rows": [
                            [
                                item.get("title", "")[:50] + "..." if len(item.get("title", "")) > 50 else item.get("title", ""),
                                item.get("priority", 0),
                                item.get("category", ""),
                                item.get("frequency", 0)
                            ] for item in analysis["top_issues"][:10]
                        ]
                    },
                    "position": {"x": 0, "y": 6, "w": 12, "h": 4}
                })
            
            # 5. Gauge de sentimento
            sentiment_metrics = analysis.get("sentiment_metrics", {})
            if sentiment_metrics:
                components.append({
                    "id": "sentiment_gauge",
                    "type": "gauge_chart",
                    "title": "Análise de Sentimento",
                    "data": {
                        "value": abs(sentiment_metrics.get("overall_score", 0)) * 100,
                        "max": 100,
                        "ranges": [
                            {"from": 0, "to": 30, "color": "#22C55E"},
                            {"from": 30, "to": 70, "color": "#EAB308"},
                            {"from": 70, "to": 100, "color": "#EF4444"}
                        ]
                    },
                    "position": {"x": 0, "y": 10, "w": 6, "h": 3}
                })
            
            config["layout"]["components"] = components
            
            return config
            
        except Exception as e:
            print(f"Erro ao gerar configuração do dashboard: {e}")
            return {}
    
    def create_dashboard(self, package_name: str, backlog_data: Dict[str, Any],
                        user_id: str = None, session_id: str = None,
                        expires_hours: int = 168) -> Dict[str, Any]:  # 7 dias por padrão
        """Criar dashboard personalizado"""
        try:
            # Analisar dados do backlog
            analysis = self.analyze_backlog_for_dashboard(backlog_data)
            
            # Gerar configuração do dashboard
            dashboard_config = self.generate_dashboard_config(analysis, package_name)
            
            # Gerar URL personalizada
            custom_url = self.generate_custom_url(package_name, backlog_data)
            
            # Data de expiração
            expires_at = datetime.now() + timedelta(hours=expires_hours)
            
            # Salvar no banco
            dashboard_id = str(uuid.uuid4())
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                cur.execute("""
                    INSERT INTO custom_dashboards 
                    (id, user_id, session_id, package_name, dashboard_config, 
                     custom_url, title, description, expires_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dashboard_id,
                    user_id,
                    session_id,
                    package_name,
                    json.dumps(dashboard_config),
                    custom_url,
                    dashboard_config.get("title", "Dashboard"),
                    dashboard_config.get("description", ""),
                    expires_at.isoformat(),
                    json.dumps({
                        "backlog_summary": backlog_data.get('summary', {}),
                        "generation_timestamp": datetime.now().isoformat(),
                        "analysis": analysis
                    })
                ))
                
                # Salvar componentes
                for component in dashboard_config.get("layout", {}).get("components", []):
                    cur.execute("""
                        INSERT INTO dashboard_components 
                        (dashboard_id, component_type, component_config, 
                         position_x, position_y, width, height)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        dashboard_id,
                        component.get("type", "unknown"),
                        json.dumps(component),
                        component.get("position", {}).get("x", 0),
                        component.get("position", {}).get("y", 0),
                        component.get("position", {}).get("w", 4),
                        component.get("position", {}).get("h", 3)
                    ))
                
                conn.commit()
            
            return {
                "dashboard_id": dashboard_id,
                "custom_url": custom_url,
                "full_url": f"/dashboard/{custom_url}",
                "title": dashboard_config.get("title"),
                "expires_at": expires_at.isoformat(),
                "components_count": len(dashboard_config.get("layout", {}).get("components", [])),
                "config": dashboard_config
            }
            
        except Exception as e:
            raise Exception(f"Erro ao criar dashboard: {str(e)}")
    
    def get_dashboard_by_url(self, custom_url: str) -> Optional[Dict[str, Any]]:
        """Obter dashboard pela URL personalizada"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Buscar dashboard
                cur.execute("""
                    SELECT * FROM custom_dashboards 
                    WHERE custom_url = ? AND is_active = 1
                """, (custom_url,))
                
                dashboard_row = cur.fetchone()
                if not dashboard_row:
                    return None
                
                # Verificar se não expirou
                expires_at = datetime.fromisoformat(dashboard_row['expires_at']) if dashboard_row['expires_at'] else None
                if expires_at and expires_at < datetime.now():
                    return None
                
                # Incrementar contador de acesso
                cur.execute("""
                    UPDATE custom_dashboards 
                    SET access_count = access_count + 1 
                    WHERE id = ?
                """, (dashboard_row['id'],))
                
                # Buscar componentes
                cur.execute("""
                    SELECT * FROM dashboard_components 
                    WHERE dashboard_id = ? AND is_visible = 1
                    ORDER BY order_index, position_y, position_x
                """, (dashboard_row['id'],))
                
                components = [dict(row) for row in cur.fetchall()]
                
                conn.commit()
                
                # Montar resposta
                dashboard_config = json.loads(dashboard_row['dashboard_config'])
                
                return {
                    "id": dashboard_row['id'],
                    "title": dashboard_row['title'],
                    "description": dashboard_row['description'],
                    "package_name": dashboard_row['package_name'],
                    "custom_url": dashboard_row['custom_url'],
                    "created_at": dashboard_row['created_at'],
                    "expires_at": dashboard_row['expires_at'],
                    "access_count": dashboard_row['access_count'] + 1,
                    "config": dashboard_config,
                    "components": components,
                    "metadata": json.loads(dashboard_row['metadata']) if dashboard_row['metadata'] else {}
                }
                
        except Exception as e:
            print(f"Erro ao buscar dashboard: {e}")
            return None
    
    def list_dashboards(self, package_name: str = None, user_id: str = None,
                       limit: int = 50) -> List[Dict[str, Any]]:
        """Listar dashboards criados"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                where_conditions = ["is_active = 1"]
                params = []
                
                if package_name:
                    where_conditions.append("package_name = ?")
                    params.append(package_name)
                
                if user_id:
                    where_conditions.append("user_id = ?")
                    params.append(user_id)
                
                where_clause = " AND ".join(where_conditions)
                params.append(limit)
                
                cur.execute(f"""
                    SELECT id, title, description, package_name, custom_url, 
                           created_at, expires_at, access_count
                    FROM custom_dashboards 
                    WHERE {where_clause}
                    ORDER BY created_at DESC
                    LIMIT ?
                """, params)
                
                dashboards = []
                for row in cur.fetchall():
                    dashboard = dict(row)
                    
                    # Verificar se não expirou
                    expires_at = datetime.fromisoformat(row['expires_at']) if row['expires_at'] else None
                    dashboard['is_expired'] = expires_at and expires_at < datetime.now()
                    
                    dashboards.append(dashboard)
                
                return dashboards
                
        except Exception as e:
            print(f"Erro ao listar dashboards: {e}")
            return []
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Deletar dashboard (soft delete)"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                cur.execute("""
                    UPDATE custom_dashboards 
                    SET is_active = 0 
                    WHERE id = ?
                """, (dashboard_id,))
                
                conn.commit()
                return cur.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao deletar dashboard: {e}")
            return False
    
    def cleanup_expired_dashboards(self) -> int:
        """Limpar dashboards expirados"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                cur.execute("""
                    UPDATE custom_dashboards 
                    SET is_active = 0 
                    WHERE expires_at < datetime('now') AND is_active = 1
                """)
                
                conn.commit()
                return cur.rowcount
                
        except Exception as e:
            print(f"Erro ao limpar dashboards expirados: {e}")
            return 0

