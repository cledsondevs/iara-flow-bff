import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.extensions
from pgvector.psycopg2 import register_vector

# Registrar o tipo vector globalmente para todas as novas conexões
# Isso garante que o tipo 'vector' seja reconhecido pelo psycopg2
# antes de qualquer operação que o utilize.
psycopg2.extensions.register_type(register_vector(None))

from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage

class MemoryService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL não configurada nas variáveis de ambiente.")
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self._create_tables()
    
    def _get_connection(self):
        """Obter conexão com o banco de dados"""
        conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        register_vector(conn)
        return conn
    
    def _create_tables(self):
        """Criar tabelas necessárias para memória"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                    conn.commit() # Commit explícito para a criação da extensão
                    # Tabela para conversas
    
    def save_message(self, user_id: str, session_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar mensagem e resposta na memória"""
        try:
            # Gerar embeddings
            message_embedding = self.embeddings.embed_query(message)
            response_embedding = self.embeddings.embed_query(response)
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO conversations 
                        (user_id, session_id, message, response, message_embedding, response_embedding, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        user_id, session_id, message, response,
                        message_embedding, response_embedding,
                        json.dumps(metadata) if metadata else None
                    ))
                    conn.commit()
                    
            # Verificar se deve salvar na memória de longo prazo
            self._evaluate_for_long_term_memory(user_id, message, response)
            
        except Exception as e:
            raise Exception(f"Erro ao salvar mensagem: {str(e)}")
    
    def get_conversation_history(self, user_id: str, session_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Recuperar histórico de conversa"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    if session_id:
                        cur.execute("""
                            SELECT message, response, metadata, created_at
                            FROM conversations
                            WHERE user_id = %s AND session_id = %s
                            ORDER BY created_at DESC
                            LIMIT %s
                        """, (user_id, session_id, limit))
                    else:
                        cur.execute("""
                            SELECT message, response, metadata, created_at
                            FROM conversations
                            WHERE user_id = %s
                            ORDER BY created_at DESC
                            LIMIT %s
                        """, (user_id, limit))
                    
                    rows = cur.fetchall()
                    
                    # Converter para formato LangChain
                    history = []
                    for row in reversed(rows):  # Reverter para ordem cronológica
                        history.append(HumanMessage(content=row['message']))
                        history.append(AIMessage(content=row['response']))
                    
                    return history
                    
        except Exception as e:
            raise Exception(f"Erro ao recuperar histórico: {str(e)}")
    
    def clear_conversation_history(self, user_id: str, session_id: Optional[str] = None):
        """Limpar histórico de conversa"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    if session_id:
                        cur.execute("""
                            DELETE FROM conversations
                            WHERE user_id = %s AND session_id = %s
                        """, (user_id, session_id))
                    else:
                        cur.execute("""
                            DELETE FROM conversations
                            WHERE user_id = %s
                        """, (user_id,))
                    
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao limpar histórico: {str(e)}")
    
    def search_similar_conversations(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """Buscar conversas similares usando embeddings"""
        try:
            query_embedding = self.embeddings.embed_query(query)
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT message, response, metadata, created_at,
                               (message_embedding <=> %s) as message_distance,
                               (response_embedding <=> %s) as response_distance
                        FROM conversations
                        WHERE user_id = %s
                        ORDER BY LEAST(message_embedding <=> %s, response_embedding <=> %s)
                        LIMIT %s
                    """, (query_embedding, query_embedding, user_id, query_embedding, query_embedding, limit))
                    
                    rows = cur.fetchall()
                    return [dict(row) for row in rows]
                    
        except Exception as e:
            raise Exception(f"Erro ao buscar conversas similares: {str(e)}")
    
    def _evaluate_for_long_term_memory(self, user_id: str, message: str, response: str):
        """Avaliar se a conversa deve ser salva na memória de longo prazo"""
        try:
            # Critérios simples para memória de longo prazo
            # Pode ser expandido com lógica mais sofisticada
            keywords = ['importante', 'lembrar', 'preferência', 'configuração', 'projeto']
            
            combined_text = f"{message} {response}".lower()
            importance_score = sum(1 for keyword in keywords if keyword in combined_text)
            
            if importance_score > 0 or len(response) > 200:  # Respostas longas podem ser importantes
                self._save_to_long_term_memory(
                    user_id=user_id,
                    content=f"Pergunta: {message}\nResposta: {response}",
                    memory_type="conversation",
                    importance_score=importance_score,
                    metadata={
                        "original_message": message,
                        "original_response": response,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
                
        except Exception as e:
            print(f"Erro ao avaliar para memória de longo prazo: {e}")
    
    def _save_to_long_term_memory(self, user_id: str, content: str, memory_type: str, 
                                 importance_score: float = 0.0, metadata: Optional[Dict] = None):
        """Salvar na memória de longo prazo"""
        try:
            content_embedding = self.embeddings.embed_query(content)
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO long_term_memory 
                        (user_id, content, content_embedding, memory_type, importance_score, metadata)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id, content, content_embedding, memory_type, importance_score,
                        json.dumps(metadata) if metadata else None
                    ))
                    conn.commit()
                    
        except Exception as e:
            print(f"Erro ao salvar na memória de longo prazo: {e}")
    
    def get_relevant_long_term_memories(self, user_id: str, query: str, limit: int = 3) -> List[Dict]:
        """Recuperar memórias de longo prazo relevantes"""
        try:
            query_embedding = self.embeddings.embed_query(query)
            
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT content, memory_type, importance_score, metadata, created_at,
                               (content_embedding <=> %s) as distance
                        FROM long_term_memory
                        WHERE user_id = %s
                        ORDER BY (content_embedding <=> %s), importance_score DESC
                        LIMIT %s
                    """, (query_embedding, user_id, query_embedding, limit))
                    
                    rows = cur.fetchall()
                    return [dict(row) for row in rows]
                    
        except Exception as e:
            raise Exception(f"Erro ao recuperar memórias de longo prazo: {str(e)}")

