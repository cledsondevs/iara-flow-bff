"""
Serviço principal do agente autônomo de análise de reviews
Integra todos os componentes: coleta, análise, geração de backlog e memória
"""
import os
import json
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from app.services.review_collector_service import ReviewCollectorService
from app.services.sentiment_analysis_service import SentimentAnalysisService
from app.services.backlog_generator_service import BacklogGeneratorService
from app.services.isolated_memory_service import IsolatedMemoryService
from app.models.review_models import StoreType

class ReviewAgentService:
    def __init__(self):
        self.collector = ReviewCollectorService()
        self.analyzer = SentimentAnalysisService()
        self.backlog_generator = BacklogGeneratorService()
        self.memory = IsolatedMemoryService()
        
        self.is_running = False
        self.scheduler_thread = None
        
        self._setup_scheduler()
    
    def _setup_scheduler(self):
        """Configurar agendamento automático"""
        # Agendar coleta de reviews a cada 6 horas
        schedule.every(6).hours.do(self._scheduled_collection)
        
        # Agendar análise de sentimento a cada 2 horas
        schedule.every(2).hours.do(self._scheduled_analysis)
        
        # Agendar geração de backlog diariamente
        schedule.every().day.at("09:00").do(self._scheduled_backlog_generation)
        
        # Agendar atualização de padrões de memória diariamente
        schedule.every().day.at("23:00").do(self._scheduled_memory_update)
    
    def start_autonomous_mode(self):
        """Iniciar modo autônomo com agendamento"""
        if self.is_running:
            return {"status": "already_running"}
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        return {
            "status": "started",
            "message": "Agente autônomo iniciado com sucesso",
            "scheduled_tasks": [
                "Coleta de reviews: a cada 6 horas",
                "Análise de sentimento: a cada 2 horas", 
                "Geração de backlog: diariamente às 09:00",
                "Atualização de memória: diariamente às 23:00"
            ]
        }
    
    def stop_autonomous_mode(self):
        """Parar modo autônomo"""
        self.is_running = False
        schedule.clear()
        
        return {
            "status": "stopped",
            "message": "Agente autônomo parado com sucesso"
        }
    
    def _run_scheduler(self):
        """Executar agendador em thread separada"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto
    
    def _scheduled_collection(self):
        """Coleta agendada de reviews"""
        try:
            result = self.collector.collect_all_pending()
            print(f"Coleta automática concluída: {result['total_reviews']} reviews coletados")
            
            # Registrar na memória de longo prazo
            self.memory.save_to_long_term_memory(
                user_id="system",
                content=f"Coleta automática: {result['total_reviews']} reviews de {result['total_apps']} apps",
                memory_type="system_activity",
                importance_score=0.3,
                metadata=result
            )
            
        except Exception as e:
            print(f"Erro na coleta agendada: {e}")
    
    def _scheduled_analysis(self):
        """Análise agendada de sentimento"""
        try:
            result = self.analyzer.analyze_pending_reviews()
            print(f"Análise automática concluída: {result['analyzed']} reviews analisados")
            
            # Registrar na memória
            self.memory.save_to_long_term_memory(
                user_id="system",
                content=f"Análise automática: {result['analyzed']} reviews analisados",
                memory_type="system_activity",
                importance_score=0.3,
                metadata=result
            )
            
        except Exception as e:
            print(f"Erro na análise agendada: {e}")
    
    def _scheduled_backlog_generation(self):
        """Geração agendada de backlog"""
        try:
            # Obter todos os apps configurados
            apps = self.collector.get_apps_for_collection()
            
            total_generated = 0
            for app in apps:
                result = self.backlog_generator.process_reviews_to_backlog(
                    package_name=app.package_name,
                    days=7
                )
                total_generated += result['generated_items']
            
            print(f"Geração automática de backlog: {total_generated} itens gerados")
            
            # Registrar na memória
            self.memory.save_to_long_term_memory(
                user_id="system",
                content=f"Geração automática de backlog: {total_generated} itens para {len(apps)} apps",
                memory_type="system_activity",
                importance_score=0.5,
                metadata={"total_items": total_generated, "apps_count": len(apps)}
            )
            
        except Exception as e:
            print(f"Erro na geração agendada de backlog: {e}")
    
    def _scheduled_memory_update(self):
        """Atualização agendada de padrões de memória"""
        try:
            # Atualizar padrões de sentimento para todos os apps
            apps = self.collector.get_apps_for_collection()
            
            for app in apps:
                self.analyzer.update_sentiment_patterns(app.package_name)
                
                # Registrar evolução do sentimento
                summary = self.analyzer.get_sentiment_summary(app.package_name, days=1)
                for topic_data in summary.get('top_topics', []):
                    topic = topic_data['topic']
                    sentiment_dist = summary['sentiment_distribution']
                    
                    self.memory.record_sentiment_evolution(
                        package_name=app.package_name,
                        topic=topic,
                        sentiment_distribution=sentiment_dist
                    )
            
            print(f"Atualização de memória concluída para {len(apps)} apps")
            
        except Exception as e:
            print(f"Erro na atualização de memória: {e}")
    
    def add_app_for_monitoring(self, package_name: str, app_name: str,
                             stores: List[str] = None,
                             collection_frequency: int = 6) -> Dict[str, Any]:
        """Adicionar aplicativo para monitoramento"""
        try:
            if stores is None:
                stores = ["google_play"]
            
            store_types = [StoreType(store) for store in stores]
            
            app_id = self.collector.add_app_config(
                package_name=package_name,
                app_name=app_name,
                stores=store_types,
                collection_frequency=collection_frequency
            )
            
            # Fazer coleta inicial
            initial_result = self.collect_reviews_for_app(package_name)
            
            return {
                "app_id": app_id,
                "package_name": package_name,
                "app_name": app_name,
                "stores": stores,
                "collection_frequency": collection_frequency,
                "initial_collection": initial_result,
                "status": "added_successfully"
            }
            
        except Exception as e:
            raise Exception(f"Erro ao adicionar app para monitoramento: {str(e)}")
    
    def collect_reviews_for_app(self, package_name: str) -> Dict[str, Any]:
        """Coletar reviews para um aplicativo específico"""
        try:
            # Obter configuração do app
            target_app = self.collector.get_app_config_by_package_name(package_name)
            
            if not target_app:
                raise Exception(f"App {package_name} não encontrado nas configurações")
            
            total_reviews = 0
            results = []
            
            for store in target_app.stores:
                reviews = self.collector.collect_reviews(package_name, store)
                saved_count = self.collector.save_reviews(reviews)
                total_reviews += saved_count
                
                results.append({
                    "store": store.value,
                    "collected": len(reviews),
                    "saved": saved_count
                })
            
            # Atualizar timestamp de coleta
            self.collector.update_last_collection(package_name)
            
            return {
                "package_name": package_name,
                "total_reviews_collected": total_reviews,
                "store_results": results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao coletar reviews: {str(e)}")
    
    def analyze_app_sentiment(self, package_name: str) -> Dict[str, Any]:
        """Analisar sentimento para um aplicativo específico"""
        try:
            # Analisar reviews pendentes
            analysis_result = self.analyzer.analyze_pending_reviews()
            
            # Obter resumo de sentimento
            sentiment_summary = self.analyzer.get_sentiment_summary(package_name)
            
            # Atualizar padrões de sentimento
            self.analyzer.update_sentiment_patterns(package_name)
            
            return {
                "package_name": package_name,
                "analysis_result": analysis_result,
                "sentiment_summary": sentiment_summary,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao analisar sentimento: {str(e)}")
    
    def generate_backlog_for_app(self, package_name: str, 
                               days: int = 7) -> Dict[str, Any]:
        """Gerar backlog para um aplicativo específico"""
        try:
            # Obter contexto da memória de longo prazo
            context = {
                "package_name": package_name,
                "patterns": self.backlog_generator.analyze_review_patterns(package_name, days),
                "current_backlog": []  # Poderia buscar backlog atual aqui
            }
            
            # Otimizar geração com base na memória
            optimization = self.memory.optimize_backlog_generation(context)
            
            # Gerar backlog
            result = self.backlog_generator.process_reviews_to_backlog(package_name, days)
            
            # Aprender padrões para futuras otimizações
            if result['generated_items'] > 0:
                self._learn_from_backlog_generation(package_name, result, optimization)
            
            return {
                "package_name": package_name,
                "generation_result": result,
                "optimization_applied": optimization,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao gerar backlog: {str(e)}")
    
    def _learn_from_backlog_generation(self, package_name: str,
                                     generation_result: Dict[str, Any],
                                     optimization: Dict[str, Any]):
        """Aprender com o processo de geração de backlog"""
        try:
            # Registrar padrões de sentimento identificados
            patterns = generation_result.get('summary', {})
            
            for category, data in patterns.get('category_summary', {}).items():
                self.memory.learn_sentiment_pattern(
                    package_name=package_name,
                    pattern_type="backlog_category",
                    pattern_data={
                        "key": f"{package_name}_{category}",
                        "category": category,
                        "frequency": data.get('count', 0),
                        "avg_priority": data.get('avg_priority', 0)
                    },
                    confidence=0.7
                )
            
            # Se houve otimizações aplicadas, registrar como padrão de sucesso
            if optimization.get('optimization_patterns'):
                for pattern in optimization['optimization_patterns']:
                    self.memory.learn_backlog_optimization_pattern(
                        pattern_name=f"auto_{pattern['pattern_name']}",
                        description=f"Padrão aplicado automaticamente para {package_name}",
                        success_indicators=["items_generated"],
                        failure_indicators=["no_items_generated"],
                        optimization_rules=pattern.get('optimization_rules', {})
                    )
            
        except Exception as e:
            print(f"Erro ao aprender com geração de backlog: {e}")
    
    def get_app_dashboard(self, package_name: str) -> Dict[str, Any]:
        """Obter dashboard completo de um aplicativo"""
        try:
            # Resumo de sentimento
            sentiment_summary = self.analyzer.get_sentiment_summary(package_name, days=30)
            
            # Resumo do backlog
            backlog_summary = self.backlog_generator.get_backlog_summary(package_name)
            
            # Tendências de sentimento
            sentiment_trends = self.memory.get_sentiment_trends(package_name, days=30)
            
            # Padrões aprendidos
            learned_patterns = self.memory.get_sentiment_patterns(package_name)
            
            return {
                "package_name": package_name,
                "sentiment_summary": sentiment_summary,
                "backlog_summary": backlog_summary,
                "sentiment_trends": sentiment_trends,
                "learned_patterns": len(learned_patterns),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao obter dashboard: {str(e)}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obter status geral do sistema"""
        try:
            # Apps monitorados
            apps = self.collector.get_apps_for_collection()
            
            # Estatísticas gerais
            with self.collector._get_connection() as conn:
                with conn.cursor() as cur:
                    # Total de reviews
                    cur.execute("SELECT COUNT(*) as total FROM reviews")
                    total_reviews = cur.fetchone()['total']
                    
                    # Reviews analisados
                    cur.execute("SELECT COUNT(*) as analyzed FROM reviews WHERE sentiment IS NOT NULL")
                    analyzed_reviews = cur.fetchone()['analyzed']
                    
                    # Itens de backlog
                    cur.execute("SELECT COUNT(*) as total FROM backlog_items")
                    total_backlog = cur.fetchone()['total']
                    
                    # Itens pendentes
                    cur.execute("SELECT COUNT(*) as pending FROM backlog_items WHERE status = 'pending'")
                    pending_backlog = cur.fetchone()['pending']
            
            return {
                "autonomous_mode": self.is_running,
                "monitored_apps": len(apps),
                "total_reviews": total_reviews,
                "analyzed_reviews": analyzed_reviews,
                "analysis_coverage": (analyzed_reviews / total_reviews * 100) if total_reviews > 0 else 0,
                "total_backlog_items": total_backlog,
                "pending_backlog_items": pending_backlog,
                "apps": [{"package_name": app.package_name, "app_name": app.app_name} for app in apps],
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao obter status do sistema: {str(e)}")
    
    def process_user_query(self, query: str, user_id: str) -> Dict[str, Any]:
        """Processar consulta do usuário usando memória de longo prazo"""
        try:
            # Buscar informações relevantes na memória
            relevant_memories = self.memory.get_relevant_long_term_memories(user_id, query)
            
            # Analisar a consulta para determinar ação
            if "status" in query.lower() or "resumo" in query.lower():
                return self.get_system_status()
            
            elif "dashboard" in query.lower():
                # Tentar extrair nome do app da consulta
                apps = self.collector.get_apps_for_collection()
                for app in apps:
                    if app.package_name.lower() in query.lower() or app.app_name.lower() in query.lower():
                        return self.get_app_dashboard(app.package_name)
                
                # Se não encontrou app específico, retornar status geral
                return self.get_system_status()
            
            elif "coletar" in query.lower() or "reviews" in query.lower():
                # Tentar extrair nome do app
                apps = self.collector.get_apps_for_collection()
                for app in apps:
                    if app.package_name.lower() in query.lower() or app.app_name.lower() in query.lower():
                        return self.collect_reviews_for_app(app.package_name)
                
                # Se não especificou app, coletar todos
                return self.collector.collect_all_pending()
            
            elif "backlog" in query.lower():
                # Tentar extrair nome do app
                apps = self.collector.get_apps_for_collection()
                for app in apps:
                    if app.package_name.lower() in query.lower() or app.app_name.lower() in query.lower():
                        return self.generate_backlog_for_app(app.package_name)
                
                # Gerar para todos os apps
                results = []
                for app in apps:
                    result = self.generate_backlog_for_app(app.package_name)
                    results.append(result)
                
                return {"results": results}
            
            else:
                # Resposta genérica com informações relevantes da memória
                return {
                    "message": "Consulta processada",
                    "relevant_memories": relevant_memories,
                    "suggestions": [
                        "Use 'status' para ver o status geral",
                        "Use 'dashboard [app]' para ver dashboard de um app",
                        "Use 'coletar [app]' para coletar reviews",
                        "Use 'backlog [app]' para gerar backlog"
                    ]
                }
            
        except Exception as e:
            raise Exception(f"Erro ao processar consulta: {str(e)}")

