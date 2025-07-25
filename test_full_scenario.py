#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.chats.services.gemini_chat_service import GeminiChatService

def test_full_scenario():
    print("=== Teste Completo do Cenário do Usuário ===")
    
    try:
        # Inicializar o serviço
        gemini_service = GeminiChatService()
        print("✅ GeminiChatService inicializado com sucesso")
        
        user_id = "1"
        session_id = ""  # Mesmo que no teste do usuário
        
        # Primeira mensagem: "lembre-se disso: Meu nome é Cledson"
        print("\n1. Primeira mensagem com 'lembre-se disso':")
        message1 = "lembre-se disso: Meu nome é Cledson"
        print(f"Enviando: {message1}")
        
        response1 = gemini_service.process_message(message1, user_id, session_id)
        print(f"Resposta: {response1['message']}")
        print(f"Fato salvo: {response1.get('fact_saved', False)}")
        
        # Segunda mensagem: "qual meu nome ?"
        print("\n2. Segunda mensagem perguntando o nome:")
        message2 = "qual meu nome ?"
        print(f"Enviando: {message2}")
        
        response2 = gemini_service.process_message(message2, user_id, session_id)
        print(f"Resposta: {response2['message']}")
        
        # Verificar se o nome foi lembrado
        if "cledson" in response2['message'].lower():
            print("✅ SUCESSO: O assistente lembrou do nome!")
        else:
            print("❌ FALHA: O assistente não lembrou do nome.")
            
        # Verificar perfil do usuário diretamente
        print("\n3. Verificando perfil do usuário:")
        profile = gemini_service.memory_service.get_user_profile(user_id)
        print(f"Perfil completo: {profile}")
        
        facts = gemini_service.memory_service.get_user_facts(user_id)
        print(f"Fatos salvos: {facts}")
        
        context = gemini_service.memory_service.get_user_context_for_chat(user_id)
        print(f"Contexto gerado: {context}")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_scenario()
