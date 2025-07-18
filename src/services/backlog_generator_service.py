"""
Serviço para geração automática de itens de backlog baseado em análise de reviews
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
import psycopg2
from psycopg2.extras import RealDictCursor

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.models.review_models import BacklogItem, SentimentType

class BacklogGeneratorService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL não configurada nas variáveis de ambiente.")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self._setup_prompts()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados"""
        conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        return conn
    
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
                with conn.cursor() as cur:
                    where_clause = "WHERE created_at >= NOW() - INTERVAL '%s days'" % days
                    if package_name:
                        where_clause += f" AND package_name = '{package_name}'"
                    
                    # Problemas mais frequentes (reviews negativos)
                    cur.execute(f"""
                        SELECT 
                            jsonb_array_elements_text(
                                COALESCE(metadata->'analysis'->'main_issues', '[]')
                            ) as issue,
                            COUNT(*) as frequency,
                            AVG(rating) as avg_rating,
                            array_agg(id) as review_ids
                        FROM reviews 
                        {where_clause}
                        AND sentiment = 'negative'
                        AND metadata->'analysis'->'main_issues' IS NOT NULL
                        GROUP BY issue
                        HAVING COUNT(*) >= 2
                        ORDER BY frequency DESC
                        LIMIT 20
                    """)
                    
                    frequent_issues = []
                    for row in cur.fetchall():
                        frequent_issues.append({
                            "issue": row['issue'],
                            "frequency": row['frequency'],
                            "avg_rating": float(row['avg_rating']),
                            "review_ids": row['review_ids']
                        })
                    
                    # Sugestões dos usuários
                    cur.execute(f"""
                        SELECT 
                            jsonb_array_elements_text(
                                COALESCE(metadata->'analysis'->'suggestions', '[]')
                            ) as suggestion,
                            COUNT(*) as frequency,
                            array_agg(id) as review_ids
                        FROM reviews 
                        {where_clause}
                        AND metadata->'analysis'->'suggestions' IS NOT NULL
                        GROUP BY suggestion
                        HAVING COUNT(*) >= 2
                        ORDER BY frequency DESC
                        LIMIT 15
                    """)
                    
                    user_suggestions = []
                    for row in cur.fetchall():
                        user_suggestions.append({
                            "suggestion": row['suggestion'],
                            "frequency": row['frequency'],
                            "review_ids": row['review_ids']
                        })
                    
                    # Tópicos com sentimento negativo
                    cur.execute(f"""
                        SELECT 
                            jsonb_array_elements_text(topics) as topic,
                            COUNT(*) as frequency,
                            AVG(rating) as avg_rating,
                            COUNT(CASE WHEN sentiment = 'negative' THEN 1 END) as negative_count
                        FROM reviews 
                        {where_clause}
                        AND topics IS NOT NULL
                        GROUP BY topic
                        HAVING COUNT(CASE WHEN sentiment = 'negative' THEN 1 END) >= 2
                        ORDER BY negative_count DESC, frequency DESC
                        LIMIT 15
                    """)
                    
                    negative_topics = []
                    for row in cur.fetchall():
                        negative_topics.append({
                            "topic": row['topic'],
                            "frequency": row['frequency'],
                            "avg_rating": float(row['avg_rating']),
                            "negative_count": row['negative_count'],
                            "negative_ratio": row['negative_count'] / row['frequency']
                        })
                    
                    return {
                        "frequent_issues": frequent_issues,
                        "user_suggestions": user_suggestions,
                        "negative_topics": negative_topics,
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
                with conn.cursor() as cur:
                    for item in items:
                        # Verificar se já existe item similar
                        existing_id = self._find_similar_backlog_item(item, cur)
                        
                        if existing_id:
                            # Atualizar item existente
                            cur.execute("""
                                UPDATE backlog_items 
                                SET 
                                    frequency = frequency + %s,
                                    source_reviews = source_reviews || %s,
                                    updated_at = CURRENT_TIMESTAMP,
                                    metadata = COALESCE(metadata, '{}') || %s
                                WHERE id = %s
                                RETURNING id
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
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                RETURNING id
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
                            
                            result = cur.fetchone()
                            saved_ids.append(str(result['id']))
                    
                    conn.commit()
            
            return saved_ids
            
        except Exception as e:
            raise Exception(f"Erro ao salvar itens de backlog: {str(e)}")
    
    def _find_similar_backlog_item(self, item: BacklogItem, cursor) -> Optional[str]:
        """Encontrar item de backlog similar existente"""
        try:
            # Buscar por título similar ou tópicos relacionados
            cursor.execute("""
                SELECT id FROM backlog_items 
                WHERE 
                    (LOWER(title) LIKE LOWER(%s) OR LOWER(%s) LIKE LOWER(title))
                    AND status != 'done'
                    AND category = %s
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
                with conn.cursor() as cur:
                    where_clause = "WHERE created_at >= NOW() - INTERVAL '%s days'" % days
                    if package_name:
                        where_clause += f" AND package_name = '{package_name}'"
                    
                    cur.execute(f"""
                        SELECT 
                            sentiment,
                            COUNT(*) as count,
                            AVG(rating) as avg_rating
                        FROM reviews 
                        {where_clause}
                        AND sentiment IS NOT NULL
                        GROUP BY sentiment
                    """)
                    
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
                with conn.cursor() as cur:
                    where_clause = ""
                    params = []
                    
                    if package_name:
                        where_clause = "WHERE metadata->>'package_name' = %s"
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
                                 days: int = 7) -> Dict[str, Any]:
        """Processo completo: analisar reviews e gerar backlog"""
        try:
            # Gerar itens de backlog
            backlog_items = self.generate_backlog_items(package_name, days)
            
            # Salvar no banco
            saved_ids = self.save_backlog_items(backlog_items)
            
            # Obter resumo
            summary = self.get_backlog_summary(package_name)
            
            return {
                "generated_items": len(backlog_items),
                "saved_items": len(saved_ids),
                "saved_ids": saved_ids,
                "summary": summary,
                "package_name": package_name,
                "analysis_period_days": days
            }
            
        except Exception as e:
            raise Exception(f"Erro no processo de geração de backlog: {str(e)}")

