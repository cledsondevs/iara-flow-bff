"""
Serviço para geração automática de itens de backlog baseado em análise de reviews
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
import sqlite3

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.review_models import BacklogItem, SentimentType
from app.services.email_service import EmailSenderService



class BacklogGeneratorService:
    def __init__(self):
        self.database_path = os.getenv("DB_PATH", "./iara_flow.db")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Inicializar serviço de e-mail
        self.email_service = EmailSenderService()
        
        self._setup_prompts()
        self._init_tables()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados SQLite"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """Inicializar tabelas necessárias"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Tabela de reviews
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS reviews (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT,
                        rating INTEGER,
                        sentiment TEXT,
                        topics TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabela de backlog items
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS backlog_items (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        title TEXT NOT NULL,
                        description TEXT,
                        priority INTEGER DEFAULT 3,
                        category TEXT DEFAULT 'improvement',
                        source_reviews TEXT,
                        sentiment_score REAL DEFAULT 0.0,
                        frequency INTEGER DEFAULT 1,
                        status TEXT DEFAULT 'pending',
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                
        except Exception as e:
            print(f"Erro ao inicializar tabelas: {e}")
    
    def _setup_prompts(self):
        """Configurar prompts para geração de backlog"""
        
        self.backlog_generation_prompt = ChatPromptTemplate.from_template("""
Analise os seguintes problemas e sugestões extraídos de reviews de aplicativo e gere itens de backlog acionáveis.

Dados dos Reviews:
- Problemas frequentes: {frequent_issues}
- Sugestões dos usuários: {user_suggestions}
- Tópicos negativos: {negative_topics}
- Frequência por tópico: {topic_frequencies}
- Sentimento geral: {sentiment_summary}

Gere itens de backlog seguindo estas diretrizes:
1. Priorize problemas com maior frequência e impacto negativo
2. Crie títulos claros e acionáveis
3. Inclua descrição detalhada com contexto dos reviews
4. Defina prioridade (1-5, sendo 5 crítico)
5. Categorize como: bug, feature, improvement, performance, ui/ux

Retorne um JSON com a seguinte estrutura:
{{
    "backlog_items": [
        {{
            "title": "Corrigir travamento durante login",
            "description": "Usuários relatam travamento frequente ao tentar fazer login. Problema mencionado em X reviews.",
            "priority": 5,
            "category": "bug",
            "estimated_impact": "high",
            "user_pain_level": "critical",
            "frequency": 15,
            "related_topics": ["login", "crash", "authentication"]
        }}
    ]
}}

Seja específico e focado em soluções que melhorem a experiência do usuário.
""")
        
        self.priority_calculation_prompt = ChatPromptTemplate.from_template("""
Calcule a prioridade de um item de backlog baseado nos seguintes critérios:

Item: {title}
Descrição: {description}
Frequência de menções: {frequency}
Sentimento médio: {sentiment_score}
Tópicos relacionados: {topics}
Impacto estimado: {impact}

Critérios de priorização:
- Frequência alta (>10 menções) = +2 pontos
- Sentimento muito negativo (<-0.5) = +2 pontos
- Categoria "bug" = +1 ponto
- Impacto "high" = +1 ponto
- Tópicos críticos (crash, data_loss, security) = +2 pontos

Retorne um JSON:
{{
    "priority": 4,
    "reasoning": "Alta frequência de menções (15) e sentimento muito negativo (-0.8)",
    "urgency": "high"
}}
""")
    
    def analyze_review_patterns(self, package_name: str = None, 
                              days: int = 7) -> Dict[str, Any]:
        """Analisar padrões nos reviews para identificar problemas recorrentes"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                where_clause = "WHERE created_at >= datetime('now', '-' || ? || ' days')"
                params = [days]
                
                if package_name:
                    where_clause += " AND package_name = ?"
                    params.append(package_name)
                
                # Problemas mais frequentes (reviews negativos)
                cur.execute(f"""
                    SELECT 
                        json_extract(metadata, '$.analysis.main_issues') as issues_json,
                        rating,
                        id
                    FROM reviews 
                    {where_clause}
                    AND sentiment = 'negative'
                    AND json_extract(metadata, '$.analysis.main_issues') IS NOT NULL
                """, params)
                
                frequent_issues = {}
                for row in cur.fetchall():
                    try:
                        issues = json.loads(row['issues_json']) if row['issues_json'] else []
                        for issue in issues:
                            if issue not in frequent_issues:
                                frequent_issues[issue] = {
                                    'issue': issue,
                                    'frequency': 0,
                                    'ratings': [],
                                    'review_ids': []
                                }
                            frequent_issues[issue]['frequency'] += 1
                            frequent_issues[issue]['ratings'].append(row['rating'])
                            frequent_issues[issue]['review_ids'].append(row['id'])
                    except (json.JSONDecodeError, TypeError):
                        continue
                
                # Converter para lista e calcular médias
                frequent_issues_list = []
                for issue_data in frequent_issues.values():
                    if issue_data['frequency'] >= 2:
                        issue_data['avg_rating'] = sum(issue_data['ratings']) / len(issue_data['ratings'])
                        del issue_data['ratings']  # Remove para economizar espaço
                        frequent_issues_list.append(issue_data)
                
                frequent_issues_list.sort(key=lambda x: x['frequency'], reverse=True)
                frequent_issues_list = frequent_issues_list[:20]
                
                # Sugestões dos usuários
                cur.execute(f"""
                    SELECT 
                        json_extract(metadata, '$.analysis.suggestions') as suggestions_json,
                        id
                    FROM reviews 
                    {where_clause}
                    AND json_extract(metadata, '$.analysis.suggestions') IS NOT NULL
                """, params)
                
                user_suggestions = {}
                for row in cur.fetchall():
                    try:
                        suggestions = json.loads(row['suggestions_json']) if row['suggestions_json'] else []
                        for suggestion in suggestions:
                            if suggestion not in user_suggestions:
                                user_suggestions[suggestion] = {
                                    'suggestion': suggestion,
                                    'frequency': 0,
                                    'review_ids': []
                                }
                            user_suggestions[suggestion]['frequency'] += 1
                            user_suggestions[suggestion]['review_ids'].append(row['id'])
                    except (json.JSONDecodeError, TypeError):
                        continue
                
                user_suggestions_list = [
                    data for data in user_suggestions.values() 
                    if data['frequency'] >= 2
                ]
                user_suggestions_list.sort(key=lambda x: x['frequency'], reverse=True)
                user_suggestions_list = user_suggestions_list[:15]
                
                # Tópicos com sentimento negativo
                cur.execute(f"""
                    SELECT 
                        topics,
                        rating,
                        sentiment
                    FROM reviews 
                    {where_clause}
                    AND topics IS NOT NULL
                """, params)
                
                negative_topics = {}
                for row in cur.fetchall():
                    try:
                        topics = json.loads(row['topics']) if row['topics'] else []
                        for topic in topics:
                            if topic not in negative_topics:
                                negative_topics[topic] = {
                                    'topic': topic,
                                    'frequency': 0,
                                    'ratings': [],
                                    'negative_count': 0
                                }
                            negative_topics[topic]['frequency'] += 1
                            negative_topics[topic]['ratings'].append(row['rating'])
                            if row['sentiment'] == 'negative':
                                negative_topics[topic]['negative_count'] += 1
                    except (json.JSONDecodeError, TypeError):
                        continue
                
                negative_topics_list = []
                for topic_data in negative_topics.values():
                    if topic_data['negative_count'] >= 2:
                        topic_data['avg_rating'] = sum(topic_data['ratings']) / len(topic_data['ratings'])
                        topic_data['negative_ratio'] = topic_data['negative_count'] / topic_data['frequency']
                        del topic_data['ratings']  # Remove para economizar espaço
                        negative_topics_list.append(topic_data)
                
                negative_topics_list.sort(key=lambda x: (x['negative_count'], x['frequency']), reverse=True)
                negative_topics_list = negative_topics_list[:15]
                
                return {
                    "frequent_issues": frequent_issues_list,
                    "user_suggestions": user_suggestions_list,
                    "negative_topics": negative_topics_list,
                    "analysis_period": days,
                    "package_name": package_name
                }
                    
        except Exception as e:
            raise Exception(f"Erro ao analisar padrões de reviews: {str(e)}")
    
    def generate_backlog_items(self, package_name: str = None, 
                             days: int = 7) -> List[BacklogItem]:
        """Gerar itens de backlog baseado na análise de reviews"""
        try:
            # Analisar padrões
            patterns = self.analyze_review_patterns(package_name, days)
            
            # Preparar dados para o prompt
            frequent_issues = [item["issue"] for item in patterns["frequent_issues"][:10]]
            user_suggestions = [item["suggestion"] for item in patterns["user_suggestions"][:10]]
            negative_topics = [item["topic"] for item in patterns["negative_topics"][:10]]
            
            topic_frequencies = {
                item["topic"]: item["frequency"] 
                for item in patterns["negative_topics"]
            }
            
            # Calcular sentimento geral
            sentiment_summary = self._calculate_sentiment_summary(package_name, days)
            
            # Gerar prompt
            formatted_prompt = self.backlog_generation_prompt.format(
                frequent_issues=frequent_issues,
                user_suggestions=user_suggestions,
                negative_topics=negative_topics,
                topic_frequencies=topic_frequencies,
                sentiment_summary=sentiment_summary
            )
            
            # Executar geração
            response = self.llm.invoke(formatted_prompt)
            
            try:
                result = json.loads(response.content)
                backlog_data = result.get("backlog_items", [])
            except json.JSONDecodeError:
                print("Erro ao parsear resposta JSON, usando fallback")
                backlog_data = self._generate_fallback_backlog(patterns)
            
            # Converter para objetos BacklogItem
            backlog_items = []
            for item_data in backlog_data:
                # Encontrar reviews relacionados
                source_reviews = self._find_related_reviews(
                    item_data.get("related_topics", []),
                    patterns,
                    package_name,
                    days
                )
                
                backlog_item = BacklogItem(
                    title=item_data.get("title", ""),
                    description=item_data.get("description", ""),
                    priority=item_data.get("priority", 3),
                    category=item_data.get("category", "improvement"),
                    source_reviews=source_reviews,
                    sentiment_score=self._calculate_item_sentiment_score(
                        item_data.get("related_topics", []),
                        patterns
                    ),
                    frequency=item_data.get("frequency", 1),
                    metadata={
                        "estimated_impact": item_data.get("estimated_impact", "medium"),
                        "user_pain_level": item_data.get("user_pain_level", "medium"),
                        "related_topics": item_data.get("related_topics", []),
                        "generated_from": "review_analysis",
                        "analysis_period_days": days,
                        "package_name": package_name
                    }
                )
                backlog_items.append(backlog_item)
            
            return backlog_items
            
        except Exception as e:
            raise Exception(f"Erro ao gerar itens de backlog: {str(e)}")
    
    def save_backlog_items(self, items: List[BacklogItem]) -> List[str]:
        """Salvar itens de backlog no banco de dados"""
        try:
            saved_ids = []
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                for item in items:
                    # Verificar se já existe item similar
                    existing_id = self._find_similar_backlog_item(item, cur)
                    
                    if existing_id:
                        # Atualizar item existente
                        cur.execute("""
                            UPDATE backlog_items 
                            SET 
                                frequency = frequency + ?,
                                source_reviews = json_patch(COALESCE(source_reviews, '[]'), ?),
                                updated_at = CURRENT_TIMESTAMP,
                                metadata = json_patch(COALESCE(metadata, '{}'), ?)
                            WHERE id = ?
                        """, (
                            item.frequency,
                            json.dumps(item.source_reviews),
                            json.dumps({"last_update_reason": "frequency_increase"}),
                            existing_id
                        ))
                        saved_ids.append(existing_id)
                    else:
                        # Criar novo item
                        cur.execute("""
                            INSERT INTO backlog_items 
                            (title, description, priority, category, source_reviews,
                             sentiment_score, frequency, status, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            item.title,
                            item.description,
                            item.priority,
                            item.category,
                            json.dumps(item.source_reviews),
                            item.sentiment_score,
                            item.frequency,
                            item.status,
                            json.dumps(item.metadata)
                        ))
                        
                        saved_ids.append(cur.lastrowid)
                
                conn.commit()
            
            return [str(id) for id in saved_ids]
            
        except Exception as e:
            raise Exception(f"Erro ao salvar itens de backlog: {str(e)}")
    
    def _find_similar_backlog_item(self, item: BacklogItem, cursor) -> Optional[str]:
        """Encontrar item de backlog similar existente"""
        try:
            # Buscar por título similar ou tópicos relacionados
            cursor.execute("""
                SELECT id FROM backlog_items 
                WHERE 
                    (LOWER(title) LIKE LOWER(?) OR LOWER(?) LIKE LOWER(title))
                    AND status != 'done'
                    AND category = ?
                LIMIT 1
            """, (f"%{item.title}%", item.title, item.category))
            
            result = cursor.fetchone()
            return str(result['id']) if result else None
            
        except Exception:
            return None
    
    def _calculate_sentiment_summary(self, package_name: str = None, 
                                   days: int = 7) -> Dict[str, Any]:
        """Calcular resumo de sentimento para o período"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                where_clause = "WHERE created_at >= datetime('now', '-' || ? || ' days')"
                params = [days]
                
                if package_name:
                    where_clause += " AND package_name = ?"
                    params.append(package_name)
                
                cur.execute(f"""
                    SELECT 
                        sentiment,
                        COUNT(*) as count,
                        AVG(rating) as avg_rating
                    FROM reviews 
                    {where_clause}
                    AND sentiment IS NOT NULL
                    GROUP BY sentiment
                """, params)
                
                results = cur.fetchall()
                
                summary = {
                    "positive": {"count": 0, "avg_rating": 0},
                    "negative": {"count": 0, "avg_rating": 0},
                    "neutral": {"count": 0, "avg_rating": 0}
                }
                
                total_count = 0
                for row in results:
                    sentiment = row['sentiment']
                    count = row['count']
                    summary[sentiment] = {
                        "count": count,
                        "avg_rating": float(row['avg_rating'])
                    }
                    total_count += count
                
                # Calcular percentuais
                for sentiment in summary:
                    if total_count > 0:
                        summary[sentiment]["percentage"] = (
                            summary[sentiment]["count"] / total_count * 100
                        )
                    else:
                        summary[sentiment]["percentage"] = 0
                
                return summary
                    
        except Exception as e:
            return {"positive": {"count": 0}, "negative": {"count": 0}, "neutral": {"count": 0}}
    
    def _find_related_reviews(self, topics: List[str], patterns: Dict[str, Any],
                            package_name: str = None, days: int = 7) -> List[str]:
        """Encontrar IDs de reviews relacionados aos tópicos"""
        try:
            review_ids = []
            
            # Buscar em problemas frequentes
            for issue_data in patterns["frequent_issues"]:
                if any(topic.lower() in issue_data["issue"].lower() for topic in topics):
                    review_ids.extend(issue_data["review_ids"])
            
            # Buscar em sugestões
            for suggestion_data in patterns["user_suggestions"]:
                if any(topic.lower() in suggestion_data["suggestion"].lower() for topic in topics):
                    review_ids.extend(suggestion_data["review_ids"])
            
            # Remover duplicatas e limitar
            unique_ids = list(set(review_ids))[:10]
            return [str(id) for id in unique_ids]
            
        except Exception:
            return []
    
    def _calculate_item_sentiment_score(self, topics: List[str], 
                                      patterns: Dict[str, Any]) -> float:
        """Calcular score de sentimento para um item baseado nos tópicos"""
        try:
            scores = []
            
            for topic_data in patterns["negative_topics"]:
                if topic_data["topic"] in topics:
                    # Score baseado na proporção de reviews negativos
                    negative_ratio = topic_data.get("negative_ratio", 0)
                    avg_rating = topic_data.get("avg_rating", 3)
                    
                    # Normalizar para escala -1 a 1
                    score = (avg_rating - 3) / 2 - negative_ratio
                    scores.append(score)
            
            return sum(scores) / len(scores) if scores else 0.0
            
        except Exception:
            return 0.0
    
    def _generate_fallback_backlog(self, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Gerar backlog básico quando a IA falha"""
        items = []
        
        # Gerar itens baseados em problemas frequentes
        for issue in patterns["frequent_issues"][:5]:
            items.append({
                "title": f"Resolver: {issue['issue'][:50]}...",
                "description": f"Problema reportado {issue['frequency']} vezes com rating médio de {issue['avg_rating']:.1f}",
                "priority": 5 if issue['frequency'] > 10 else 3,
                "category": "bug",
                "frequency": issue['frequency'],
                "related_topics": ["bug", "issue"]
            })
        
        # Gerar itens baseados em sugestões
        for suggestion in patterns["user_suggestions"][:3]:
            items.append({
                "title": f"Implementar: {suggestion['suggestion'][:50]}...",
                "description": f"Sugestão mencionada {suggestion['frequency']} vezes pelos usuários",
                "priority": 2,
                "category": "feature",
                "frequency": suggestion['frequency'],
                "related_topics": ["feature", "suggestion"]
            })
        
        return items
    
    def get_backlog_summary(self, package_name: str = None) -> Dict[str, Any]:
        """Obter resumo do backlog atual"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                where_clause = ""
                params = []
                
                if package_name:
                    where_clause = "WHERE json_extract(metadata, '$.package_name') = ?"
                    params.append(package_name)
                
                # Contagem por status
                cur.execute(f"""
                    SELECT 
                        status,
                        COUNT(*) as count,
                        AVG(priority) as avg_priority
                    FROM backlog_items 
                    {where_clause}
                    GROUP BY status
                """, params)
                
                status_summary = {
                    row['status']: {
                        'count': row['count'],
                        'avg_priority': float(row['avg_priority'])
                    } for row in cur.fetchall()
                }
                
                # Contagem por categoria
                cur.execute(f"""
                    SELECT 
                        category,
                        COUNT(*) as count,
                        AVG(priority) as avg_priority
                    FROM backlog_items 
                    {where_clause}
                    GROUP BY category
                    ORDER BY count DESC
                """, params)
                
                category_summary = {
                    row['category']: {
                        'count': row['count'],
                        'avg_priority': float(row['avg_priority'])
                    } for row in cur.fetchall()
                }
                
                # Itens de alta prioridade
                cur.execute(f"""
                    SELECT title, priority, category, frequency
                    FROM backlog_items 
                    {where_clause}
                    {'AND' if where_clause else 'WHERE'} priority >= 4
                    AND status = 'pending'
                    ORDER BY priority DESC, frequency DESC
                    LIMIT 10
                """, params)
                
                high_priority_items = [dict(row) for row in cur.fetchall()]
                
                return {
                    "status_summary": status_summary,
                    "category_summary": category_summary,
                    "high_priority_items": high_priority_items,
                    "package_name": package_name
                }
                    
        except Exception as e:
            raise Exception(f"Erro ao obter resumo do backlog: {str(e)}")
    
    def process_reviews_to_backlog(self, package_name: str = None, 
                                 days: int = 7, 
                                 recipient_email: str = None) -> Dict[str, Any]:
        """Processo completo: analisar reviews e gerar backlog"""
        try:
            # Gerar itens de backlog
            backlog_items = self.generate_backlog_items(package_name, days)
            
            # Salvar no banco
            saved_ids = self.save_backlog_items(backlog_items)
            
            # Obter resumo
            summary = self.get_backlog_summary(package_name)
            
            # Preparar dados para o e-mail
            email_result = None
            if recipient_email:
                try:
                    # Preparar dados do relatório para o e-mail
                    report_data = self._prepare_backlog_email_data(
                        backlog_items, summary, package_name, days
                    )
                    
                    # Enviar e-mail
                    email_result = self.email_service.send_backlog_report_email(
                        recipient_email, report_data
                    )
                    
                except Exception as email_error:
                    print(f"Erro ao enviar e-mail: {email_error}")
                    email_result = {
                        "status": "error", 
                        "message": f"Erro ao enviar e-mail: {str(email_error)}"
                    }
            
            return {
                "generated_items": len(backlog_items),
                "saved_items": len(saved_ids),
                "saved_ids": saved_ids,
                "summary": summary,
                "package_name": package_name,
                "analysis_period_days": days,
                "email_result": email_result
            }
            
        except Exception as e:
            # Fallback: retornar dados mock em caso de erro
            print(f"Erro no processo de geração de backlog: {str(e)}")
            raise Exception(f"Erro no processo de geração de backlog: {str(e)}")
    
    def _prepare_backlog_email_data(self, backlog_items: List[BacklogItem], 
                                  summary: Dict[str, Any], 
                                  package_name: str, 
                                  days: int) -> Dict[str, Any]:
        """Preparar dados do backlog para envio por e-mail"""
        try:
            # Itens de alta prioridade
            high_priority_items = [
                item for item in backlog_items 
                if item.priority >= 4
            ]
            
            # Categorizar itens
            items_by_category = {}
            for item in backlog_items:
                if item.category not in items_by_category:
                    items_by_category[item.category] = []
                items_by_category[item.category].append({
                    'title': item.title,
                    'description': item.description,
                    'priority': item.priority,
                    'frequency': item.frequency,
                    'sentiment_score': item.sentiment_score
                })
            
            # Principais temas identificados
            main_themes = []
            for item in backlog_items:
                if item.metadata and 'related_topics' in item.metadata:
                    main_themes.extend(item.metadata['related_topics'])
            
            # Contar frequência dos temas
            theme_counts = {}
            for theme in main_themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            # Top 5 temas mais frequentes
            top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'package_name': package_name or 'Aplicativo',
                'total_items': len(backlog_items),
                'high_priority_count': len(high_priority_items),
                'analysis_period_days': days,
                'items_by_category': items_by_category,
                'high_priority_items': [
                    {
                        'title': item.title,
                        'description': item.description,
                        'priority': item.priority,
                        'category': item.category,
                        'frequency': item.frequency
                    } for item in high_priority_items[:10]
                ],
                'main_themes': [theme for theme, count in top_themes],
                'category_summary': summary.get('category_summary', {}),
                'status_summary': summary.get('status_summary', {})
            }
            
        except Exception as e:
            print(f"Erro ao preparar dados do e-mail: {e}")
            return {
                'package_name': package_name or 'Aplicativo',
                'total_items': len(backlog_items),
                'high_priority_count': 0,
                'analysis_period_days': days,
                'items_by_category': {},
                'high_priority_items': [],
                'main_themes': [],
                'category_summary': {},
                'status_summary': {}
            }
