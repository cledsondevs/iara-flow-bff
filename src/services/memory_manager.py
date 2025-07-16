from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
from langchain.tools import tool
import os

# Carregue as credenciais do Supabase do seu ambiente
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

# Modelo para criar os embeddings (vetores)
embeddings = OpenAIEmbeddings()

def get_long_term_memory_for_user(user_id: str):
    """Cria uma Vector Store conectada à tabela de um usuário específico."""
    vector_store = SupabaseVectorStore(
        client=supabase,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents", # Função padrão do pgvector
        # Filtra os vetores para retornar apenas os do usuário atual!
        filter={"user_id": user_id}
    )
    return vector_store

@tool
def remember(query: str, user_id: str) -> str:
    """Use isso para lembrar informações de conversas passadas ou dados que você aprendeu anteriormente."""
    memory_store = get_long_term_memory_for_user(user_id)
    # Busca os 3 pedaços de informação mais relevantes
    relevant_docs = memory_store.similarity_search(query, k=3)
    if relevant_docs:
        return "Informações relevantes encontradas: " + "\n".join([doc.page_content for doc in relevant_docs])
    else:
        return "Nenhuma informação relevante encontrada na memória de longo prazo."

@tool
def learn(information: str, user_id: str) -> str:
    """Use isso para salvar uma nova informação importante para uso futuro. A informação deve ser concisa e relevante."""
    memory_store = get_long_term_memory_for_user(user_id)
    # Adiciona a nova informação ao banco de dados vetorial
    memory_store.add_texts([information], metadatas=[{"user_id": user_id}])
    return "Informação aprendida com sucesso."


