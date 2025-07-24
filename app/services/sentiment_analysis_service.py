"""
Serviço para análise de sentimento e extração de tópicos de reviews
"""
import os
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter
import sqlite3
from datetime import datetime

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.models.review_models import Review, SentimentType, SentimentPattern

class SentimentAnalysisService:
    def __init__(self):
        self.database_path = os.getenv("DB_PATH", "./iara_flow.db")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self._setup_prompts()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados SQLite"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _setup_prompts(self):
        """Configurar prompts para análise de sentimento e tópicos"""
        
        # Prompt para análise de sentimento e tópicos
        self.sentiment_prompt = ChatPromptTemplate.from_template("""
Analise o seguinte review de aplicativo e extraia as informações solicitadas.

Review: "{review_text}"
Rating: {rating}/5

Retorne um JSON com a seguinte estrutura:
{{
    "sentiment": "positive|negative|neutral",
    "confidence": 0.95,
    "topics": ["bug", "performance", "ui"],
    "keywords": ["lento", "travando", "interface"],
    "main_issues": ["App trava frequentemente", "Interface confusa"],
    "suggestions": ["Melhorar performance", "Redesign da interface"],
    "category": "bug|feature|improvement|praise|complaint"
}}

Critérios:
- sentiment: baseado no conteúdo e rating (1-2=negative, 3=neutral, 4-5=positive)
- confidence: confiança na análise (0-1)
- topics: temas principais mencionados (máximo 5)
- keywords: palavras-chave importantes (máximo 10)
- main_issues: problemas específicos mencionados
- suggestions: sugestões implícitas ou explícitas
- category: categoria principal do feedback

Seja preciso e objetivo na análise.
""")
        
        # Prompt para agrupamento de tópicos similares
        self.topic_grouping_prompt = ChatPromptTemplate.from_template("""
Analise os seguintes tópicos extraídos de reviews e agrupe-os por similaridade:

Tópicos: {topics}

Retorne um JSON com grupos de tópicos similares:
{{
    "groups": [
        {{
            "main_topic": "performance",
            "related_topics": ["lentidão", "travamento", "lag"],
            "frequency": 15
        }}
    ]
}}
""")
    
    def analyze_review_sentiment(self, review: Review) -> Dict[str, Any]:
        """Analisar sentimento e extrair tópicos de um review"""
        try:
            # Preparar o prompt
            formatted_prompt = self.sentiment_prompt.format(
                review_text=review.content,
                rating=review.rating
            )
            
            # Executar análise
            response = self.llm.invoke(formatted_prompt)
            
            # Parsear resposta JSON
            try:
                analysis = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback para análise básica
                analysis = self._basic_sentiment_analysis(review)
            
            # Validar e normalizar dados
            sentiment = analysis.get("sentiment", "neutral")
            if sentiment not in ["positive", "negative", "neutral"]:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "confidence": analysis.get("confidence", 0.5),
                "topics": analysis.get("topics", [])[:5],  # Máximo 5 tópicos
                "keywords": analysis.get("keywords", [])[:10],  # Máximo 10 keywords
                "main_issues": analysis.get("main_issues", []),
                "suggestions": analysis.get("suggestions", []),
                "category": analysis.get("category", "general")
            }
            
        except Exception as e:
            print(f"Erro na análise de sentimento: {e}")
            return self._basic_sentiment_analysis(review)
    
    def _basic_sentiment_analysis(self, review: Review) -> Dict[str, Any]:
        """Análise básica de sentimento baseada em rating e palavras-chave"""
        # Análise baseada no rating
        if review.rating <= 2:
            sentiment = "negative"
        elif review.rating >= 4:
            sentiment = "positive"
        else:
            sentiment = "neutral"
        
        # Palavras-chave básicas
        negative_words = ["bug", "erro", "problema", "ruim", "péssimo", "lento", "trava"]
        positive_words = ["bom", "ótimo", "excelente", "rápido", "fácil", "útil"]
        
        content_lower = review.content.lower()
        
        # Extrair tópicos básicos
        topics = []
        if any(word in content_lower for word in ["bug", "erro", "problema"]):
            topics.append("bug")
        if any(word in content_lower for word in ["lento", "trava", "demora"]):
            topics.append("performance")
        if any(word in content_lower for word in ["interface", "design", "visual"]):
            topics.append("ui")
        
        return {
            "sentiment": sentiment,
            "confidence": 0.6,
            "topics": topics,
            "keywords": [],
            "main_issues": [],
            "suggestions": [],
            "category": "general"
        }
    
    def analyze_reviews_batch(self, reviews: List[Review]) -> List[Dict[str, Any]]:
        """Analisar sentimento de múltiplos reviews"""
        results = []
        
        for review in reviews:
            try:
                analysis = self.analyze_review_sentiment(review)
                analysis["review_id"] = review.id
                results.append(analysis)
            except Exception as e:
                print(f"Erro ao analisar review {review.id}: {e}")
                continue
        
        return results
    
    def update_review_analysis(self, review_id: str, analysis: Dict[str, Any]):
        """Atualizar review com análise de sentimento"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Obter metadata atual
                cur.execute("SELECT metadata FROM reviews WHERE id = ?", (review_id,))
                result = cur.fetchone()
                
                current_metadata = {}
                if result and result['metadata']:
                    try:
                        current_metadata = json.loads(result['metadata'])
                    except json.JSONDecodeError:
                        current_metadata = {}
                
                # Adicionar análise ao metadata
                current_metadata["analysis"] = {
                    "confidence": analysis["confidence"],
                    "main_issues": analysis["main_issues"],
                    "suggestions": analysis["suggestions"],
                    "category": analysis["category"]
                }
                
                cur.execute("""
                    UPDATE reviews 
                    SET 
                        sentiment = ?,
                        topics = ?,
                        keywords = ?,
                        metadata = ?
                    WHERE id = ?
                """, (
                    analysis["sentiment"],
                    json.dumps(analysis["topics"]),
                    json.dumps(analysis["keywords"]),
                    json.dumps(current_metadata),
                    review_id
                ))
                conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao atualizar análise do review: {str(e)}")
    
    def get_unanalyzed_reviews(self, limit: int = 100) -> List[Review]:
        """Obter reviews que ainda não foram analisados"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                cur.execute("""
                    SELECT * FROM reviews 
                    WHERE sentiment IS NULL 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cur.fetchall()
                
                reviews = []
                for row in rows:
                    try:
                        topics = json.loads(row['topics']) if row['topics'] else []
                        keywords = json.loads(row['keywords']) if row['keywords'] else []
                        metadata = json.loads(row['metadata']) if row['metadata'] else {}
                    except json.JSONDecodeError:
                        topics = []
                        keywords = []
                        metadata = {}
                    
                    review = Review(
                        id=str(row['id']),
                        package_name=row['package_name'],
                        store=row['store'],
                        review_id=row['review_id'],
                        user_name=row['user_name'],
                        rating=row['rating'],
                        content=row['content'],
                        date=datetime.fromisoformat(row['review_date']) if row['review_date'] else None,
                        sentiment=SentimentType(row['sentiment']) if row['sentiment'] else None,
                        topics=topics,
                        keywords=keywords,
                        metadata=metadata,
                        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                    )
                    reviews.append(review)
                
                return reviews
                    
        except Exception as e:
            raise Exception(f"Erro ao obter reviews não analisados: {str(e)}")
    
    def analyze_pending_reviews(self) -> Dict[str, Any]:
        """Analisar todos os reviews pendentes"""
        try:
            reviews = self.get_unanalyzed_reviews()
            
            results = {
                "total_reviews": len(reviews),
                "analyzed": 0,
                "errors": 0
            }
            
            for review in reviews:
                try:
                    analysis = self.analyze_review_sentiment(review)
                    self.update_review_analysis(review.id, analysis)
                    results["analyzed"] += 1
                except Exception as e:
                    print(f"Erro ao analisar review {review.id}: {e}")
                    results["errors"] += 1
            
            return results
            
        except Exception as e:
            raise Exception(f"Erro na análise de reviews pendentes: {str(e)}")
    
    def get_sentiment_summary(self, package_name: str = None, 
                            days: int = 30) -> Dict[str, Any]:
        """Obter resumo de sentimentos por aplicativo"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                where_clause = "WHERE created_at >= datetime('now', '-' || ? || ' days')"
                params = [days]
                
                if package_name:
                    where_clause += " AND package_name = ?"
                    params.append(package_name)
                
                # Contagem por sentimento
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
                
                sentiment_counts = {row['sentiment']: {
                    'count': row['count'], 
                    'avg_rating': float(row['avg_rating'])
                } for row in cur.fetchall()}
                
                # Tópicos mais frequentes
                cur.execute(f"""
                    SELECT 
                        json_extract(topics, '$[' || value || ']') as topic,
                        COUNT(*) as frequency
                    FROM reviews, json_each(topics) 
                    {where_clause}
                    AND topics IS NOT NULL
                    AND json_extract(topics, '$[' || value || ']') IS NOT NULL
                    GROUP BY topic
                    ORDER BY frequency DESC
                    LIMIT 10
                """, params)
                
                top_topics = [{'topic': row['topic'], 'frequency': row['frequency']} 
                            for row in cur.fetchall() if row['topic']]
                
                return {
                    "sentiment_distribution": sentiment_counts,
                    "top_topics": top_topics,
                    "period_days": days,
                    "package_name": package_name
                }
                    
        except Exception as e:
            raise Exception(f"Erro ao obter resumo de sentimentos: {str(e)}")
    
    def update_sentiment_patterns(self, package_name: str):
        """Atualizar padrões de sentimento para um aplicativo"""
        try:
            # Obter tópicos e sentimentos recentes
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Buscar tópicos e sentimentos dos últimos 7 dias
                cur.execute("""
                    SELECT 
                        json_extract(topics, '$[' || t.value || ']') as topic,
                        sentiment,
                        COUNT(*) as frequency,
                        GROUP_CONCAT(DISTINCT json_extract(keywords, '$[' || k.value || ']')) as keywords
                    FROM reviews r, 
                         json_each(r.topics) as t
                    LEFT JOIN json_each(r.keywords) as k ON 1=1
                    WHERE r.package_name = ? 
                    AND r.created_at >= datetime('now', '-7 days')
                    AND r.topics IS NOT NULL
                    AND json_extract(r.topics, '$[' || t.value || ']') IS NOT NULL
                    GROUP BY topic, sentiment
                """, (package_name,))
                
                patterns = cur.fetchall()
                
                for pattern in patterns:
                    if not pattern['topic']:
                        continue
                        
                    # Preparar dados do padrão
                    sentiment_trend = [{
                        "sentiment": pattern['sentiment'],
                        "frequency": pattern['frequency'],
                        "date": datetime.utcnow().isoformat()
                    }]
                    
                    keywords = []
                    if pattern['keywords']:
                        keywords = [k.strip() for k in pattern['keywords'].split(',') if k.strip()]
                    
                    # Inserir ou atualizar padrão
                    cur.execute("""
                        INSERT OR REPLACE INTO sentiment_patterns 
                        (package_name, topic, sentiment_trend, keywords, frequency, last_seen)
                        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (
                        package_name,
                        pattern['topic'],
                        json.dumps(sentiment_trend),
                        json.dumps(keywords),
                        pattern['frequency']
                    ))
                
                conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao atualizar padrões de sentimento: {str(e)}")



