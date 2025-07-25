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
        logger.info(f"Inicializando MemoryService com database path: {self.db_path}")
        
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
            logger.info(f"CONTEÚDO SALVO - MESSAGE: '{message[:100]}{'...' if len(message) > 100 else ''}'")
            logger.info(f"CONTEÚDO SALVO - RESPONSE: '{response[:100]}{'...' if len(response) > 100 else ''}'")
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
                conversation_id = cur.lastrowid
                conn.commit()
                cur.close()
                
            logger.info(f"Conversa salva com sucesso - ID: {conversation_id}, User: {user_id}, Session: {session_id}")
            if metadata:
                logger.info(f"METADATA SALVA: {metadata}")
                
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
            logger.info(f"PROFILE UPDATES RECEBIDOS: {profile_updates}")
            
            with self._get_connection() as conn:
                cur = conn.cursor()
                
                # Primeiro, tentar recuperar o perfil existente DENTRO DA MESMA CONEXÃO
                cur.execute("""
                    SELECT profile_data
                    FROM user_profiles
                    WHERE user_id = ?
                """, (user_id,))
                
                result = cur.fetchone()
                
                current_profile_data = {}
                if result:
                    current_profile_data = json.loads(result['profile_data'])
                    logger.info(f"PERFIL ATUAL: {current_profile_data}")
                else:
                    logger.info(f"Perfil não encontrado para mesclagem - User: {user_id}, iniciando com perfil vazio")
                
                # Mesclar os dados existentes com as atualizações
                merged_profile = current_profile_data.copy()
                merged_profile.update(profile_updates)
                
                logger.info(f"PERFIL FINAL SALVO: {merged_profile}")
                
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
        
        import re
        # Padrões para detectar nome
        name_patterns = [
            r"meu nome é ([\wÀ-ú]+)",
            r"me chamo ([\wÀ-ú]+)",
            r"sou o ([\wÀ-ú]+)",
            r"sou a ([\wÀ-ú]+)",
            r"eu sou ([\wÀ-ú]+)",
            r"meu nome eh ([\wÀ-ú]+)",
            r"me chamo de ([\wÀ-ú]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).title()
                if name and len(name) > 1:
                    extracted_info["name"] = name
                    logger.info(f"Nome extraído da mensagem: {name}")
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
            logger.info(f"Informações extraídas pela função: {extracted_info}")
            
            # Se encontrou informações, atualizar o perfil
            if extracted_info:
                logger.info(f"Atualizando perfil com informações extraídas: {extracted_info}")
                self.update_user_profile(user_id, extracted_info)
            else:
                logger.info(f"Nenhuma informação extraída. Criando/Atualizando perfil vazio para o usuário: {user_id}")
                self.update_user_profile(user_id, {})
                
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem com atualização de perfil - User: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao salvar mensagem com atualização de perfil: {str(e)}")
    
    def get_user_context_for_chat(self, user_id: str) -> str:
        """Obter contexto do usuário para o chat, incluindo histórico e perfil"""
        try:
            logger.info(f"Obtendo contexto do usuário para chat - User: {user_id}")
            
            context_parts = []
            
            # 1. Adicionar informações do perfil do usuário
            user_profile = self.get_user_profile(user_id)
            if user_profile and user_profile["profile_data"]:
                profile_str = json.dumps(user_profile["profile_data"], ensure_ascii=False)
                context_parts.append(f"Informações do perfil do usuário: {profile_str}")
                logger.info(f"Perfil do usuário adicionado ao contexto: {profile_str}")
            else:
                logger.info("Nenhum perfil de usuário encontrado para adicionar ao contexto.")
            
            # 2. Adicionar histórico de conversas recentes (se houver)
            # O session_id aqui pode precisar ser dinâmico, dependendo de como você gerencia as sessões.
            # Por enquanto, vamos assumir que o contexto é para a sessão atual ou mais recente.
            # Para um contexto mais robusto, você pode precisar passar o session_id para esta função.
            # Por simplicidade, vamos pegar as últimas N conversas do usuário, independente da sessão.
            
            # Modificação: Para pegar o histórico de conversas, precisamos de um session_id.
            # Se o objetivo é um contexto geral do usuário, talvez seja melhor pegar as últimas conversas
            # independente da sessão, ou a última sessão ativa. Por enquanto, vamos deixar como está
            # e considerar que o `session_id` será passado ou inferido em um nível superior.
            
            # Vamos adicionar um placeholder para o histórico de conversas, pois a função get_conversation_history
            # requer um session_id. Para um contexto geral, talvez seja necessário uma nova função
            # que recupere as últimas conversas de todas as sessões ou da sessão mais recente.
            # Por enquanto, vamos focar no perfil do usuário.
            
            # Exemplo de como poderia ser se tivéssemos um session_id aqui:
            # conversation_history = self.get_conversation_history(user_id, session_id, limit=5)
            # if conversation_history:
            #     history_str = "Histórico de conversas recentes:\n"
            #     for entry in conversation_history:
            #         history_str += f"Usuário: {entry['message']}\n"
            #         history_str += f"Assistente: {entry['response']}\n"
            #     context_parts.append(history_str)
            #     logger.info("Histórico de conversas adicionado ao contexto.")
            
            full_context = "\n".join(context_parts)
            logger.info(f"Contexto final do usuário para chat: {full_context[:200]}...")
            return full_context
            
        except Exception as e:
            logger.error(f"Erro ao obter contexto do usuário para chat: {user_id}, Error: {str(e)}")
            raise Exception(f"Erro ao obter contexto do usuário para chat: {str(e)}")



    
    def detect_and_save_user_fact(self, message: str, user_id: str) -> tuple[str, bool]:
        """Detectar comando 'Lembre-se disso' e salvar informação do usuário"""
        try:
            logger.info(f"Detectando comando de memória na mensagem - User: {user_id}")
            
            # Detectar comando "Lembre-se disso" ou variações
            remember_patterns = [
                "lembre-se disso",
                "lembre disso",
                "salve isso",
                "guarde isso",
                "memorize isso",
                "anote isso"
            ]
            
            message_lower = message.lower()
            fact_saved = False
            processed_message = message
            
            for pattern in remember_patterns:
                if pattern in message_lower:
                    # Extrair a informação a ser lembrada
                    # Remove o comando da mensagem
                    fact_to_save = message_lower.replace(pattern, "").strip()
                    
                    if fact_to_save:
                        # Salvar como fato do usuário no perfil
                        timestamp = datetime.utcnow().isoformat()
                        fact_key = f"user_fact_{timestamp}"
                        
                        fact_data = {
                            fact_key: {
                                "content": fact_to_save,
                                "saved_at": timestamp,
                                "type": "user_fact"
                            }
                        }
                        
                        self.update_user_profile(user_id, fact_data)
                        fact_saved = True
                        
                        # Modificar a mensagem para não incluir o comando
                        processed_message = fact_to_save
                        
                        logger.info(f"Fato do usuário salvo - User: {user_id}, Fact: {fact_to_save}")
                    break
            
            return processed_message, fact_saved
            
        except Exception as e:
            logger.error(f"Erro ao detectar e salvar fato do usuário - User: {user_id}, Error: {str(e)}")
            return message, False
    
    def get_user_facts(self, user_id: str) -> List[Dict]:
        """Recuperar fatos salvos do usuário"""
        try:
            logger.info(f"Recuperando fatos do usuário: {user_id}")
            
            user_profile = self.get_user_profile(user_id)
            facts = []
            
            if user_profile and user_profile["profile_data"]:
                profile_data = user_profile["profile_data"]
                
                for key, value in profile_data.items():
                    if key.startswith("user_fact_") and isinstance(value, dict):
                        facts.append({
                            "id": key,
                            "content": value.get("content", ""),
                            "saved_at": value.get("saved_at", ""),
                            "type": value.get("type", "user_fact")
                        })
            
            logger.info(f"Fatos recuperados - User: {user_id}, Total: {len(facts)}")
            return facts
            
        except Exception as e:
            logger.error(f"Erro ao recuperar fatos do usuário - User: {user_id}, Error: {str(e)}")
            return []
    
    def delete_user_fact(self, user_id: str, fact_id: str) -> bool:
        """Deletar um fato específico do usuário"""
        try:
            logger.info(f"Deletando fato do usuário - User: {user_id}, Fact ID: {fact_id}")
            
            user_profile = self.get_user_profile(user_id)
            
            if user_profile and user_profile["profile_data"]:
                profile_data = user_profile["profile_data"].copy()
                
                if fact_id in profile_data:
                    del profile_data[fact_id]
                    
                    # Atualizar o perfil sem o fato deletado
                    with self._get_connection() as conn:
                        cur = conn.cursor()
                        cur.execute("""
                            UPDATE user_profiles 
                            SET profile_data = ?, updated_at = ?
                            WHERE user_id = ?
                        """, (
                            json.dumps(profile_data),
                            datetime.utcnow().isoformat(),
                            user_id
                        ))
                        conn.commit()
                        cur.close()
                    
                    logger.info(f"Fato deletado com sucesso - User: {user_id}, Fact ID: {fact_id}")
                    return True
                else:
                    logger.warning(f"Fato não encontrado - User: {user_id}, Fact ID: {fact_id}")
                    return False
            else:
                logger.warning(f"Perfil não encontrado para deletar fato - User: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao deletar fato do usuário - User: {user_id}, Fact ID: {fact_id}, Error: {str(e)}")
            return False

