"""
Serviço de memória aprimorado para o agente de análise de reviews
Estende o memory_service.py existente com funcionalidades específicas para reviews
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
import numpy as np

from langchain_openai import OpenAIEmbeddings
from app.services.memory_service import MemoryService

class EnhancedMemoryService(MemoryService):
    def __init__(self):
        super().__init__()
        self._create_enhanced_tables()
    
    def _create_enhanced_tables(self):
        """Criar tabelas adicionais para memória de reviews"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            # Tabela para padrões de sentimento aprendidos
            cur.execute("""
                CREATE TABLE IF NOT EXISTS review_sentiment_patterns (
                    id TEXT PRIMARY KEY,
                    package_name TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence_score REAL DEFAULT 0.0,
                    frequency INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Tabela para correlações problema-solução
            cur.execute("""
                CREATE TABLE IF NOT EXISTS problem_solution_correlations (
                    id TEXT PRIMARY KEY,
                    problem_pattern TEXT NOT NULL,
                    solution_implemented TEXT,
                    backlog_item_id TEXT,
                    sentiment_before TEXT,
                    sentiment_after TEXT,
                    effectiveness_score REAL DEFAULT 0.0,
                    time_to_impact_days INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela para evolução de sentimento ao longo do tempo
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_evolution (
                    id TEXT PRIMARY KEY,
                    package_name TEXT NOT NULL,
                    topic TEXT,
                    time_period TEXT NOT NULL,
                    sentiment_distribution TEXT NOT NULL,
                    key_metrics TEXT,
                    trend_direction TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela para padrões de otimização de backlog
            cur.execute("""
                CREATE TABLE IF NOT EXISTS backlog_optimization_patterns (
                    id TEXT PRIMARY KEY,
                    pattern_name TEXT NOT NULL,
                    pattern_description TEXT,
                    success_indicators TEXT,
                    failure_indicators TEXT,
                    optimization_rules TEXT,
                    confidence_score REAL DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao criar tabelas: {str(e)}")
    
    def learn_sentiment_pattern(self, package_name: str, pattern_type: str,
                              pattern_data: Dict[str, Any], confidence_score: float = 0.5,
                              metadata: Dict[str, Any] = None):
        """Aprender um novo padrão de sentimento"""
        try:
            pattern_id = str(uuid.uuid4())
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Verificar se padrão similar já existe
                cur.execute("""
                    SELECT id, frequency FROM review_sentiment_patterns 
                    WHERE package_name = ? AND pattern_type = ? AND pattern_data = ?
                """, (package_name, pattern_type, json.dumps(pattern_data)))
                
                existing = cur.fetchone()
                
                if existing:
                    # Atualizar padrão existente
                    cur.execute("""
                        UPDATE review_sentiment_patterns 
                        SET frequency = frequency + 1, 
                            confidence_score = ?,
                            last_updated = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (confidence_score, existing[0]))
                else:
                    # Inserir novo padrão
                    cur.execute("""
                        INSERT INTO review_sentiment_patterns 
                        (id, package_name, pattern_type, pattern_data, 
                         confidence_score, metadata)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        pattern_id, package_name, pattern_type,
                        json.dumps(pattern_data), confidence_score,
                        json.dumps(metadata or {})
                    ))
                
                conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao aprender padrão de sentimento: {str(e)}")
    
    def get_sentiment_patterns(self, package_name: str, 
                             pattern_type: str = None) -> List[Dict[str, Any]]:
        """Recuperar padrões de sentimento aprendidos"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                if pattern_type:
                    cur.execute("""
                        SELECT * FROM review_sentiment_patterns 
                        WHERE package_name = ? AND pattern_type = ?
                        ORDER BY confidence_score DESC, frequency DESC
                    """, (package_name, pattern_type))
                else:
                    cur.execute("""
                        SELECT * FROM review_sentiment_patterns 
                        WHERE package_name = ?
                        ORDER BY confidence_score DESC, frequency DESC
                    """, (package_name,))
                
                patterns = []
                for row in cur.fetchall():
                    pattern = {
                        'id': row[0],
                        'package_name': row[1],
                        'pattern_type': row[2],
                        'pattern_data': json.loads(row[3]) if row[3] else {},
                        'confidence_score': row[4],
                        'frequency': row[5],
                        'last_updated': row[6],
                        'metadata': json.loads(row[7]) if row[7] else {}
                    }
                    patterns.append(pattern)
                
                return patterns
                    
        except Exception as e:
            # Retornar lista vazia em caso de erro
            return []
    
    def record_sentiment_evolution(self, package_name: str, topic: str,
                                 sentiment_distribution: Dict[str, Any],
                                 key_metrics: Dict[str, Any] = None):
        """Registrar evolução de sentimento ao longo do tempo"""
        try:
            period_date = datetime.now().strftime('%Y-%m-%d')
            
            # Calcular direção da tendência
            if key_metrics and 'negative_ratio' in key_metrics and 'positive_ratio' in key_metrics:
                current_negative_ratio = key_metrics['negative_ratio']
                current_positive_ratio = key_metrics['positive_ratio']
                trend_direction = self._calculate_trend_direction(
                    package_name, topic, current_negative_ratio, current_positive_ratio
                )
            else:
                trend_direction = 'stable'
                key_metrics = {'total_reviews': 0}
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT OR REPLACE INTO sentiment_evolution 
                    (package_name, topic, time_period, sentiment_distribution, 
                     key_metrics, trend_direction)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    package_name, topic, period_date,
                    json.dumps(sentiment_distribution),
                    json.dumps(key_metrics),
                    trend_direction
                ))
                
                conn.commit()
                    
        except Exception as e:
            print(f"Erro ao registrar evolução de sentimento: {str(e)}")
    
    def _calculate_trend_direction(self, package_name: str, topic: str,
                                 current_negative_ratio: float,
                                 current_positive_ratio: float) -> str:
        """Calcular direção da tendência comparando com período anterior"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT key_metrics FROM sentiment_evolution 
                    WHERE package_name = ? AND topic = ?
                    ORDER BY time_period DESC
                    LIMIT 1
                """, (package_name, topic))
                
                result = cur.fetchone()
                if result:
                    previous_metrics = json.loads(result[0])
                    prev_negative = previous_metrics.get('negative_ratio', 0)
                    prev_positive = previous_metrics.get('positive_ratio', 0)
                    
                    # Comparar tendências
                    if current_negative_ratio < prev_negative and current_positive_ratio > prev_positive:
                        return 'improving'
                    elif current_negative_ratio > prev_negative and current_positive_ratio < prev_positive:
                        return 'declining'
                    else:
                        return 'stable'
                else:
                    return 'stable'
                    
        except Exception:
            return 'stable'
    
    def record_problem_solution_correlation(self, problem_pattern: str,
                                          solution_implemented: str,
                                          backlog_item_id: str = None,
                                          sentiment_before: Dict[str, Any] = None,
                                          sentiment_after: Dict[str, Any] = None,
                                          time_to_impact_days: int = None):
        """Registrar correlação entre problema e solução implementada"""
        try:
            correlation_id = str(uuid.uuid4())
            
            # Calcular score de efetividade
            effectiveness_score = 0.0
            if sentiment_before and sentiment_after:
                before_score = sentiment_before.get('positive', 0) - sentiment_before.get('negative', 0)
                after_score = sentiment_after.get('positive', 0) - sentiment_after.get('negative', 0)
                effectiveness_score = after_score - before_score
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO problem_solution_correlations 
                    (problem_pattern, solution_implemented, backlog_item_id,
                     sentiment_before, sentiment_after, effectiveness_score,
                     time_to_impact_days)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    problem_pattern, solution_implemented, backlog_item_id,
                    json.dumps(sentiment_before or {}),
                    json.dumps(sentiment_after or {}),
                    effectiveness_score, time_to_impact_days
                ))
                
                conn.commit()
                    
        except Exception as e:
            print(f"Erro ao registrar correlação: {str(e)}")
    
    def get_effective_solutions(self, problem_pattern: str) -> List[Dict[str, Any]]:
        """Obter soluções efetivas para um padrão de problema"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT 
                        solution_implemented,
                        effectiveness_score,
                        time_to_impact_days,
                        COUNT(*) as usage_count,
                        AVG(effectiveness_score) as avg_effectiveness
                    FROM problem_solution_correlations 
                    WHERE problem_pattern LIKE ? AND effectiveness_score > 0
                    GROUP BY solution_implemented
                    ORDER BY avg_effectiveness DESC, usage_count DESC
                """, (f"%{problem_pattern}%",))
                
                solutions = []
                for row in cur.fetchall():
                    solution = {
                        'solution': row[0],
                        'effectiveness_score': row[1],
                        'time_to_impact_days': row[2],
                        'usage_count': row[3],
                        'avg_effectiveness': row[4]
                    }
                    solutions.append(solution)
                
                return solutions
                    
        except Exception as e:
            return []
    
    def learn_backlog_optimization_pattern(self, pattern_name: str,
                                         pattern_description: str,
                                         success_indicators: List[str],
                                         failure_indicators: List[str],
                                         optimization_rules: Dict[str, Any]):
        """Aprender padrão de otimização de backlog"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT OR REPLACE INTO backlog_optimization_patterns 
                    (pattern_name, pattern_description, success_indicators,
                     failure_indicators, optimization_rules, confidence_score,
                     usage_count, last_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    pattern_name, pattern_description,
                    json.dumps(success_indicators),
                    json.dumps(failure_indicators),
                    json.dumps(optimization_rules),
                    0.8, 1
                ))
                
                conn.commit()
                    
        except Exception as e:
            print(f"Erro ao aprender padrão de otimização: {str(e)}")
    
    def get_backlog_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Obter sugestões de otimização para o backlog atual"""
        try:
            suggestions = []
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT * FROM backlog_optimization_patterns 
                    ORDER BY confidence_score DESC, usage_count DESC
                """)
                
                for row in cur.fetchall():
                    suggestion = {
                        'pattern_name': row[1],
                        'description': row[2],
                        'success_indicators': json.loads(row[3]) if row[3] else [],
                        'failure_indicators': json.loads(row[4]) if row[4] else [],
                        'optimization_rules': json.loads(row[5]) if row[5] else {},
                        'confidence_score': row[6]
                    }
                    suggestions.append(suggestion)
                
                return suggestions
                    
        except Exception as e:
            return []
    
    def get_sentiment_trends(self, package_name: str, 
                           days: int = 30) -> Dict[str, Any]:
        """Obter tendências de sentimento para um aplicativo"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT 
                        topic,
                        time_period,
                        key_metrics,
                        trend_direction
                    FROM sentiment_evolution 
                    WHERE package_name = ? 
                    AND time_period >= date('now', '-{} days')
                    ORDER BY time_period DESC
                """.format(days), (package_name,))
                
                trends = {}
                for row in cur.fetchall():
                    topic = row[0] or 'general'
                    if topic not in trends:
                        trends[topic] = []
                    
                    trend_data = {
                        'time_period': row[1],
                        'metrics': json.loads(row[2]) if row[2] else {},
                        'direction': row[3]
                    }
                    trends[topic].append(trend_data)
                
                return trends
                    
        except Exception as e:
            return {}
    
    def optimize_backlog_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Otimizar geração de backlog baseado na memória de longo prazo"""
        try:
            package_name = context.get('package_name', '')
            patterns = context.get('patterns', {})
            current_backlog = context.get('current_backlog', [])
            
            # Obter padrões de otimização aprendidos
            optimization_suggestions = self.get_backlog_optimization_suggestions()
            
            # Obter soluções efetivas para problemas similares
            effective_solutions = []
            for pattern in patterns.get('common_issues', []):
                solutions = self.get_effective_solutions(pattern)
                effective_solutions.extend(solutions)
            
            # Obter tendências de sentimento
            sentiment_trends = self.get_sentiment_trends(package_name)
            
            optimization_result = {
                'optimization_suggestions': optimization_suggestions,
                'effective_solutions': effective_solutions,
                'sentiment_trends': sentiment_trends,
                'priority_adjustments': self._calculate_priority_adjustments(
                    patterns, sentiment_trends
                ),
                'recommended_focus_areas': self._identify_focus_areas(
                    patterns, sentiment_trends
                )
            }
            
            return optimization_result
            
        except Exception as e:
            print(f"Erro na otimização de backlog: {str(e)}")
            return {
                'optimization_suggestions': [],
                'effective_solutions': [],
                'sentiment_trends': {},
                'priority_adjustments': {},
                'recommended_focus_areas': []
            }
    
    def _calculate_priority_adjustments(self, patterns: Dict[str, Any], 
                                      sentiment_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular ajustes de prioridade baseados em padrões e tendências"""
        adjustments = {}
        
        # Aumentar prioridade para problemas com tendência de piora
        for topic, trend_data in sentiment_trends.items():
            if trend_data and len(trend_data) > 0:
                latest_trend = trend_data[0]
                if latest_trend.get('direction') == 'declining':
                    adjustments[topic] = 'increase_priority'
                elif latest_trend.get('direction') == 'improving':
                    adjustments[topic] = 'maintain_priority'
        
        return adjustments
    
    def _identify_focus_areas(self, patterns: Dict[str, Any], 
                            sentiment_trends: Dict[str, Any]) -> List[str]:
        """Identificar áreas de foco baseadas em padrões e tendências"""
        focus_areas = []
        
        # Identificar problemas mais frequentes
        common_issues = patterns.get('common_issues', [])
        if common_issues:
            focus_areas.extend(common_issues[:3])  # Top 3 problemas
        
        # Identificar tópicos com tendência negativa
        for topic, trend_data in sentiment_trends.items():
            if trend_data and len(trend_data) > 0:
                latest_trend = trend_data[0]
                if latest_trend.get('direction') == 'declining':
                    if topic not in focus_areas:
                        focus_areas.append(topic)
        
        return focus_areas

