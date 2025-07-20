import os
from dotenv import load_dotenv
from src.services.memory_service import MemoryService
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def test_memory_service():
    print("Iniciando teste do MemoryService...")
    
    # Certifique-se de que DATABASE_URL e OPENAI_API_KEY estão configuradas no .env
    # Exemplo: DB_PATH="./iara_flow.db"
    # OPENAI_API_KEY="sua_chave_openai"

    try:
        memory_service = MemoryService()
        print("MemoryService inicializado com sucesso.")

        user_id = "test_user_123"
        session_id = "test_session_456"

        # Limpar histórico para garantir um teste limpo
        memory_service.clear_conversation_history(user_id, session_id)
        print("Histórico de conversa limpo.")

        # Salvar algumas mensagens
        print("Salvando mensagens...")
        memory_service.save_message(user_id, session_id, "Olá, como você está?", "Estou bem, obrigado! Como posso ajudar?")
        memory_service.save_message(user_id, session_id, "Qual é a capital da França?", "A capital da França é Paris.")
        memory_service.save_message(user_id, session_id, "Conte-me uma piada.", "Por que o tomate não anda de bicicleta? Porque ele refoga!")
        print("Mensagens salvas.")

        # Recuperar histórico de conversa
        print("Recuperando histórico de conversa...")
        history = memory_service.get_conversation_history(user_id, session_id)
        print(f"Histórico recuperado: {history}")
        assert len(history) == 6  # 3 perguntas + 3 respostas
        assert isinstance(history[0], HumanMessage)
        assert isinstance(history[1], AIMessage)

        # Testar busca de similaridade de conversas
        print("Testando busca de conversas similares...")
        similar_conversations = memory_service.search_similar_conversations(user_id, "Me fale sobre cidades europeias")
        print(f"Conversas similares encontradas: {similar_conversations}")
        assert len(similar_conversations) > 0
        assert "Paris" in similar_conversations[0]["response"]

        # Testar memória de longo prazo (a avaliação é interna, então vamos verificar se algo foi salvo)
        print("Testando memória de longo prazo...")
        # Forçar uma entrada na memória de longo prazo para teste
        memory_service._save_to_long_term_memory(
            user_id=user_id,
            content="Este é um teste de memória de longo prazo sobre IA.",
            memory_type="teste",
            importance_score=0.9
        )
        print("Entrada de memória de longo prazo forçada.")

        relevant_memories = memory_service.get_relevant_long_term_memories(user_id, "inteligência artificial")
        print(f"Memórias de longo prazo relevantes: {relevant_memories}")
        assert len(relevant_memories) > 0
        assert "IA" in relevant_memories[0]["content"]

        print("Todos os testes do MemoryService concluídos com sucesso!")

    except Exception as e:
        print(f"Erro durante o teste do MemoryService: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_service()
