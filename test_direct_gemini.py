#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.chats.services.gemini_chat_service import GeminiChatService

def test_gemini_direct():
    print("=== Teste Direto do GeminiChatService ===")
    
    try:
        # Inicializar o serviço
        gemini_service = GeminiChatService()
        print("✅ GeminiChatService inicializado com sucesso")
        
        # Testar processamento de mensagem
        user_id = "test_user_direct"
        session_id = "test_session_direct"
        message = "Olá, qual é o meu nome?"
        
        print(f"Processando mensagem: {message}")
        response = gemini_service.process_message(message, user_id, session_id)
        
        print("✅ Mensagem processada com sucesso")
        print(f"Resposta: {response}")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_direct()
