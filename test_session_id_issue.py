#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.services.memory_service import MemoryService

def test_session_id_issue():
    print("=== Teste do Problema com session_id Vazio ===")
    
    try:
        memory_service = MemoryService()
        user_id = "1"
        
        # Testar com session_id vazio (como no teste do usuário)
        session_id_empty = ""
        print(f"Testando com session_id vazio: '{session_id_empty}'")
        
        # Salvar uma conversa
        memory_service.save_conversation(
            user_id=user_id,
            session_id=session_id_empty,
            message="Teste com session_id vazio",
            response="Resposta de teste"
        )
        print("✅ Conversa salva com session_id vazio")
        
        # Tentar recuperar histórico
        history = memory_service.get_conversation_history(user_id, session_id_empty, limit=10)
        print(f"Histórico recuperado: {len(history)} mensagens")
        
        # Testar com session_id None
        session_id_none = None
        print(f"\nTestando com session_id None: {session_id_none}")
        
        # Salvar uma conversa
        memory_service.save_conversation(
            user_id=user_id,
            session_id=session_id_none,
            message="Teste com session_id None",
            response="Resposta de teste None"
        )
        print("✅ Conversa salva com session_id None")
        
        # Tentar recuperar histórico
        history_none = memory_service.get_conversation_history(user_id, session_id_none, limit=10)
        print(f"Histórico recuperado: {len(history_none)} mensagens")
        
        # Verificar se as conversas estão sendo salvas separadamente
        print(f"\nConversas com session_id vazio: {len(history)}")
        print(f"Conversas com session_id None: {len(history_none)}")
        
        # Verificar diretamente no banco
        with memory_service._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id, session_id, message FROM conversations WHERE user_id = ? ORDER BY created_at", (user_id,))
            all_conversations = cur.fetchall()
            cur.close()
            
            print(f"\nTodas as conversas no banco para user_id '{user_id}':")
            for conv in all_conversations:
                print(f"  session_id: '{conv['session_id']}' | message: {conv['message']}")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_session_id_issue()
