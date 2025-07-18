import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


class MemoryService:
    def __init__(self):
        # Configuração do Chroma
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db",  # Diretório local para persistir os dados
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Coleções do Chroma
        self.short_term_collection = self._get_or_create_collection("short_term_memory")
        self.long_term_collection = self._get_or_create_collection("long_term_memory")
        
        # Configuração do OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base=os.getenv('OPENAI_API_BASE')
        )
        
        # Configuração do PostgreSQL (apenas para dados estruturados)
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'iara_flow'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
        
        # Inicializar tabelas do PostgreSQL
        self._init_postgres_tables()
    
    def _get_or_create_collection(self, name: str):
        """Obter ou criar uma coleção no Chroma"""
        try:
            return self.chroma_client.get_collection(name=name)
        except Exception:
            return self.chroma_client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}  # Usar distância de cosseno
            )
    
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
        """Inicializar tabelas do PostgreSQL (sem pgvector)"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    # Tabela para metadados de conversas (sem embeddings)
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
                    
                    # Tabela para metadados de memória de longo prazo (sem embeddings)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS long_term_memory (
                            id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) NOT NULL,
                            content TEXT NOT NULL,
                            memory_type VARCHAR(100) NOT NULL,
                            importance_score FLOAT DEFAULT 0.0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            metadata JSONB
                        )
                    """)
                    
                    # Índices para melhor performance
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
                        ON conversations(user_id)
                    """)
                    
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS idx_conversations_created_at 
                        ON conversations(created_at)
                    """)
                    
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS idx_long_term_memory_user_id 
                        ON long_term_memory(user_id)
                    """)
                    
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS idx_long_term_memory_importance 
                        ON long_term_memory(importance_score)
                    """)
                    
                    conn.commit()
                    
        except Exception as e:
            print(f"Erro ao inicializar tabelas: {e}")
    
    def save_conversation(self, user_id: str, message: str, response: str, metadata: Optional[Dict] = None):
        """Salvar conversa na memória de curto prazo usando Chroma"""
        try:
            # Criar texto combinado para embedding
            combined_text = f"Pergunta: {message}\nResposta: {response}"
            
            # Gerar embedding
            embedding = self.embeddings.embed_query(combined_text)
            
            # Criar ID único para o documento
            doc_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            
            # Preparar metadados
            doc_metadata = {
                "user_id": user_id,
                "message": message,
                "response": response,
                "created_at": datetime.utcnow().isoformat(),
                "type": "conversation"
            }
            if metadata:
                doc_metadata.update(metadata)
            
            # Salvar no Chroma
            self.short_term_collection.add(
                embeddings=[embedding],
                documents=[combined_text],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
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
            
            # Avaliar para memória de longo prazo
            self._evaluate_for_long_term_memory(user_id, message, response)
            
        except Exception as e:
            raise Exception(f"Erro ao salvar conversa: {str(e)}")
    
    def get_similar_conversations(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """Buscar conversas similares usando Chroma"""
        try:
            # Gerar embedding da query
            query_embedding = self.embeddings.embed_query(query)
            
            # Buscar no Chroma
            results = self.short_term_collection.query(
                query_embeddings=[query_embedding],
                n_results=limit * 2,  # Buscar mais para filtrar por user_id
                where={"user_id": user_id}
            )
            
            # Processar resultados
            conversations = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    if len(conversations) >= limit:
                        break
                    
                    conversations.append({
                        "message": metadata.get("message", ""),
                        "response": metadata.get("response", ""),
                        "metadata": metadata,
                        "created_at": metadata.get("created_at"),
                        "distance": distance
                    })
            
            return conversations
            
        except Exception as e:
            raise Exception(f"Erro ao buscar conversas similares: {str(e)}")
    
    def _evaluate_for_long_term_memory(self, user_id: str, message: str, response: str):
        """Avaliar se a conversa deve ser salva na memória de longo prazo"""
        try:
            # Critérios para memória de longo prazo
            keywords = ['importante', 'lembrar', 'preferência', 'configuração', 'projeto', 
                       'salvar', 'guardar', 'memorizar', 'não esquecer']
            
            combined_text = f"{message} {response}".lower()
            importance_score = sum(1 for keyword in keywords if keyword in combined_text)
            
            # Critérios adicionais
            if len(response) > 200:  # Respostas longas
                importance_score += 1
            
            if any(word in combined_text for word in ['como', 'tutorial', 'passo a passo']):
                importance_score += 1
            
            if importance_score > 0:
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
        """Salvar na memória de longo prazo usando Chroma"""
        try:
            # Gerar embedding
            embedding = self.embeddings.embed_query(content)
            
            # Criar ID único
            doc_id = f"ltm_{user_id}_{datetime.utcnow().timestamp()}"
            
            # Preparar metadados
            doc_metadata = {
                "user_id": user_id,
                "memory_type": memory_type,
                "importance_score": importance_score,
                "created_at": datetime.utcnow().isoformat(),
                "type": "long_term_memory"
            }
            if metadata:
                doc_metadata.update(metadata)
            
            # Salvar no Chroma
            self.long_term_collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            # Salvar metadados no PostgreSQL
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO long_term_memory 
                        (user_id, content, memory_type, importance_score, metadata)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        user_id, content, memory_type, importance_score,
                        json.dumps(metadata) if metadata else None
                    ))
                    conn.commit()
                    
        except Exception as e:
            print(f"Erro ao salvar na memória de longo prazo: {e}")
    
    def get_relevant_long_term_memories(self, user_id: str, query: str, limit: int = 3) -> List[Dict]:
        """Recuperar memórias de longo prazo relevantes usando Chroma"""
        try:
            # Gerar embedding da query
            query_embedding = self.embeddings.embed_query(query)
            
            # Buscar no Chroma
            results = self.long_term_collection.query(
                query_embeddings=[query_embedding],
                n_results=limit * 2,  # Buscar mais para filtrar por user_id
                where={"user_id": user_id}
            )
            
            # Processar resultados
            memories = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    if len(memories) >= limit:
                        break
                    
                    memories.append({
                        "content": doc,
                        "memory_type": metadata.get("memory_type", ""),
                        "importance_score": metadata.get("importance_score", 0.0),
                        "metadata": metadata,
                        "created_at": metadata.get("created_at"),
                        "distance": distance
                    })
            
            return memories
            
        except Exception as e:
            raise Exception(f"Erro ao recuperar memórias de longo prazo: {str(e)}")
    
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
            # Limpar do Chroma
            # Buscar todos os documentos do usuário
            short_term_results = self.short_term_collection.get(
                where={"user_id": user_id}
            )
            if short_term_results['ids']:
                self.short_term_collection.delete(ids=short_term_results['ids'])
            
            long_term_results = self.long_term_collection.get(
                where={"user_id": user_id}
            )
            if long_term_results['ids']:
                self.long_term_collection.delete(ids=long_term_results['ids'])
            
            # Limpar do PostgreSQL
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM conversations WHERE user_id = %s", (user_id,))
                    cur.execute("DELETE FROM long_term_memory WHERE user_id = %s", (user_id,))
                    conn.commit()
                    
        except Exception as e:
            raise Exception(f"Erro ao limpar memória do usuário: {str(e)}")
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """Obter estatísticas da memória do usuário"""
        try:
            stats = {
                "short_term_conversations": 0,
                "long_term_memories": 0,
                "total_conversations": 0
            }
            
            # Contar no Chroma
            short_term_results = self.short_term_collection.get(
                where={"user_id": user_id}
            )
            stats["short_term_conversations"] = len(short_term_results['ids']) if short_term_results['ids'] else 0
            
            long_term_results = self.long_term_collection.get(
                where={"user_id": user_id}
            )
            stats["long_term_memories"] = len(long_term_results['ids']) if long_term_results['ids'] else 0
            
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

