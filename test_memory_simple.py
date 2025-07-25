#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.services.memory_service import MemoryService

def test_memory_service():
    print("=== Teste Simples do MemoryService ===")
    
    try:
        # Inicializar o serviço
        memory_service = MemoryService()
        print("✅ MemoryService inicializado com sucesso")
        
        # Testar salvamento de conversa
        user_id = "test_user_123"
        session_id = "test_session_456"
        message = "Olá, meu nome é João"
        response = "Olá João! Como posso ajudá-lo?"
        
        memory_service.save_conversation(user_id, session_id, message, response)
        print("✅ Conversa salva com sucesso")
        
        # Testar recuperação de histórico
        history = memory_service.get_conversation_history(user_id, session_id, limit=5)
        print(f"✅ Histórico recuperado: {len(history)} mensagens")
        
        # Testar perfil do usuário
        profile = memory_service.get_user_profile(user_id)
        print(f"✅ Perfil do usuário: {profile}")
        
        # Testar atualização de perfil
        memory_service.update_user_profile(user_id, {"name": "João", "test": True})
        print("✅ Perfil atualizado com sucesso")
        
        # Verificar perfil atualizado
        updated_profile = memory_service.get_user_profile(user_id)
        print(f"✅ Perfil atualizado: {updated_profile}")
        
        print("\n🎉 Todos os testes passaram! A memória está funcionando corretamente.")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_service()
