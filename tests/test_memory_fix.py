#!/usr/bin/env python3
"""
Script de teste para validar as correções no sistema de memória
"""

import sys
import os
import json
import sqlite3
from datetime import datetime

# Adicionar o diretório do app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.memory_service import MemoryService
from app.config.settings import Config

def test_memory_service():
    """Testar o MemoryService corrigido"""
    print("🧪 Iniciando testes do MemoryService...")
    
    # Criar instância do serviço
    memory_service = MemoryService()
    
    # Dados de teste
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"
    test_message = "Olá, meu nome é João e tenho 30 anos"
    test_response = "Olá João! Prazer em conhecê-lo. Como posso ajudá-lo hoje?"
    
    print(f"📝 Testando com usuário: {test_user_id}")
    print(f"📝 Sessão: {test_session_id}")
    
    try:
        # Teste 1: Salvar conversa com atualização de perfil
        print("\n1️⃣ Testando save_message_with_profile_update...")
        memory_service.save_message_with_profile_update(
            user_id=test_user_id,
            session_id=test_session_id,
            message=test_message,
            response=test_response,
            metadata={"test": True}
        )
        print("✅ Conversa salva com sucesso!")
        
        # Teste 2: Recuperar perfil do usuário
        print("\n2️⃣ Testando get_user_profile...")
        user_profile = memory_service.get_user_profile(test_user_id)
        print(f"📊 Perfil recuperado: {json.dumps(user_profile, indent=2, ensure_ascii=False)}")
        
        # Teste 3: Recuperar histórico de conversas
        print("\n3️⃣ Testando get_conversation_history...")
        history = memory_service.get_conversation_history(test_user_id, test_session_id, limit=5)
        print(f"📚 Histórico recuperado: {len(history)} conversas")
        for i, conv in enumerate(history):
            print(f"  {i+1}. Mensagem: {conv['message'][:50]}...")
            print(f"     Resposta: {conv['response'][:50]}...")
        
        # Teste 4: Atualizar perfil diretamente
        print("\n4️⃣ Testando update_user_profile...")
        profile_updates = {
            "profissao": "desenvolvedor",
            "cidade": "São Paulo",
            "interesse": "tecnologia"
        }
        memory_service.update_user_profile(test_user_id, profile_updates)
        print("✅ Perfil atualizado com sucesso!")
        
        # Verificar perfil atualizado
        updated_profile = memory_service.get_user_profile(test_user_id)
        print(f"📊 Perfil atualizado: {json.dumps(updated_profile, indent=2, ensure_ascii=False)}")
        
        # Teste 5: Testar função detect_and_save_user_fact
        print("\n5️⃣ Testando detect_and_save_user_fact...")
        fact_message = "Lembre-se disso: eu gosto de café pela manhã"
        processed_msg, fact_saved = memory_service.detect_and_save_user_fact(fact_message, test_user_id)
        print(f"📝 Mensagem processada: {processed_msg}")
        print(f"💾 Fato salvo: {fact_saved}")
        
        # Teste 6: Recuperar fatos do usuário
        print("\n6️⃣ Testando get_user_facts...")
        user_facts = memory_service.get_user_facts(test_user_id)
        print(f"📋 Fatos do usuário: {len(user_facts)} encontrados")
        for fact in user_facts:
            print(f"  - {fact['content']}")
        
        # Teste 7: Obter contexto para chat
        print("\n7️⃣ Testando get_user_context_for_chat...")
        context = memory_service.get_user_context_for_chat(test_user_id)
        print(f"🎯 Contexto do usuário: {context[:200]}...")
        
        # Teste 8: Estatísticas de memória
        print("\n8️⃣ Testando get_memory_stats...")
        stats = memory_service.get_memory_stats(test_user_id)
        print(f"📈 Estatísticas: {json.dumps(stats, indent=2)}")
        
        print("\n✅ Todos os testes passaram com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_integrity():
    """Testar integridade do banco de dados"""
    print("\n🔍 Testando integridade do banco de dados...")
    
    try:
        db_path = Config.DATABASE_PATH
        print(f"📁 Caminho do banco: {db_path}")
        
        if not os.path.exists(db_path):
            print("❌ Banco de dados não existe!")
            return False
        
        # Conectar ao banco e verificar tabelas
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Tabelas encontradas: {[table[0] for table in tables]}")
        
        # Verificar estrutura da tabela conversations
        cursor.execute("PRAGMA table_info(conversations);")
        conversations_schema = cursor.fetchall()
        print(f"🏗️ Schema da tabela conversations: {len(conversations_schema)} colunas")
        
        # Verificar estrutura da tabela user_profiles
        cursor.execute("PRAGMA table_info(user_profiles);")
        profiles_schema = cursor.fetchall()
        print(f"🏗️ Schema da tabela user_profiles: {len(profiles_schema)} colunas")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM conversations;")
        conv_count = cursor.fetchone()[0]
        print(f"💬 Total de conversas: {conv_count}")
        
        cursor.execute("SELECT COUNT(*) FROM user_profiles;")
        profile_count = cursor.fetchone()[0]
        print(f"👤 Total de perfis: {profile_count}")
        
        conn.close()
        print("✅ Integridade do banco verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar integridade do banco: {str(e)}")
        return False

def cleanup_test_data():
    """Limpar dados de teste"""
    print("\n🧹 Limpando dados de teste...")
    
    try:
        memory_service = MemoryService()
        test_user_id = "test_user_123"
        
        # Limpar memória do usuário de teste
        memory_service.clear_user_memory(test_user_id)
        print("✅ Dados de teste limpos!")
        
    except Exception as e:
        print(f"❌ Erro ao limpar dados de teste: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando validação das correções do sistema de memória")
    print("=" * 60)
    
    # Testar integridade do banco
    db_ok = test_database_integrity()
    
    if db_ok:
        # Testar funcionalidades do MemoryService
        tests_ok = test_memory_service()
        
        if tests_ok:
            print("\n🎉 Todas as correções foram validadas com sucesso!")
            print("✅ O sistema de memória está funcionando corretamente")
        else:
            print("\n❌ Alguns testes falharam. Verifique os logs acima.")
            sys.exit(1)
    else:
        print("\n❌ Problemas na integridade do banco de dados.")
        sys.exit(1)
    
    # Opcionalmente limpar dados de teste
    print("\n🤔 Deseja limpar os dados de teste? (y/n): ", end="")
    try:
        choice = input().lower()
        if choice in ['y', 'yes', 's', 'sim']:
            cleanup_test_data()
    except:
        pass
    
    print("\n✨ Validação concluída!")

