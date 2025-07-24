
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
                        session_id TEXT NOT NULL,
                        message TEXT NOT NULL,
                        response TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # Tabela para perfil/memória global do usuário
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL UNIQUE,
                        profile_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                cur.close()
        except Exception as e:
            print(f"Erro ao inicializar tabelas SQLite: {e}")
    
    def save_message(self, user_id: str, session_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar conversa no SQLite"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO conversations (user_id, session_id, message, response, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id, session_id, message, response,
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao salvar conversa: {str(e)}")
    
    def get_conversation_history(self, user_id: str, session_id: str, limit: int = 10) -> List[Dict]:
        """Recuperar histórico de conversas do SQLite"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT message, response, created_at, metadata
                    FROM conversations
                    WHERE user_id = ? AND session_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, session_id, limit))
                
                results = cur.fetchall()
                cur.close()
                return [dict(row) for row in results]
        except Exception as e:
            raise Exception(f"Erro ao recuperar histórico: {str(e)}")
    
    def clear_user_memory(self, user_id: str):
        """Limpar toda a memória de um usuário"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao limpar memória do usuário: {str(e)}")
    
    def clear_conversation_history(self, user_id: str, session_id: str):
        """Limpar histórico de conversa específico de uma sessão"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM conversations WHERE user_id = ? AND session_id = ?", (user_id, session_id))
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao limpar histórico de conversa: {str(e)}")

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
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Recuperar perfil global do usuário"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT profile_data, created_at, updated_at
                    FROM user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                
                result = cur.fetchone()
                cur.close()
                
                if result:
                    profile_data = json.loads(result['profile_data'])
                    return {
                        "profile_data": profile_data,
                        "created_at": result['created_at'],
                        "updated_at": result['updated_at']
                    }
                else:
                    # Retornar perfil vazio se não existir
                    return {
                        "profile_data": {},
                        "created_at": None,
                        "updated_at": None
                    }
        except Exception as e:
            raise Exception(f"Erro ao recuperar perfil do usuário: {str(e)}")
    
    def update_user_profile(self, user_id: str, profile_updates: Dict):
        """Atualizar perfil global do usuário"""
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Primeiro, tentar recuperar o perfil existente
                current_profile = self.get_user_profile(user_id)
                
                # Mesclar os dados existentes com as atualizações
                merged_profile = current_profile["profile_data"].copy()
                merged_profile.update(profile_updates)
                
                # Inserir ou atualizar o perfil
                cur.execute("""
                    INSERT OR REPLACE INTO user_profiles (user_id, profile_data, updated_at)
                    VALUES (?, ?, ?)
                """, (
                    user_id,
                    json.dumps(merged_profile),
                    datetime.utcnow().isoformat()
                ))
                
                conn.commit()
                cur.close()
        except Exception as e:
            raise Exception(f"Erro ao atualizar perfil do usuário: {str(e)}")
    
    def extract_user_info_from_message(self, message: str, response: str) -> Dict:
        """Extrair informações do usuário de uma mensagem (método simples)"""
        extracted_info = {}
        
        # Detectar nome do usuário
        message_lower = message.lower()
        
        # Padrões para detectar nome
        name_patterns = [
            "meu nome é ",
            "me chamo ",
            "sou o ",
            "sou a ",
            "eu sou ",
            "meu nome eh ",
            "me chamo de "
        ]
        
        for pattern in name_patterns:
            if pattern in message_lower:
                # Encontrar o nome após o padrão
                start_index = message_lower.find(pattern) + len(pattern)
                remaining_text = message[start_index:].strip()
                
                # Pegar a primeira palavra como nome (assumindo que é o primeiro nome)
                name_parts = remaining_text.split()
                if name_parts:
                    # Remover pontuação comum
                    name = name_parts[0].rstrip('.,!?;')
                    if name and len(name) > 1:  # Validação básica
                        extracted_info["name"] = name.title()
                        break
        
        # Detectar outras informações úteis
        if "trabalho como" in message_lower or "sou um" in message_lower or "sou uma" in message_lower:
            extracted_info["mentioned_profession"] = True
        
        if "anos" in message_lower and any(char.isdigit() for char in message):
            extracted_info["mentioned_age"] = True
        
        return extracted_info
    
    def save_message_with_profile_update(self, user_id: str, session_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar mensagem e atualizar perfil do usuário automaticamente"""
        try:
            # Salvar a mensagem normalmente
            self.save_message(user_id, session_id, message, response, metadata)
            
            # Extrair informações do usuário da mensagem
            extracted_info = self.extract_user_info_from_message(message, response)
            
            # Se encontrou informações, atualizar o perfil
            if extracted_info:
                self.update_user_profile(user_id, extracted_info)
                
        except Exception as e:
            raise Exception(f"Erro ao salvar mensagem com atualização de perfil: {str(e)}")
    
    def get_user_context_for_chat(self, user_id: str) -> str:
        """Obter contexto do usuário para incluir no chat"""
        try:
            profile = self.get_user_profile(user_id)
            profile_data = profile["profile_data"]
            
            if not profile_data:
                return ""
            
            context_parts = []
            
            if "name" in profile_data:
                context_parts.append(f"O nome do usuário é {profile_data['name']}")
            
            if "mentioned_profession" in profile_data:
                context_parts.append("O usuário mencionou sua profissão anteriormente")
            
            if "mentioned_age" in profile_data:
                context_parts.append("O usuário mencionou sua idade anteriormente")
            
            if context_parts:
                return "Informações sobre o usuário: " + "; ".join(context_parts) + "."
            
            return ""
            
        except Exception as e:
            # Se houver erro, retornar string vazia para não quebrar o chat
            return ""


# Instância global do serviço
memory_service = MemoryService()




