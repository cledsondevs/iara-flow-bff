from dotenv import load_dotenv
load_dotenv()
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


class MemoryService:
    def __init__(self):
        # Configuração do PostgreSQL
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", "admin"),
            "user": os.getenv("DB_USER", "admin"),
            "password": os.getenv("DB_PASSWORD", "admin")
        }
        
        # Inicializar tabelas do PostgreSQL
        self._init_postgres_tables()
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexões com PostgreSQL"""
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _init_postgres_tables(self):
        """Inicializar tabelas do PostgreSQL"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Tabela para metadados de conversas
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS conversations (
                            id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) NOT NULL,
                            message TEXT NOT NULL,
                            response TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            metadata JSONB
                        )
                    """)
                    
                    conn.commit()
                    
        except Exception as e:
            print(f"Erro ao inicializar tabelas: {e}")
    
    def save_conversation(self, user_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar conversa no PostgreSQL"""
        try:
            # Salvar metadados no PostgreSQL
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO conversations (user_id, message, response, metadata)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        user_id, message, response,
                        json.dumps(metadata) if metadata else None
                    ))
                    conn.commit()
            
        except Exception as e:
            raise Exception(f"Erro ao salvar conversa: {str(e)}")
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Recuperar histórico de conversas do PostgreSQL"""
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT message, response, created_at, metadata
                        FROM conversations
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        LIMIT %s
                    """, (user_id, limit))
                    
                    results = cur.fetchall()
                    return [dict(row) for row in results]
                    
        except Exception as e:
            raise Exception(f"Erro ao recuperar histórico: {str(e)}")
    
    def clear_user_memory(self, user_id: str):
        """Limpar toda a memória de um usuário"""
        try:
            # Limpar do PostgreSQL
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM conversations WHERE user_id = %s", (user_id,))
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao limpar memória do usuário: {str(e)}")
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """Obter estatísticas da memória do usuário"""
        try:
            stats = {
                "total_conversations": 0
            }
            
            # Contar no PostgreSQL
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM conversations WHERE user_id = %s", (user_id,))
                    stats["total_conversations"] = cur.fetchone()[0]
            
            return stats
            
        except Exception as e:
            raise Exception(f"Erro ao obter estatísticas: {str(e)}")


# Instância global do serviço
memory_service = MemoryService()



