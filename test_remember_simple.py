#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.services.memory_service import MemoryService

def test_remember_functionality():
    print("=== Teste da Funcionalidade 'Lembre-se disso' ===")
    
    try:
        memory_service = MemoryService()
        user_id = "test_user_remember"
        
        # Testar detecção e salvamento de fato
        message = "lembre-se disso: eu gosto de café pela manhã"
        cleaned_message, fact_saved = memory_service.detect_and_save_user_fact(message, user_id)
        
        print(f"Mensagem original: {message}")
        print(f"Mensagem limpa: {cleaned_message}")
        print(f"Fato salvo: {fact_saved}")
        
        if fact_saved:
            print("✅ Funcionalidade 'lembre-se disso' detectou e salvou o fato")
        else:
            print("❌ Funcionalidade 'lembre-se disso' não funcionou")
        
        # Verificar fatos salvos
        facts = memory_service.get_user_facts(user_id)
        print(f"✅ Fatos salvos: {facts}")
        
        # Testar contexto do usuário
        context = memory_service.get_user_context_for_chat(user_id)
        print(f"✅ Contexto do usuário: {context}")
        
        print("\n🎉 Teste da funcionalidade 'lembre-se disso' concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_remember_functionality()
