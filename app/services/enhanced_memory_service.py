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
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Tabela para padrões de sentimento aprendidos
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS review_sentiment_patterns (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT NOT NULL,
                        pattern_type TEXT NOT NULL,
                        pattern_data TEXT NOT NULL,
                        confidence_score REAL DEFAULT 0.0,
                        frequency INTEGER DEFAULT 1,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        UNIQUE(package_name, pattern_type, json_extract(pattern_data, '$.key'))
                    )
                """)
                
                # Tabela para correlações problema-solução
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS problem_solution_correlations (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        problem_pattern TEXT NOT NULL,
                        solution_implemented TEXT,
                        backlog_item_id TEXT,
                        sentiment_before TEXT,
                        sentiment_after TEXT,
                        effectiveness_score REAL DEFAULT 0.0,
                        time_to_impact_days INTEGER,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabela para evolução de sentimento
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sentiment_evolution (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT NOT NULL,
                        topic TEXT NOT NULL,
                        time_period DATE NOT NULL,
                        sentiment_distribution TEXT NOT NULL,
                        key_metrics TEXT,
                        trend_direction TEXT,
                        metadata TEXT,
                        UNIQUE(package_name, topic, time_period)
                    )
                """)
                
                # Tabela para otimização de backlog
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS backlog_optimization_patterns (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        pattern_name TEXT NOT NULL UNIQUE,
                        pattern_description TEXT,
                        success_indicators TEXT,
                        failure_indicators TEXT,
                        optimization_rules TEXT,
                        confidence_score REAL DEFAULT 0.0,
                        usage_count INTEGER DEFAULT 0,
                        last_used TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                conn.commit()
                cur.close()
                    
        except Exception as e:
            print(f"Erro ao criar tabelas aprimoradas: {e}")
    
    def learn_sentiment_pattern(self, package_name: str, pattern_type: str, 
                              pattern_data: Dict[str, Any], confidence: float = 0.5):
        """Aprender um novo padrão de sentimento"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Verificar se padrão já existe
                    pattern_key = pattern_data.get('key', str(uuid.uuid4()))
                    pattern_data['key'] = pattern_key
                    
                    cur.execute("""
                        INSERT OR REPLACE INTO review_sentiment_patterns 
                        (package_name, pattern_type, pattern_data, confidence_score, frequency, last_updated)
                        VALUES (?, ?, ?, ?, 
                                COALESCE((SELECT frequency FROM review_sentiment_patterns 
                                         WHERE package_name = ? AND pattern_type = ? 
                                         AND json_extract(pattern_data, '$.key') = ?), 0) + 1,
                                CURRENT_TIMESTAMP)
                    """, (
                        package_name, pattern_type, json.dumps(pattern_data),
                        confidence, package_name, pattern_type, pattern_key
                    ))
                    
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao aprender padrão de sentimento: {str(e)}")
    
    def get_sentiment_patterns(self, package_name: str, 
                             pattern_type: str = None) -> List[Dict[str, Any]]:
        """Recuperar padrões de sentimento aprendidos"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
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
                        patterns.append({
                            'id': row['id'],
                            'package_name': row['package_name'],
                            'pattern_type': row['pattern_type'],
                            'pattern_data': json.loads(row['pattern_data']) if row['pattern_data'] else {},
                            'confidence_score': row['confidence_score'],
                            'frequency': row['frequency'],
                            'last_updated': row['last_updated']
                        })
                    
                    return patterns
                    
        except Exception as e:
            raise Exception(f"Erro ao recuperar padrões de sentimento: {str(e)}")
    
    def record_sentiment_evolution(self, package_name: str, topic: str,
                                 sentiment_distribution: Dict[str, Any],
                                 period_date: datetime = None):
        """Registrar evolução do sentimento para um tópico"""
        try:
            if period_date is None:
                period_date = datetime.utcnow().date()
            
            # Calcular métricas-chave
            total_reviews = sum(sentiment_distribution.values())
            if total_reviews > 0:
                negative_ratio = sentiment_distribution.get('negative', 0) / total_reviews
                positive_ratio = sentiment_distribution.get('positive', 0) / total_reviews
                
                # Determinar direção da tendência (comparar com período anterior)
                trend_direction = self._calculate_trend_direction(
                    package_name, topic, negative_ratio, positive_ratio
                )
                
                key_metrics = {
                    'total_reviews': total_reviews,
                    'negative_ratio': negative_ratio,
                    'positive_ratio': positive_ratio,
                    'sentiment_score': positive_ratio - negative_ratio
                }
            else:
                trend_direction = 'stable'
                key_metrics = {'total_reviews': 0}
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
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
            raise Exception(f"Erro ao registrar evolução de sentimento: {str(e)}")
    
    def _calculate_trend_direction(self, package_name: str, topic: str,
                                 current_negative_ratio: float,
                                 current_positive_ratio: float) -> str:
        """Calcular direção da tendência comparando com período anterior"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT key_metrics FROM sentiment_evolution 
                        WHERE package_name = ? AND topic = ?
                        ORDER BY time_period DESC
                        LIMIT 1
                    """, (package_name, topic))
                    
                    result = cur.fetchone()
                    if not result:
                        return 'new'
                    
                    previous_metrics = json.loads(result['key_metrics'])
                    prev_negative = previous_metrics.get('negative_ratio', 0)
                    prev_positive = previous_metrics.get('positive_ratio', 0)
                    
                    # Calcular mudança
                    negative_change = current_negative_ratio - prev_negative
                    positive_change = current_positive_ratio - prev_positive
                    
                    if abs(negative_change) < 0.05 and abs(positive_change) < 0.05:
                        return 'stable'
                    elif negative_change > 0.1:
                        return 'worsening'
                    elif positive_change > 0.1:
                        return 'improving'
                    else:
                        return 'slight_change'
                        
        except Exception:
            return 'unknown'
    
    def record_problem_solution_correlation(self, problem_pattern: str,
                                          solution: str = None,
                                          backlog_item_id: str = None,
                                          sentiment_before: Dict = None,
                                          sentiment_after: Dict = None):
        """Registrar correlação entre problema e solução"""
        try:
            effectiveness_score = 0.0
            time_to_impact = None
            
            if sentiment_before and sentiment_after:
                # Calcular efetividade baseada na melhoria do sentimento
                before_score = sentiment_before.get('positive', 0) - sentiment_before.get('negative', 0)
                after_score = sentiment_after.get('positive', 0) - sentiment_after.get('negative', 0)
                effectiveness_score = after_score - before_score
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO problem_solution_correlations 
                        (problem_pattern, solution_implemented, backlog_item_id,
                         sentiment_before, sentiment_after, effectiveness_score,
                         time_to_impact_days)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        problem_pattern, solution, backlog_item_id,
                        json.dumps(sentiment_before) if sentiment_before else None,
                        json.dumps(sentiment_after) if sentiment_after else None,
                        effectiveness_score, time_to_impact
                    ))
                    
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao registrar correlação problema-solução: {str(e)}")
    
    def get_effective_solutions(self, problem_pattern: str) -> List[Dict[str, Any]]:
        """Obter soluções efetivas para um padrão de problema"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            solution_implemented,
                            effectiveness_score,
                            time_to_impact_days,
                            COUNT(*) as frequency
                        FROM problem_solution_correlations 
                        WHERE LOWER(problem_pattern) LIKE LOWER(?)
                        AND effectiveness_score > 0.1
                        GROUP BY solution_implemented, effectiveness_score, time_to_impact_days
                        ORDER BY effectiveness_score DESC, frequency DESC
                        LIMIT 5
                    """, (f"%{problem_pattern}%",))
                    
                    solutions = []
                    for row in cur.fetchall():
                        solutions.append({
                            'solution': row['solution_implemented'],
                            'effectiveness_score': row['effectiveness_score'],
                            'time_to_impact_days': row['time_to_impact_days'],
                            'frequency': row['frequency']
                        })
                    
                    return solutions
                    
        except Exception as e:
            raise Exception(f"Erro ao obter soluções efetivas: {str(e)}")
    
    def learn_backlog_optimization_pattern(self, pattern_name: str,
                                         description: str,
                                         success_indicators: List[str],
                                         failure_indicators: List[str],
                                         optimization_rules: Dict[str, Any]):
        """Aprender padrão de otimização de backlog"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT OR REPLACE INTO backlog_optimization_patterns 
                        (pattern_name, pattern_description, success_indicators,
                         failure_indicators, optimization_rules, confidence_score,
                         usage_count, last_used)
                        VALUES (?, ?, ?, ?, ?, ?, 
                                COALESCE((SELECT usage_count FROM backlog_optimization_patterns 
                                         WHERE pattern_name = ?), 0) + 1,
                                CURRENT_TIMESTAMP)
                    """, (
                        pattern_name, description,
                        json.dumps(success_indicators),
                        json.dumps(failure_indicators),
                        json.dumps(optimization_rules),
                        0.5,  # Confiança inicial
                        pattern_name
                    ))
                    
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao aprender padrão de otimização: {str(e)}")
    
    def get_backlog_optimization_suggestions(self, current_backlog: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Obter sugestões de otimização para o backlog atual"""
        try:
            suggestions = []
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM backlog_optimization_patterns 
                        ORDER BY confidence_score DESC, usage_count DESC
                    """)
                    
                    patterns = cur.fetchall()
                    
                    for pattern in patterns:
                        # Analisar se o padrão se aplica ao backlog atual
                        rules = json.loads(pattern['optimization_rules']) if pattern['optimization_rules'] else {}
                        
                        if self._pattern_applies_to_backlog(rules, current_backlog):
                            suggestions.append({
                                'pattern_name': pattern['pattern_name'],
                                'description': pattern['pattern_description'],
                                'optimization_rules': rules,
                                'confidence': pattern['confidence_score'],
                                'usage_count': pattern['usage_count']
                            })
                    
                    return suggestions[:5]  # Top 5 sugestões
                    
        except Exception as e:
            raise Exception(f"Erro ao obter sugestões de otimização: {str(e)}")
    
    def _pattern_applies_to_backlog(self, rules: Dict[str, Any], 
                                  backlog: List[Dict[str, Any]]) -> bool:
        """Verificar se um padrão de otimização se aplica ao backlog atual"""
        try:
            # Análise básica - pode ser expandida
            if 'min_items' in rules:
                if len(backlog) < rules['min_items']:
                    return False
            
            if 'required_categories' in rules:
                categories = [item.get('category', '') for item in backlog]
                for req_category in rules['required_categories']:
                    if req_category not in categories:
                        return False
            
            if 'priority_distribution' in rules:
                high_priority_count = sum(1 for item in backlog 
                                        if item.get('priority', 0) >= 4)
                if high_priority_count < rules['priority_distribution'].get('min_high_priority', 0):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_sentiment_trends(self, package_name: str, 
                           days: int = 30) -> Dict[str, Any]:
        """Obter tendências de sentimento para um aplicativo"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            topic,
                            time_period,
                            key_metrics,
                            trend_direction
                        FROM sentiment_evolution 
                        WHERE package_name = ? 
                        AND time_period >= date('now', '-' || ? || ' days')
                        ORDER BY topic, time_period
                    """, (package_name, days))
                    
                    trends = {}
                    for row in cur.fetchall():
                        topic = row['topic']
                        if topic not in trends:
                            trends[topic] = {
                                'data_points': [],
                                'current_trend': row['trend_direction']
                            }
                        
                        trends[topic]['data_points'].append({
                            'date': row['time_period'],
                            'metrics': json.loads(row['key_metrics']) if row['key_metrics'] else {}
                        })
                    
                    return {
                        'package_name': package_name,
                        'period_days': days,
                        'trends': trends
                    }
                    
        except Exception as e:
            raise Exception(f"Erro ao obter tendências de sentimento: {str(e)}")
    
    def optimize_backlog_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Otimizar geração de backlog baseado na memória de longo prazo"""
        try:
            package_name = context.get('package_name')
            current_patterns = context.get('patterns', {})
            
            # Buscar padrões históricos similares
            historical_patterns = self.get_sentiment_patterns(package_name)
            
            # Buscar soluções efetivas para problemas similares
            effective_solutions = []
            for issue in current_patterns.get('frequent_issues', []):
                solutions = self.get_effective_solutions(issue.get('issue', ''))
                effective_solutions.extend(solutions)
            
            # Obter sugestões de otimização
            current_backlog = context.get('current_backlog', [])
            optimization_suggestions = self.get_backlog_optimization_suggestions(current_backlog)
            
            # Compilar recomendações
            recommendations = {
                'avoid_duplicates': self._find_potential_duplicates(current_patterns, historical_patterns),
                'prioritize_items': self._suggest_priority_adjustments(current_patterns, effective_solutions),
                'optimization_patterns': optimization_suggestions,
                'historical_context': {
                    'similar_patterns_found': len(historical_patterns),
                    'effective_solutions_available': len(effective_solutions)
                }
            }
            
            return recommendations
            
        except Exception as e:
            raise Exception(f"Erro na otimização de geração de backlog: {str(e)}")
    
    def _find_potential_duplicates(self, current_patterns: Dict[str, Any],
                                 historical_patterns: List[Dict[str, Any]]) -> List[str]:
        """Identificar potenciais duplicatas baseado em padrões históricos"""
        duplicates = []
        
        try:
            current_issues = [issue['issue'] for issue in current_patterns.get('frequent_issues', [])]
            
            for pattern in historical_patterns:
                if pattern['pattern_type'] == 'frequent_issue':
                    historical_issue = pattern['pattern_data'].get('issue', '')
                    
                    for current_issue in current_issues:
                        # Verificação simples de similaridade
                        if (len(set(current_issue.lower().split()) & 
                               set(historical_issue.lower().split())) >= 2):
                            duplicates.append(f"Possível duplicata: '{current_issue}' similar a '{historical_issue}'")
            
            return duplicates
            
        except Exception:
            return []
    
    def _suggest_priority_adjustments(self, current_patterns: Dict[str, Any],
                                    effective_solutions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sugerir ajustes de prioridade baseado em soluções efetivas"""
        suggestions = []
        
        try:
            for issue in current_patterns.get('frequent_issues', []):
                issue_text = issue.get('issue', '').lower()
                
                # Verificar se há soluções efetivas conhecidas
                for solution in effective_solutions:
                    if any(word in issue_text for word in solution['solution'].lower().split()):
                        suggestions.append({
                            'issue': issue['issue'],
                            'suggested_priority': min(5, issue.get('frequency', 1) // 2 + 2),
                            'reason': f"Solução efetiva conhecida (score: {solution['effectiveness_score']:.2f})",
                            'recommended_solution': solution['solution']
                        })
                        break
            
            return suggestions
            
        except Exception:
            return []

