
from dotenv import load_dotenv
load_dotenv()
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
from contextlib import contextmanager


class MemoryService:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH", "./iara_flow.db")
        self._init_sqlite_tables()
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexões com SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row # Para retornar resultados como dicionários
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _init_sqlite_tables(self):
        """Inicializar tabelas do SQLite"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                # Tabela para metadados de conversas
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        message TEXT NOT NULL,
                        response TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                conn.commit()
                cur.close()
        except Exception as e:
            print(f"Erro ao inicializar tabelas SQLite: {e}")
    
    def save_conversation(self, user_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar conversa no SQLite"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO conversations (user_id, message, response, metadata)
                    VALUES (?, ?, ?, ?)
                """, (
                    user_id, message, response,
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao salvar conversa: {str(e)}")
    
    def get_conversation_history(self, user_id: str, session_id: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Recuperar histórico de conversas do SQLite"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                if session_id:
                    cur.execute("""
                        SELECT message, response, created_at, metadata
                        FROM conversations
                        WHERE user_id = ? AND json_extract(metadata, '$.session_id') = ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """, (user_id, session_id, limit))
                else:
                    cur.execute("""
                        SELECT message, response, created_at, metadata
                        FROM conversations
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """, (user_id, limit))
                
                results = cur.fetchall()
                cur.close()
                
                formatted_history = []
                for row in reversed(results): # Inverter para ordem cronológica
                    formatted_history.append({"type": "human", "content": row["message"]})
                    formatted_history.append({"type": "ai", "content": row["response"]})
                return formatted_history
        except Exception as e:
            raise Exception(f"Erro ao recuperar histórico: {str(e)}")
    
    def clear_conversation_history(self, user_id: str, session_id: Optional[str] = None):
        """Limpar memória do agente para um usuário e sessão específicos"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                if session_id:
                    cur.execute("DELETE FROM conversations WHERE user_id = ? AND json_extract(metadata, '$.session_id') = ?", (user_id, session_id))
                else:
                    cur.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao limpar memória do usuário: {str(e)}")
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """Obter estatísticas da memória do usuário"""
        try:
            stats = {
                "total_conversations": 0
            }
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (user_id,))
                stats["total_conversations"] = cur.fetchone()[0]
                cur.close()
            return stats
        except Exception as e:
            raise Exception(f"Erro ao obter estatísticas: {str(e)}")


# Instância global do serviço
memory_service = MemoryService()




