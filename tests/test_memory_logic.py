#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

from app.services.memory_service import MemoryService

def test_memory_logic():
    print("=== Teste da Lógica de Memória (Sem API) ===")
    
    try:
        # Inicializar o serviço
        memory_service = MemoryService()
        print("✅ MemoryService inicializado com sucesso")
        
        user_id = "1"
        session_id = ""
        
        # Limpar dados anteriores
        memory_service.clear_user_memory(user_id)
        print("✅ Memória do usuário limpa")
        
        # Primeira mensagem: "lembre-se disso: Meu nome é Cledson"
        print("\n1. Processando 'lembre-se disso: Meu nome é Cledson':")
        message1 = "lembre-se disso: Meu nome é Cledson"
        
        processed_message, fact_saved = memory_service.detect_and_save_user_fact(message1, user_id)
        print(f"Mensagem processada: {processed_message}")
        print(f"Fato salvo: {fact_saved}")
        
        # Verificar se o fato foi salvo
        facts = memory_service.get_user_facts(user_id)
        print(f"Fatos salvos: {facts}")
        
        # Verificar contexto do usuário
        context = memory_service.get_user_context_for_chat(user_id)
        print(f"Contexto gerado: {context}")
        
        # Simular salvamento da conversa
        memory_service.save_message_with_profile_update(
            user_id=user_id,
            session_id=session_id,
            message=message1,
            response="✅ Informação salva na memória! Ok, Cledson. Lembrei que seu nome é Cledson.",
            metadata={"fact_saved": fact_saved}
        )
        print("✅ Conversa salva com atualização de perfil")
        
        # Verificar perfil após salvamento
        profile = memory_service.get_user_profile(user_id)
        print(f"Perfil após salvamento: {profile}")
        
        # Segunda mensagem: simular "qual meu nome ?"
        print("\n2. Simulando segunda mensagem 'qual meu nome ?':")
        message2 = "qual meu nome ?"
        
        # Verificar se o contexto seria incluído
        context2 = memory_service.get_user_context_for_chat(user_id)
        print(f"Contexto para segunda mensagem: {context2}")
        
        # Verificar histórico
        history = memory_service.get_conversation_history(user_id, session_id, limit=10)
        print(f"Histórico de conversas: {len(history)} mensagens")
        for i, conv in enumerate(history):
            print(f"  {i+1}. Usuário: {conv['message']}")
            print(f"     Assistente: {conv['response']}")
        
        # Verificar se o nome está no contexto
        if "cledson" in context2.lower():
            print("✅ SUCESSO: O nome está no contexto do usuário!")
        else:
            print("❌ FALHA: O nome não está no contexto do usuário.")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_logic()
