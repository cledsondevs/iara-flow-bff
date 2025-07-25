"""
Serviço para coleta de reviews de lojas de aplicativos
"""
import os
import json
import uuid
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
from contextlib import contextmanager

from app.models.review_models import Review, StoreType, AppConfig
from app.config.settings import Config

class ReviewCollectorService:
    def __init__(self):
        self.database_path = "./data/iara_flow.db"
        self.api_base_url = "http://200.98.64.133:5000/api/scraping/google-play"
        self._create_tables()
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexões com SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _create_tables(self):
        """Criar tabelas necessárias para reviews e configurações"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Tabela para configurações de aplicativos
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS app_configs (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT NOT NULL UNIQUE,
                        app_name TEXT NOT NULL,
                        stores TEXT NOT NULL DEFAULT '["google_play"]',
                        collection_frequency INTEGER DEFAULT 6,
                        is_active BOOLEAN DEFAULT 1,
                        last_collection TIMESTAMP,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabela para reviews coletados
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS reviews (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT NOT NULL,
                        store TEXT NOT NULL,
                        review_id TEXT NOT NULL,
                        user_name TEXT,
                        rating INTEGER,
                        content TEXT NOT NULL,
                        review_date TIMESTAMP,
                        sentiment TEXT,
                        topics TEXT DEFAULT '[]',
                        keywords TEXT DEFAULT '[]',
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(package_name, store, review_id)
                    )
                """)
                
                # Tabela para itens de backlog (se não existir)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS backlog_items (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        title TEXT NOT NULL,
                        description TEXT,
                        priority INTEGER DEFAULT 1,
                        category TEXT,
                        source_reviews TEXT DEFAULT '[]',
                        sentiment_score REAL DEFAULT 0.0,
                        frequency INTEGER DEFAULT 1,
                        status TEXT DEFAULT 'pending',
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Tabela para padrões de sentimento
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sentiment_patterns (
                        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
                        package_name TEXT NOT NULL,
                        topic TEXT NOT NULL,
                        sentiment_trend TEXT DEFAULT '[]',
                        keywords TEXT DEFAULT '[]',
                        frequency INTEGER DEFAULT 0,
                        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        UNIQUE(package_name, topic)
                    )
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
                cur = conn.cursor()
                
                cur.execute("""
                    INSERT OR REPLACE INTO app_configs 
                    (package_name, app_name, stores, collection_frequency, is_active)
                    VALUES (?, ?, ?, ?, 1)
                """, (package_name, app_name, json.dumps(stores_json), collection_frequency))
                
                # Obter o ID do registro inserido/atualizado
                cur.execute("SELECT id FROM app_configs WHERE package_name = ?", (package_name,))
                result = cur.fetchone()
                conn.commit()
                
                return str(result['id']) if result else str(cur.lastrowid)
                    
        except Exception as e:
            raise Exception(f"Erro ao adicionar configuração do app: {str(e)}")
    
    def get_apps_for_collection(self) -> List[AppConfig]:
        """Obter aplicativos que precisam de coleta de reviews"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Buscar apps ativos que precisam de coleta
                cur.execute("""
                    SELECT * FROM app_configs 
                    WHERE is_active = 1 
                    AND (
                        last_collection IS NULL 
                        OR last_collection < datetime('now', '-6 hours')
                    )
                """)
                
                rows = cur.fetchall()
                
                configs = []
                for row in rows:
                    try:
                        stores_data = json.loads(row['stores']) if row['stores'] else ['google_play']
                        stores = [StoreType(store) for store in stores_data]
                    except (json.JSONDecodeError, ValueError):
                        stores = [StoreType.GOOGLE_PLAY]
                    
                    config = AppConfig(
                        id=str(row['id']),
                        package_name=row['package_name'],
                        app_name=row['app_name'],
                        stores=stores,
                        collection_frequency=row['collection_frequency'],
                        is_active=bool(row['is_active']),
                        last_collection=datetime.fromisoformat(row['last_collection']) if row['last_collection'] else None,
                        metadata=json.loads(row['metadata']) if row['metadata'] else None,
                        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                    )
                    configs.append(config)
                
                return configs
                    
        except Exception as e:
            raise Exception(f"Erro ao obter apps para coleta: {str(e)}")
    
    def get_app_config_by_package_name(self, package_name: str) -> Optional[AppConfig]:
        """Obter configuração de um aplicativo pelo package_name"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                cur.execute("""
                    SELECT * FROM app_configs 
                    WHERE package_name = ?
                """, (package_name,))
                
                row = cur.fetchone()
                
                if row:
                    try:
                        stores_data = json.loads(row['stores']) if row['stores'] else ['google_play']
                        stores = [StoreType(store) for store in stores_data]
                    except (json.JSONDecodeError, ValueError):
                        stores = [StoreType.GOOGLE_PLAY]
                    
                    config = AppConfig(
                        id=str(row['id']),
                        package_name=row['package_name'],
                        app_name=row['app_name'],
                        stores=stores,
                        collection_frequency=row['collection_frequency'],
                        is_active=bool(row['is_active']),
                        last_collection=datetime.fromisoformat(row['last_collection']) if row['last_collection'] else None,
                        metadata=json.loads(row['metadata']) if row['metadata'] else None,
                        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                    )
                    return config
                return None
                    
        except Exception as e:
            raise Exception(f"Erro ao obter configuração do app: {str(e)}")

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
                cur = conn.cursor()
                
                for review in reviews:
                    try:
                        cur.execute("""
                            INSERT OR IGNORE INTO reviews 
                            (package_name, store, review_id, user_name, rating, 
                             content, review_date, sentiment, topics, keywords, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            review.package_name,
                            review.store.value,
                            review.review_id,
                            review.user_name,
                            review.rating,
                            review.content,
                            review.date.isoformat() if review.date else None,
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
                cur = conn.cursor()
                
                cur.execute("""
                    UPDATE app_configs 
                    SET last_collection = CURRENT_TIMESTAMP 
                    WHERE package_name = ?
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

