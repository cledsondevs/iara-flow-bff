"""
Serviço de Memória Isolado - Versão Profissional
Sistema de memória completamente novo e isolado para garantir persistência confiável
"""

import json
import os
import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager
from app.config.settings import Config

# Configurar logging específico para o serviço isolado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IsolatedMemoryService:
    """
    Serviço de memória completamente isolado com nova arquitetura de banco de dados
    """
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        logger.info(f"[ISOLATED_MEMORY] Inicializando serviço isolado - DB: {self.db_path}")
        
        # Garantir diretório do banco
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"[ISOLATED_MEMORY] Diretório criado: {db_dir}")
        
        self._initialize_isolated_tables()
        logger.info("[ISOLATED_MEMORY] Serviço inicializado com sucesso")
    
    @contextmanager
    def _get_db_connection(self):
        """Context manager para conexões isoladas com SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            # Configurações para melhor performance e confiabilidade
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA temp_store=MEMORY")
            conn.execute("PRAGMA mmap_size=268435456")  # 256MB
            yield conn
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro na conexão: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _initialize_isolated_tables(self):
        """Inicializar tabelas isoladas do sistema de memória"""
        try:
            logger.info("[ISOLATED_MEMORY] Criando tabelas isoladas...")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Tabela principal de memória de conversas (isolada)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory_conversations (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        user_message TEXT NOT NULL,
                        assistant_response TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        created_at TEXT NOT NULL,
                        metadata_json TEXT,
                        message_hash TEXT
                    )
                """)
                
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_conversations_user_id ON memory_conversations(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_conversations_session_id ON memory_conversations(session_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_conversations_timestamp ON memory_conversations(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_conversations_user_session_time ON memory_conversations(user_id, session_id, timestamp)")
                
                # Tabela isolada de perfis de usuário
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory_user_profiles (
                        id TEXT PRIMARY KEY,
                        user_id TEXT UNIQUE NOT NULL,
                        profile_json TEXT NOT NULL,
                        version INTEGER DEFAULT 1,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        last_interaction TEXT
                    )
                """)
                
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_profiles_user_id ON memory_user_profiles(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_profiles_updated_at ON memory_user_profiles(updated_at)")
                
                # Tabela para fatos específicos do usuário (isolada)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory_user_facts (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        fact_content TEXT NOT NULL,
                        fact_type TEXT DEFAULT 'general',
                        confidence REAL DEFAULT 1.0,
                        source TEXT DEFAULT 'conversation',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1
                    )
                """)
                
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_facts_user_id ON memory_user_facts(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_facts_fact_type ON memory_user_facts(fact_type)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_facts_is_active ON memory_user_facts(is_active)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_user_facts_user_active ON memory_user_facts(user_id, is_active)")
                
                # Tabela para contexto de sessão (isolada)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory_session_context (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        context_data TEXT NOT NULL,
                        last_updated TEXT NOT NULL,
                        expires_at TEXT,
                        is_active INTEGER DEFAULT 1,
                        UNIQUE(user_id, session_id)
                    )
                """)
                
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_session_context_user_id ON memory_session_context(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_session_context_session_id ON memory_session_context(session_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_session_context_is_active ON memory_session_context(is_active)")
                conn.commit()
                logger.info("[ISOLATED_MEMORY] Tabelas isoladas criadas com sucesso")
                
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao criar tabelas: {e}")
            raise e
    
    def save_conversation_isolated(
        self, 
        user_id: str, 
        session_id: str, 
        user_message: str, 
        assistant_response: str, 
        metadata: Optional[Dict] = None
    ) -> str:
        """Salvar conversa no sistema isolado"""
        try:
            conversation_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().timestamp()
            created_at = datetime.utcnow().isoformat()
            
            # Criar hash da mensagem para evitar duplicatas
            import hashlib
            message_content = f"{user_id}:{session_id}:{user_message}:{assistant_response}"
            message_hash = hashlib.md5(message_content.encode()).hexdigest()
            
            logger.info(f"[ISOLATED_MEMORY] Salvando conversa - User: {user_id}, Session: {session_id}")
            logger.info(f"[ISOLATED_MEMORY] Mensagem: {user_message[:100]}...")
            logger.info(f"[ISOLATED_MEMORY] Resposta: {assistant_response[:100]}...")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar se já existe uma conversa similar recente (evitar duplicatas)
                cursor.execute("""
                    SELECT id FROM memory_conversations 
                    WHERE user_id = ? AND session_id = ? AND message_hash = ?
                    AND timestamp > ?
                """, (user_id, session_id, message_hash, timestamp - 300))  # 5 minutos
                
                existing = cursor.fetchone()
                if existing:
                    logger.warning(f"[ISOLATED_MEMORY] Conversa duplicada detectada, ignorando")
                    return existing['id']
                
                # Inserir nova conversa
                cursor.execute("""
                    INSERT INTO memory_conversations 
                    (id, user_id, session_id, user_message, assistant_response, 
                     timestamp, created_at, metadata_json, message_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    conversation_id, user_id, session_id, user_message, 
                    assistant_response, timestamp, created_at,
                    json.dumps(metadata) if metadata else None,
                    message_hash
                ))
                
                conn.commit()
                
            logger.info(f"[ISOLATED_MEMORY] Conversa salva - ID: {conversation_id}")
            
            # Atualizar perfil do usuário automaticamente
            self._auto_update_user_profile(user_id, user_message, assistant_response)
            
            return conversation_id
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao salvar conversa: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def get_conversation_history_isolated(
        self, 
        user_id: str, 
        limit: int = 10
    ) -> List[Dict]:
        """Recuperar histórico de conversas do sistema isolado, independente da sessão"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Recuperando histórico global - User: {user_id}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, user_message, assistant_response, timestamp, 
                           created_at, metadata_json
                    FROM memory_conversations
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, limit))
                
                results = cursor.fetchall()
                
            conversations = []
            for row in results:
                conv_data = {
                    "id": row["id"],
                    "message": row["user_message"],
                    "response": row["assistant_response"],
                    "timestamp": row["timestamp"],
                    "created_at": row["created_at"],
                    "metadata": {}
                }
                
                if row["metadata_json"]:
                    try:
                        conv_data["metadata"] = json.loads(row["metadata_json"])
                    except json.JSONDecodeError:
                        logger.warning(f"[ISOLATED_MEMORY] Erro ao parsear metadata para conversa {row['id']}")
                
                conversations.append(conv_data)
            
            logger.info(f"[ISOLATED_MEMORY] Histórico global recuperado: {len(conversations)} conversas")
            return conversations
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao recuperar histórico global: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def get_user_profile_isolated(self, user_id: str) -> Dict:
        """Recuperar perfil do usuário do sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Recuperando perfil - User: {user_id}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT profile_json, version, created_at, updated_at, last_interaction
                    FROM memory_user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                
                result = cursor.fetchone()
                
            if result:
                profile_data = json.loads(result['profile_json'])
                logger.info(f"[ISOLATED_MEMORY] Perfil encontrado - User: {user_id}, Versão: {result['version']}")
                
                return {
                    "user_id": user_id,
                    "profile_data": profile_data,
                    "version": result['version'],
                    "created_at": result['created_at'],
                    "updated_at": result['updated_at'],
                    "last_interaction": result['last_interaction']
                }
            else:
                logger.info(f"[ISOLATED_MEMORY] Perfil não encontrado - User: {user_id}, criando novo")
                return self._create_new_user_profile(user_id)
                
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao recuperar perfil: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def update_user_profile_isolated(self, user_id: str, profile_updates: Dict) -> bool:
        """Atualizar perfil do usuário no sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Atualizando perfil - User: {user_id}")
            logger.info(f"[ISOLATED_MEMORY] Updates: {profile_updates}")
            
            current_time = datetime.utcnow().isoformat()
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Buscar perfil atual
                cursor.execute("""
                    SELECT profile_json, version FROM memory_user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                
                result = cursor.fetchone()
                
                if result:
                    # Atualizar perfil existente
                    current_profile = json.loads(result['profile_json'])
                    new_version = result['version'] + 1
                    
                    # Mesclar dados
                    current_profile.update(profile_updates)
                    
                    cursor.execute("""
                        UPDATE memory_user_profiles
                        SET profile_json = ?, version = ?, updated_at = ?, last_interaction = ?
                        WHERE user_id = ?
                    """, (
                        json.dumps(current_profile),
                        new_version,
                        current_time,
                        current_time,
                        user_id
                    ))
                    
                    logger.info(f"[ISOLATED_MEMORY] Perfil atualizado - User: {user_id}, Versão: {new_version}")
                    
                else:
                    # Criar novo perfil
                    profile_id = str(uuid.uuid4())
                    
                    cursor.execute("""
                        INSERT INTO memory_user_profiles
                        (id, user_id, profile_json, version, created_at, updated_at, last_interaction)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        profile_id,
                        user_id,
                        json.dumps(profile_updates),
                        1,
                        current_time,
                        current_time,
                        current_time
                    ))
                    
                    logger.info(f"[ISOLATED_MEMORY] Novo perfil criado - User: {user_id}")
                
                conn.commit()
                
            return True
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao atualizar perfil: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def save_user_fact_isolated(self, user_id: str, fact_content: str, fact_type: str = "general") -> str:
        """Salvar fato específico do usuário no sistema isolado"""
        try:
            fact_id = str(uuid.uuid4())
            current_time = datetime.utcnow().isoformat()
            
            logger.info(f"[ISOLATED_MEMORY] Salvando fato - User: {user_id}, Tipo: {fact_type}")
            logger.info(f"[ISOLATED_MEMORY] Conteúdo: {fact_content}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO memory_user_facts
                    (id, user_id, fact_content, fact_type, confidence, source, 
                     created_at, updated_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fact_id, user_id, fact_content, fact_type, 1.0, "conversation",
                    current_time, current_time, 1
                ))
                
                conn.commit()
                
            logger.info(f"[ISOLATED_MEMORY] Fato salvo - ID: {fact_id}")
            return fact_id
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao salvar fato: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def get_user_facts_isolated(self, user_id: str) -> List[Dict]:
        """Recuperar fatos do usuário do sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Recuperando fatos - User: {user_id}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, fact_content, fact_type, confidence, source, 
                           created_at, updated_at
                    FROM memory_user_facts
                    WHERE user_id = ? AND is_active = 1
                    ORDER BY updated_at DESC
                """, (user_id,))
                
                results = cursor.fetchall()
                
            facts = []
            for row in results:
                facts.append({
                    "id": row['id'],
                    "content": row['fact_content'],
                    "type": row['fact_type'],
                    "confidence": row['confidence'],
                    "source": row['source'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                })
            
            logger.info(f"[ISOLATED_MEMORY] Fatos recuperados: {len(facts)}")
            return facts
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao recuperar fatos: {e}")
            raise Exception(f"Erro no sistema isolado de memória: {str(e)}")
    
    def get_user_context_isolated(self, user_id: str, session_id: str = None) -> str:
        """Obter contexto completo do usuário do sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Gerando contexto - User: {user_id}")
            
            context_parts = []
            
            # 1. Perfil do usuário
            profile = self.get_user_profile_isolated(user_id)
            if profile["profile_data"]:
                context_parts.append(f"Perfil do usuário: {json.dumps(profile['profile_data'], ensure_ascii=False)}")
            
            # 2. Fatos específicos
            facts = self.get_user_facts_isolated(user_id)
            if facts:
                facts_text = "Fatos importantes sobre o usuário:\n"
                for fact in facts[:5]:  # Limitar a 5 fatos mais recentes
                    facts_text += f"- {fact['content']}\n"
                context_parts.append(facts_text)
            
            # 3. Histórico recente (se session_id fornecido)
            if session_id:
                history = self.get_conversation_history_isolated(user_id, session_id, limit=3)
                if history:
                    history_text = "Histórico recente da conversa:\n"
                    for conv in reversed(history):  # Ordem cronológica
                        history_text += f"Usuário: {conv['message']}\n"
                        history_text += f"Assistente: {conv['response']}\n"
                    context_parts.append(history_text)
            
            full_context = "\n\n".join(context_parts)
            logger.info(f"[ISOLATED_MEMORY] Contexto gerado: {len(full_context)} caracteres")
            
            return full_context
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao gerar contexto: {e}")
            return ""
    
    def detect_and_save_memory_command(self, user_id: str, message: str) -> Tuple[str, bool]:
        """Detectar comandos de memória e processar"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Detectando comando de memória - User: {user_id}")
            
            message_lower = message.lower().strip()
            
            # Padrões de comando de memória
            memory_patterns = [
                ("lembre-se disso:", "remember"),
                ("lembre disso:", "remember"),
                ("salve isso:", "save"),
                ("guarde isso:", "save"),
                ("importante", "note"),
                ("memorize isso:", "remember"),
                ("anote isso:", "note")
            ]
            
            for pattern, command_type in memory_patterns:
                if pattern in message_lower:
                    # Extrair conteúdo após o comando
                    content = message_lower.split(pattern, 1)[1].strip()
                    
                    if content:
                        # Salvar como fato
                        fact_id = self.save_user_fact_isolated(user_id, content, command_type)
                        
                        # Retornar mensagem processada e flag de sucesso
                        processed_message = f"Informação salva na memória: {content}"
                        logger.info(f"[ISOLATED_MEMORY] Comando processado - Fact ID: {fact_id}")
                        
                        return processed_message, True
            
            # Nenhum comando detectado
            return message, False
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao processar comando: {e}")
            return message, False
    
    def _create_new_user_profile(self, user_id: str) -> Dict:
        """Criar novo perfil de usuário"""
        try:
            profile_id = str(uuid.uuid4())
            current_time = datetime.utcnow().isoformat()
            
            initial_profile = {
                "user_id": user_id,
                "created_at": current_time,
                "preferences": {},
                "extracted_info": {}
            }
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO memory_user_profiles
                    (id, user_id, profile_json, version, created_at, updated_at, last_interaction)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile_id, user_id, json.dumps(initial_profile),
                    1, current_time, current_time, current_time
                ))
                
                conn.commit()
                
            logger.info(f"[ISOLATED_MEMORY] Novo perfil criado - User: {user_id}")
            
            return {
                "user_id": user_id,
                "profile_data": initial_profile,
                "version": 1,
                "created_at": current_time,
                "updated_at": current_time,
                "last_interaction": current_time
            }
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao criar perfil: {e}")
            raise e
    
    def _auto_update_user_profile(self, user_id: str, user_message: str, assistant_response: str):
        """Atualizar automaticamente o perfil com base na conversa"""
        try:
            # Extrair informações básicas da mensagem
            extracted_info = self._extract_user_info(user_message)
            
            if extracted_info:
                logger.info(f"[ISOLATED_MEMORY] Auto-atualizando perfil - User: {user_id}")
                self.update_user_profile_isolated(user_id, extracted_info)
                
        except Exception as e:
            logger.warning(f"[ISOLATED_MEMORY] Erro na auto-atualização do perfil: {e}")
    
    def _extract_user_info(self, message: str) -> Dict:
        """Extrair informações do usuário da mensagem"""
        import re
        
        extracted = {}
        message_lower = message.lower()
        
        # Padrões para nome
        name_patterns = [
            r"meu nome é ([a-záàâãéêíóôõúç]+)",
            r"me chamo ([a-záàâãéêíóôõúç]+)",
            r"sou o ([a-záàâãéêíóôõúç]+)",
            r"sou a ([a-záàâãéêíóôõúç]+)",
            r"eu sou ([a-záàâãéêíóôõúç]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).title()
                if len(name) > 1:
                    extracted["name"] = name
                    break
        
        # Padrões para idade
        age_patterns = [
            r"tenho (\d+) anos",
            r"eu tenho (\d+) anos",
            r"minha idade é (\d+)",
            r"(\d+) anos de idade"
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, message_lower)
            if match:
                age = int(match.group(1))
                if 1 <= age <= 120:
                    extracted["age"] = age
                    break
        
        return extracted
    
    def clear_user_memory_isolated(self, user_id: str) -> bool:
        """Limpar toda a memória de um usuário no sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Limpando memória completa - User: {user_id}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Contar registros antes da limpeza
                cursor.execute("SELECT COUNT(*) FROM memory_conversations WHERE user_id = ?", (user_id,))
                conv_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM memory_user_facts WHERE user_id = ?", (user_id,))
                facts_count = cursor.fetchone()[0]
                
                # Limpar todas as tabelas
                cursor.execute("DELETE FROM memory_conversations WHERE user_id = ?", (user_id,))
                cursor.execute("DELETE FROM memory_user_profiles WHERE user_id = ?", (user_id,))
                cursor.execute("DELETE FROM memory_user_facts WHERE user_id = ?", (user_id,))
                cursor.execute("DELETE FROM memory_session_context WHERE user_id = ?", (user_id,))
                
                conn.commit()
                
            logger.info(f"[ISOLATED_MEMORY] Memória limpa - User: {user_id}, "
                       f"Conversas: {conv_count}, Fatos: {facts_count}")
            
            return True
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao limpar memória: {e}")
            return False
    
    def get_memory_stats_isolated(self, user_id: str) -> Dict:
        """Obter estatísticas da memória do usuário no sistema isolado"""
        try:
            logger.info(f"[ISOLATED_MEMORY] Obtendo estatísticas - User: {user_id}")
            
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Contar conversas
                cursor.execute("SELECT COUNT(*) FROM memory_conversations WHERE user_id = ?", (user_id,))
                conv_count = cursor.fetchone()[0]
                
                # Contar fatos
                cursor.execute("SELECT COUNT(*) FROM memory_user_facts WHERE user_id = ? AND is_active = 1", (user_id,))
                facts_count = cursor.fetchone()[0]
                
                # Verificar se tem perfil
                cursor.execute("SELECT COUNT(*) FROM memory_user_profiles WHERE user_id = ?", (user_id,))
                has_profile = cursor.fetchone()[0] > 0
                
                # Última interação
                cursor.execute("""
                    SELECT MAX(timestamp) FROM memory_conversations WHERE user_id = ?
                """, (user_id,))
                last_interaction = cursor.fetchone()[0]
                
            stats = {
                "user_id": user_id,
                "total_conversations": conv_count,
                "total_facts": facts_count,
                "has_profile": has_profile,
                "last_interaction": last_interaction,
                "system": "isolated_memory_v1"
            }
            
            logger.info(f"[ISOLATED_MEMORY] Estatísticas: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"[ISOLATED_MEMORY] Erro ao obter estatísticas: {e}")
            return {"error": str(e)}

