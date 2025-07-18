"""
Serviço para coleta de reviews de lojas de aplicativos
"""
import os
import json
import uuid
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import psycopg2
from psycopg2.extras import RealDictCursor

from src.models.review_models import Review, StoreType, AppConfig

class ReviewCollectorService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL não configurada nas variáveis de ambiente.")
        
        self.api_base_url = "https://bff-analyse.vercel.app/api/apps"
        self._create_tables()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados"""
        conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        return conn
    
    def _create_tables(self):
        """Criar tabelas necessárias para reviews e configurações"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Habilitar extensão uuid-ossp se não existir
                    cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
                    
                    # Tabela para configurações de aplicativos
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS app_configs (
                            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                            package_name VARCHAR(255) NOT NULL UNIQUE,
                            app_name VARCHAR(255) NOT NULL,
                            stores JSONB NOT NULL DEFAULT '["google_play"]',
                            collection_frequency INTEGER DEFAULT 6,
                            is_active BOOLEAN DEFAULT true,
                            last_collection TIMESTAMP WITH TIME ZONE,
                            metadata JSONB,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # Tabela para reviews coletados
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS reviews (
                            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                            package_name VARCHAR(255) NOT NULL,
                            store VARCHAR(50) NOT NULL,
                            review_id VARCHAR(255) NOT NULL,
                            user_name VARCHAR(255),
                            rating INTEGER,
                            content TEXT NOT NULL,
                            review_date TIMESTAMP WITH TIME ZONE,
                            sentiment VARCHAR(20),
                            topics JSONB DEFAULT '[]',
                            keywords JSONB DEFAULT '[]',
                            metadata JSONB,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(package_name, store, review_id)
                        );
                    """)
                    
                    # Tabela para itens de backlog
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS backlog_items (
                            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                            title VARCHAR(500) NOT NULL,
                            description TEXT,
                            priority INTEGER DEFAULT 1,
                            category VARCHAR(100),
                            source_reviews JSONB DEFAULT '[]',
                            sentiment_score REAL DEFAULT 0.0,
                            frequency INTEGER DEFAULT 1,
                            status VARCHAR(50) DEFAULT 'pending',
                            metadata JSONB,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # Tabela para padrões de sentimento
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS sentiment_patterns (
                            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                            package_name VARCHAR(255) NOT NULL,
                            topic VARCHAR(255) NOT NULL,
                            sentiment_trend JSONB DEFAULT '[]',
                            keywords JSONB DEFAULT '[]',
                            frequency INTEGER DEFAULT 0,
                            last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            metadata JSONB,
                            UNIQUE(package_name, topic)
                        );
                    """)
                    
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao criar tabelas: {str(e)}")
    
    def add_app_config(self, package_name: str, app_name: str, 
                      stores: List[StoreType] = None, 
                      collection_frequency: int = 6) -> str:
        """Adicionar configuração de aplicativo para coleta"""
        try:
            if stores is None:
                stores = [StoreType.GOOGLE_PLAY]
            
            stores_json = [store.value for store in stores]
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO app_configs 
                        (package_name, app_name, stores, collection_frequency)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (package_name) 
                        DO UPDATE SET 
                            app_name = EXCLUDED.app_name,
                            stores = EXCLUDED.stores,
                            collection_frequency = EXCLUDED.collection_frequency,
                            is_active = true
                        RETURNING id
                    """, (package_name, app_name, json.dumps(stores_json), collection_frequency))
                    
                    result = cur.fetchone()
                    conn.commit()
                    return str(result['id'])
                    
        except Exception as e:
            raise Exception(f"Erro ao adicionar configuração do app: {str(e)}")
    
    def get_apps_for_collection(self) -> List[AppConfig]:
        """Obter aplicativos que precisam de coleta de reviews"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Buscar apps ativos que precisam de coleta
                    cur.execute("""
                        SELECT * FROM app_configs 
                        WHERE is_active = true 
                        AND (
                            last_collection IS NULL 
                            OR last_collection < NOW() - INTERVAL '%s hours'
                        )
                    """, (6,))  # Default de 6 horas
                    
                    rows = cur.fetchall()
                    
                    configs = []
                    for row in rows:
                        stores = [StoreType(store) for store in row['stores']]
                        config = AppConfig(
                            id=str(row['id']),
                            package_name=row['package_name'],
                            app_name=row['app_name'],
                            stores=stores,
                            collection_frequency=row['collection_frequency'],
                            is_active=row['is_active'],
                            last_collection=row['last_collection'],
                            metadata=row['metadata'],
                            created_at=row['created_at']
                        )
                        configs.append(config)
                    
                    return configs
                    
        except Exception as e:
            raise Exception(f"Erro ao obter apps para coleta: {str(e)}")
    
    def collect_reviews(self, package_name: str, store: StoreType, limit: int = 100) -> List[Review]:
        """Coletar reviews de um aplicativo específico"""
        try:
            store_name = store.value
            url = f"{self.api_base_url}/{package_name}/reviews"
            params = {
                "store": store_name,
                "limit": limit
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            reviews = []
            
            if "reviews" in data:
                for review_data in data["reviews"]:
                    review = Review(
                        package_name=package_name,
                        store=store,
                        review_id=review_data.get("id", ""),
                        user_name=review_data.get("userName", ""),
                        rating=review_data.get("score", 0),
                        content=review_data.get("text", ""),
                        date=self._parse_date(review_data.get("date")),
                        metadata=review_data
                    )
                    reviews.append(review)
            
            return reviews
            
        except Exception as e:
            raise Exception(f"Erro ao coletar reviews: {str(e)}")
    
    def save_reviews(self, reviews: List[Review]) -> int:
        """Salvar reviews no banco de dados"""
        try:
            saved_count = 0
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    for review in reviews:
                        try:
                            cur.execute("""
                                INSERT INTO reviews 
                                (package_name, store, review_id, user_name, rating, 
                                 content, review_date, sentiment, topics, keywords, metadata)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (package_name, store, review_id) DO NOTHING
                            """, (
                                review.package_name,
                                review.store.value,
                                review.review_id,
                                review.user_name,
                                review.rating,
                                review.content,
                                review.date,
                                review.sentiment.value if review.sentiment else None,
                                json.dumps(review.topics),
                                json.dumps(review.keywords),
                                json.dumps(review.metadata)
                            ))
                            
                            if cur.rowcount > 0:
                                saved_count += 1
                                
                        except Exception as e:
                            print(f"Erro ao salvar review {review.review_id}: {e}")
                            continue
                    
                    conn.commit()
            
            return saved_count
            
        except Exception as e:
            raise Exception(f"Erro ao salvar reviews: {str(e)}")
    
    def update_last_collection(self, package_name: str):
        """Atualizar timestamp da última coleta"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE app_configs 
                        SET last_collection = CURRENT_TIMESTAMP 
                        WHERE package_name = %s
                    """, (package_name,))
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao atualizar última coleta: {str(e)}")
    
    def collect_all_pending(self) -> Dict[str, Any]:
        """Coletar reviews de todos os aplicativos pendentes"""
        try:
            apps = self.get_apps_for_collection()
            results = {
                "total_apps": len(apps),
                "total_reviews": 0,
                "apps_processed": [],
                "errors": []
            }
            
            for app in apps:
                try:
                    app_reviews = 0
                    
                    for store in app.stores:
                        reviews = self.collect_reviews(app.package_name, store)
                        saved_count = self.save_reviews(reviews)
                        app_reviews += saved_count
                    
                    self.update_last_collection(app.package_name)
                    
                    results["apps_processed"].append({
                        "package_name": app.package_name,
                        "app_name": app.app_name,
                        "reviews_collected": app_reviews
                    })
                    
                    results["total_reviews"] += app_reviews
                    
                except Exception as e:
                    error_msg = f"Erro ao processar {app.package_name}: {str(e)}"
                    results["errors"].append(error_msg)
                    print(error_msg)
            
            return results
            
        except Exception as e:
            raise Exception(f"Erro na coleta geral: {str(e)}")
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Converter string de data para datetime"""
        if not date_str:
            return None
        
        try:
            # Tentar diferentes formatos de data
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None

