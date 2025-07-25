import sqlite3
import os
from contextlib import contextmanager
from typing import Optional

class APIKeyService:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH", "./data/iara_flow.db")
        self._init_sqlite_table()

    @contextmanager
    def _get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def _init_sqlite_table(self):
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS api_keys (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        service_name TEXT NOT NULL,
                        api_key TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, service_name)
                    )
                """)
                conn.commit()
                cur.close()
        except Exception as e:
            print(f"Erro ao inicializar tabela de API Keys: {e}")

    def save_api_key(self, user_id: str, service_name: str, api_key: str):
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO api_keys (user_id, service_name, api_key)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, service_name) DO UPDATE SET
                        api_key = excluded.api_key,
                        updated_at = CURRENT_TIMESTAMP
                """, (user_id, service_name, api_key))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao salvar API Key: {str(e)}")

    def get_api_key(self, user_id: str, service_name: str) -> Optional[str]:
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT api_key FROM api_keys
                    WHERE user_id = ? AND service_name = ?
                """, (user_id, service_name))
                result = cur.fetchone()
                cur.close()
                return result["api_key"] if result else None
        except Exception as e:
            raise Exception(f"Erro ao obter API Key: {str(e)}")

    def delete_api_key(self, user_id: str, service_name: str):
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM api_keys
                    WHERE user_id = ? AND service_name = ?
                """, (user_id, service_name))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao deletar API Key: {str(e)}")


