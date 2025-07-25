from dotenv import load_dotenv
load_dotenv()
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
from contextlib import contextmanager
from app.config.settings import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        logger.info(f"Cledson - Inicializando MemoryService com database path: {self.db_path}")
        
        # Garantir que o diretório do banco existe
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"Diretório criado: {db_dir}")
        
        self._init_sqlite_tables()
        logger.info("MemoryService inicializado com sucesso")
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexões com SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row # Para retornar resultados como dicionários
            logger.debug(f"Conexão SQLite estabelecida: {self.db_path}")
            yield conn
        except Exception as e:
            logger.error(f"Erro na conexão SQLite: {e}")
            if conn:
                conn.rollback()
                logger.debug("Rollback executado devido ao erro")
            raise e
        finally:
            if conn:
                conn.close()
                logger.debug("Conexão SQLite fechada")
    
    def _init_sqlite_tables(self):
        """Inicializar tabelas do SQLite"""
        try:
            logger.info("Inicializando tabelas do SQLite...")
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
                logger.debug("Tabela 'conversations' criada/verificada")
                
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
                logger.debug("Tabela 'user_profiles' criada/verificada")
                
                conn.commit()
                cur.close()
                logger.info("Tabelas SQLite inicializadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar tabelas SQLite: {e}")
            raise e
    
    def save_conversation(self, user_id: str, session_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar conversa no SQLite"""
        try:
            logger.info(f"Salvando conversa - User: {user_id}, Session: {session_id}")
            logger.debug(f"Message length: {len(message)}, Response length: {len(response)}")
            
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
                
            logger.info(f"Conversa salva com sucesso - User: {user_id}, Session: {session_id}")
            if metadata:
                logger.debug(f"Metadata salva: {metadata}")
                
        except Exception as e:
            logger.error(f"Erro ao salvar conversa - User: {user_id}, Session: {session_id}, Error: {str(e)}")
            raise Exception(f"Erro ao salvar conversa: {str(e)}")
    
    def get_conversation_history(self, user_id: str, session_id: str, limit: int = 10) -> List[Dict]:
        """Recuperar histórico de conversas do SQLite"""
        try:
            logger.info(f"Recuperando histórico - User: {user_id}, Session: {session_id}, Limit: {limit}")
            
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
                
                logger.info(f"Histórico recuperado - {len(results)} registros encontrados")
                
                # Converter resultados para dicionários e parsear metadata
                parsed_results = []
                for row in results:
                    row_dict = dict(row)
                    if row_dict.get("metadata"):
                        try:
                            row_dict["metadata"] = json.loads(row_dict["metadata"])
                        except json.JSONDecodeError:
                            logger.warning(f"Erro ao parsear metadata para conversa - User: {user_id}")
                            row_dict["metadata"] = {}
                    parsed_results.append(row_dict)
                
                logger.debug(f"Histórico processado com sucesso - {len(parsed_results)} registros")
                return parsed_results
                
        except Exception as e:
            logger.error(f"Erro ao recuperar histórico - User: {user_id}, Session: {session_id}, Error: {str(e)}")
            raise Exception(f"Erro ao recuperar histórico: {str(e)}")
    
    def clear_user_memory(self, user_id: str):
        """Limpar toda a memória de um usuário"""
        try:
            logger.info(f"Limpando toda a memória do usuário: {user_id}")
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (user_id,))
                count_before = cur.fetchone()[0]
                
                cur.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
                conn.commit()
                cur.close()
                
            logger.info(f"Memória limpa - User: {user_id}, {count_before} conversas removidas")
            
        except Exception as e:
            logger.error(f"Erro ao limpar memória do usuário: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao limpar memória do usuário: {str(e)}")
    
    def clear_conversation_history(self, user_id: str, session_id: str):
        """Limpar histórico de conversa específico de uma sessão"""
        try:
            logger.info(f"Limpando histórico de sessão - User: {user_id}, Session: {session_id}")
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ? AND session_id = ?", (user_id, session_id))
                count_before = cur.fetchone()[0]
                
                cur.execute("DELETE FROM conversations WHERE user_id = ? AND session_id = ?", (user_id, session_id))
                conn.commit()
                cur.close()
                
            logger.info(f"Histórico de sessão limpo - User: {user_id}, Session: {session_id}, {count_before} conversas removidas")
            
        except Exception as e:
            logger.error(f"Erro ao limpar histórico de conversa - User: {user_id}, Session: {session_id}, Error: {str(e)}")
            raise Exception(f"Erro ao limpar histórico de conversa: {str(e)}")

    def get_memory_stats(self, user_id: str) -> Dict:
        """Obter estatísticas da memória do usuário"""
        try:
            logger.info(f"Obtendo estatísticas de memória - User: {user_id}")
            
            stats = {
                "total_conversations": 0
            }
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (user_id,))
                stats["total_conversations"] = cur.fetchone()[0]
                cur.close()
                
            logger.info(f"Estatísticas obtidas - User: {user_id}, Total conversas: {stats['total_conversations']}")
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas - User: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao obter estatísticas: {str(e)}")
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Recuperar perfil global do usuário"""
        try:
            logger.info(f"Recuperando perfil do usuário: {user_id}")
            
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
                    logger.info(f"Perfil encontrado - User: {user_id}, Items no perfil: {len(profile_data)}")
                    return {
                        "profile_data": profile_data,
                        "created_at": result['created_at'],
                        "updated_at": result['updated_at']
                    }
                else:
                    logger.info(f"Perfil não encontrado - User: {user_id}, retornando perfil vazio")
                    # Retornar perfil vazio se não existir
                    return {
                        "profile_data": {},
                        "created_at": None,
                        "updated_at": None
                    }
                    
        except Exception as e:
            logger.error(f"Erro ao recuperar perfil do usuário: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao recuperar perfil do usuário: {str(e)}")
    
    def update_user_profile(self, user_id: str, profile_updates: Dict):
        """Atualizar perfil global do usuário"""
        try:
            logger.info(f"Atualizando perfil do usuário: {user_id}")
            logger.debug(f"Updates a serem aplicados: {profile_updates}")
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Primeiro, tentar recuperar o perfil existente
                current_profile = self.get_user_profile(user_id)
                
                # Mesclar os dados existentes com as atualizações
                merged_profile = current_profile["profile_data"].copy()
                merged_profile.update(profile_updates)
                
                logger.debug(f"Perfil mesclado: {merged_profile}")
                
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
                
            logger.info(f"Perfil atualizado com sucesso - User: {user_id}")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil do usuário: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao atualizar perfil do usuário: {str(e)}")
    
    def extract_user_info_from_message(self, message: str, response: str) -> Dict:
        """Extrair informações do usuário de uma mensagem (método simples)"""
        logger.debug(f"Extraindo informações do usuário da mensagem: {message[:50]}...")
        
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
                        logger.info(f"Nome extraído da mensagem: {name.title()}")
                        break
        
        # Detectar outras informações úteis
        if "trabalho como" in message_lower or "sou um" in message_lower or "sou uma" in message_lower:
            extracted_info["mentioned_profession"] = True
            logger.debug("Profissão mencionada na mensagem")
        
        if "anos" in message_lower and any(char.isdigit() for char in message):
            extracted_info["mentioned_age"] = True
            logger.debug("Idade mencionada na mensagem")
        
        if extracted_info:
            logger.info(f"Informações extraídas: {extracted_info}")
        else:
            logger.debug("Nenhuma informação específica extraída da mensagem")
        
        return extracted_info
    
    def save_message_with_profile_update(self, user_id: str, session_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar mensagem e atualizar perfil do usuário automaticamente"""
        try:
            logger.info(f"Salvando mensagem com atualização de perfil - User: {user_id}, Session: {session_id}")
            
            # Salvar a mensagem normalmente
            self.save_conversation(user_id, session_id, message, response, metadata)
            
            # Extrair informações do usuário da mensagem
            extracted_info = self.extract_user_info_from_message(message, response)
            
            # Se encontrou informações, atualizar o perfil
            if extracted_info:
                logger.info(f"Atualizando perfil com informações extraídas: {extracted_info}")
                self.update_user_profile(user_id, extracted_info)
            else:
                logger.debug("Nenhuma informação de perfil para atualizar")
                
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem com atualização de perfil - User: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao salvar mensagem com atualização de perfil: {str(e)}")
    
    def get_user_context_for_chat(self, user_id: str) -> str:
        """Obter contexto do usuário para incluir no chat"""
        try:
            logger.debug(f"Obtendo contexto do usuário para chat: {user_id}")
            
            profile = self.get_user_profile(user_id)
            profile_data = profile["profile_data"]
            
            if not profile_data:
                logger.debug(f"Nenhum contexto disponível para usuário: {user_id}")
                return ""
            
            context_parts = []
            
            if "name" in profile_data:
                context_parts.append(f"O nome do usuário é {profile_data['name']}")
                logger.debug(f"Contexto: nome do usuário = {profile_data['name']}")
            
            if "mentioned_profession" in profile_data:
                context_parts.append("O usuário mencionou sua profissão anteriormente")
                logger.debug("Contexto: profissão mencionada")
            
            if "mentioned_age" in profile_data:
                context_parts.append("O usuário mencionou sua idade anteriormente")
                logger.debug("Contexto: idade mencionada")
            
            # Adicionar fatos específicos salvos pelo usuário
            if "user_facts" in profile_data and profile_data["user_facts"]:
                facts_text = "; ".join(profile_data["user_facts"])
                context_parts.append(f"Fatos importantes sobre o usuário: {facts_text}")
                logger.debug(f"Contexto: {len(profile_data['user_facts'])} fatos do usuário")
            
            if context_parts:
                context = "Informações sobre o usuário: " + "; ".join(context_parts) + "."
                logger.info(f"Contexto gerado para usuário {user_id}: {len(context)} caracteres")
                return context
            
            return ""
            
        except Exception as e:
            logger.error(f"Erro ao obter contexto do usuário: {user_id}, Error: {str(e)}")
            # Se houver erro, retornar string vazia para não quebrar o chat
            return ""
    
    def save_user_fact(self, user_id: str, fact: str):
        """Salvar um fato específico sobre o usuário"""
        try:
            logger.info(f"Salvando fato do usuário: {user_id}")
            logger.debug(f"Fato a ser salvo: {fact}")
            
            # Recuperar perfil atual
            profile = self.get_user_profile(user_id)
            profile_data = profile["profile_data"].copy()
            
            # Inicializar lista de fatos se não existir
            if "user_facts" not in profile_data:
                profile_data["user_facts"] = []
                logger.debug("Lista de fatos inicializada")
            
            # Adicionar o novo fato (evitar duplicatas)
            if fact not in profile_data["user_facts"]:
                profile_data["user_facts"].append(fact)
                logger.info(f"Fato adicionado - Total de fatos: {len(profile_data['user_facts'])}")
                
                # Limitar a 10 fatos para evitar contexto muito longo
                if len(profile_data["user_facts"]) > 10:
                    removed_facts = profile_data["user_facts"][:-10]
                    profile_data["user_facts"] = profile_data["user_facts"][-10:]
                    logger.info(f"Lista de fatos limitada a 10 - {len(removed_facts)} fatos antigos removidos")
                
                # Atualizar perfil
                self.update_user_profile(user_id, profile_data)
                logger.info(f"Fato salvo com sucesso - User: {user_id}")
            else:
                logger.info(f"Fato já existe, não foi duplicado - User: {user_id}")
                
        except Exception as e:
            logger.error(f"Erro ao salvar fato do usuário: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao salvar fato do usuário: {str(e)}")
    
    def detect_and_save_user_fact(self, user_message: str, user_id: str) -> tuple[str, bool]:
        """Detectar se o usuário quer salvar um fato e extraí-lo"""
        try:
            logger.debug(f"Detectando fatos na mensagem do usuário: {user_id}")
            
            # Palavras-chave que indicam que o usuário quer salvar algo
            trigger_phrases = [
                "lembre-se disso:",
                "lembre se disso:",
                "salvar para depois:",
                "minha memória:",
                "lembrar:",
                "não esqueça:",
                "importante:",
                "anotar:"
            ]
            
            message_lower = user_message.lower()
            
            for phrase in trigger_phrases:
                if phrase in message_lower:
                    logger.info(f"Frase-gatilho detectada: '{phrase}' - User: {user_id}")
                    
                    # Encontrar o índice onde começa o fato
                    start_index = message_lower.find(phrase) + len(phrase)
                    
                    # Extrair o fato (tudo que vem depois da frase-gatilho)
                    fact = user_message[start_index:].strip()
                    
                    if fact:  # Se há conteúdo para salvar
                        logger.info(f"Fato extraído: '{fact}' - User: {user_id}")
                        
                        # Salvar o fato
                        self.save_user_fact(user_id, fact)
                        
                        # Remover a instrução da mensagem original
                        cleaned_message = user_message[:message_lower.find(phrase)].strip()
                        if not cleaned_message:
                            cleaned_message = f"Entendi! Vou lembrar que {fact}"
                        
                        logger.info(f"Mensagem processada e fato salvo - User: {user_id}")
                        return cleaned_message, True
            
            logger.debug(f"Nenhuma frase-gatilho detectada - User: {user_id}")
            return user_message, False
            
        except Exception as e:
            logger.error(f"Erro ao detectar e salvar fato do usuário: {user_id}, Error: {str(e)}")
            # Em caso de erro, retornar mensagem original
            return user_message, False
    
    def get_user_facts(self, user_id: str) -> list:
        """Recuperar todos os fatos salvos sobre o usuário"""
        try:
            logger.info(f"Recuperando fatos do usuário: {user_id}")
            
            profile = self.get_user_profile(user_id)
            profile_data = profile["profile_data"]
            
            facts = profile_data.get("user_facts", [])
            logger.info(f"Fatos recuperados - User: {user_id}, Total: {len(facts)}")
            
            return facts
            
        except Exception as e:
            logger.error(f"Erro ao recuperar fatos do usuário: {user_id}, Error: {str(e)}")
            return []
    
    def remove_user_fact(self, user_id: str, fact_index: int) -> bool:
        """Remover um fato específico do usuário pelo índice"""
        try:
            logger.info(f"Removendo fato do usuário: {user_id}, Índice: {fact_index}")
            
            profile = self.get_user_profile(user_id)
            profile_data = profile["profile_data"].copy()
            
            if "user_facts" in profile_data and 0 <= fact_index < len(profile_data["user_facts"]):
                removed_fact = profile_data["user_facts"].pop(fact_index)
                self.update_user_profile(user_id, profile_data)
                
                logger.info(f"Fato removido com sucesso - User: {user_id}, Fato: '{removed_fact}'")
                return True
            else:
                logger.warning(f"Índice inválido para remoção de fato - User: {user_id}, Índice: {fact_index}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao remover fato do usuário: {user_id}, Índice: {fact_index}, Error: {str(e)}")
            return False
