import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env na raiz do projeto
load_dotenv(dotenv_path="/home/ubuntu/iara-flow-bff/.env")

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, "/home/ubuntu/iara-flow-bff")

from src.services.memory_service import MemoryService

def run_test():
    print("\n--- Iniciando Teste do MemoryService com LangChain ---")
    
    # Inicializar o MemoryService
    try:
        memory_service = MemoryService()
        print("✅ MemoryService inicializado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao inicializar MemoryService: {e}")
        return

    user_id = "test_user_langchain"
    session_id = "test_session_langchain"
    
    # Limpar memória do usuário para garantir um teste limpo
    try:
        memory_service.clear_user_memory(user_id)
        print(f"✅ Memória do usuário {user_id} limpa com sucesso.")
    except Exception as e:
        print(f"⚠️  Erro ao limpar memória do usuário (pode ser ignorado se a memória estiver vazia): {e}")

    # 1. Salvar algumas conversas
    print("\n--- Salvando conversas ---")
    conversations_to_save = [
        ("Qual é a capital da França?", "A capital da França é Paris."),
        ("Qual é o seu nome?", "Eu sou um modelo de linguagem grande, treinado pelo Google."),
        ("Pode me falar sobre a Torre Eiffel?", "A Torre Eiffel é um monumento em Paris, França."),
        ("Qual a cor do céu?", "A cor do céu geralmente é azul durante o dia."),
        ("Lembre-se que gosto de café forte.", "Entendido, você gosta de café forte.")
    ]

    for msg, resp in conversations_to_save:
        try:
            memory_service.save_message(user_id, session_id, msg, resp)
            print(f"✅ Conversa salva: \'{msg}\' / \'{resp}\'")
        except Exception as e:
            print(f"❌ Erro ao salvar conversa \'{msg}\': {e}")

    # 2. Obter histórico de conversas
    print("\n--- Obtendo histórico de conversas ---")
    try:
        history = memory_service.get_conversation_history(user_id, session_id, limit=3)
        print(f"✅ Histórico de conversas para '{user_id}':")
        for h in history:
            print(f"  - Mensagem: {h['message']}, Resposta: {h['response']}")
    except Exception as e:
        print(f"❌ Erro ao obter histórico de conversas: {e}")

    # 3. Obter estatísticas da memória
    print("\n--- Obtendo estatísticas da memória ---")
    try:
        stats = memory_service.get_memory_stats(user_id)
        print(f"✅ Estatísticas da memória para '{user_id}':")
        print(f"  - Total de conversas: {stats['total_conversations']}")
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas da memória: {e}")

    print("\n--- Teste Concluído ---")

if __name__ == "__main__":
    run_test()

