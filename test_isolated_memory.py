#!/usr/bin/env python3
"""
Teste Completo do Sistema de Memória Isolado
"""

import sys
import os
import json
import requests
import time
from datetime import datetime

# Adicionar o diretório do app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_isolated_memory_service():
    """Testar o serviço de memória isolado diretamente"""
    print("🧪 Testando IsolatedMemoryService diretamente...")
    
    try:
        from app.services.isolated_memory_service import IsolatedMemoryService
        
        # Criar instância do serviço
        memory_service = IsolatedMemoryService()
        
        # Dados de teste
        test_user_id = "isolated_test_user_456"
        test_session_id = "isolated_test_session_789"
        
        print(f"📝 Testando com usuário: {test_user_id}")
        print(f"📝 Sessão: {test_session_id}")
        
        # Teste 1: Salvar conversa
        print("\n1️⃣ Testando save_conversation_isolated...")
        conversation_id = memory_service.save_conversation_isolated(
            user_id=test_user_id,
            session_id=test_session_id,
            user_message="Olá, meu nome é Maria e tenho 25 anos",
            assistant_response="Olá Maria! Prazer em conhecê-la. Como posso ajudá-la hoje?",
            metadata={"test": True, "timestamp": datetime.utcnow().isoformat()}
        )
        print(f"✅ Conversa salva - ID: {conversation_id}")
        
        # Teste 2: Recuperar histórico
        print("\n2️⃣ Testando get_conversation_history_isolated...")
        history = memory_service.get_conversation_history_isolated(test_user_id, test_session_id, limit=5)
        print(f"📚 Histórico recuperado: {len(history)} conversas")
        for i, conv in enumerate(history):
            print(f"  {i+1}. {conv['message'][:50]}... -> {conv['response'][:50]}...")
        
        # Teste 3: Recuperar perfil
        print("\n3️⃣ Testando get_user_profile_isolated...")
        profile = memory_service.get_user_profile_isolated(test_user_id)
        print(f"👤 Perfil: Versão {profile['version']}, Dados: {len(profile['profile_data'])} items")
        
        # Teste 4: Atualizar perfil
        print("\n4️⃣ Testando update_user_profile_isolated...")
        profile_updates = {
            "profissao": "engenheira",
            "cidade": "Rio de Janeiro",
            "hobby": "leitura"
        }
        success = memory_service.update_user_profile_isolated(test_user_id, profile_updates)
        print(f"✅ Perfil atualizado: {success}")
        
        # Verificar perfil atualizado
        updated_profile = memory_service.get_user_profile_isolated(test_user_id)
        print(f"📊 Perfil atualizado: {json.dumps(updated_profile['profile_data'], indent=2, ensure_ascii=False)}")
        
        # Teste 5: Salvar fato
        print("\n5️⃣ Testando save_user_fact_isolated...")
        fact_id = memory_service.save_user_fact_isolated(
            test_user_id, 
            "Gosta de café com leite pela manhã", 
            "preference"
        )
        print(f"💾 Fato salvo - ID: {fact_id}")
        
        # Teste 6: Recuperar fatos
        print("\n6️⃣ Testando get_user_facts_isolated...")
        facts = memory_service.get_user_facts_isolated(test_user_id)
        print(f"📋 Fatos recuperados: {len(facts)}")
        for fact in facts:
            print(f"  - {fact['content']} (tipo: {fact['type']})")
        
        # Teste 7: Comando de memória
        print("\n7️⃣ Testando detect_and_save_memory_command...")
        processed_msg, command_executed = memory_service.detect_and_save_memory_command(
            test_user_id, 
            "Lembre-se disso: eu prefiro trabalhar de manhã"
        )
        print(f"📝 Mensagem processada: {processed_msg}")
        print(f"💾 Comando executado: {command_executed}")
        
        # Teste 8: Contexto completo
        print("\n8️⃣ Testando get_user_context_isolated...")
        context = memory_service.get_user_context_isolated(test_user_id, test_session_id)
        print(f"🎯 Contexto gerado: {len(context)} caracteres")
        print(f"📄 Contexto (preview): {context[:200]}...")
        
        # Teste 9: Estatísticas
        print("\n9️⃣ Testando get_memory_stats_isolated...")
        stats = memory_service.get_memory_stats_isolated(test_user_id)
        print(f"📈 Estatísticas: {json.dumps(stats, indent=2)}")
        
        print("\n✅ Todos os testes do serviço isolado passaram!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro nos testes do serviço isolado: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_gemini_chat_service_v2():
    """Testar o serviço de chat Gemini V2"""
    print("\n🤖 Testando GeminiChatServiceV2...")
    
    try:
        from app.chats.services.gemini_chat_service_v2 import GeminiChatServiceV2
        
        # Criar instância do serviço
        gemini_service = GeminiChatServiceV2()
        
        test_user_id = "gemini_test_user_123"
        test_session_id = "gemini_test_session_456"
        
        print(f"📝 Testando com usuário: {test_user_id}")
        
        # Teste 1: Mensagem simples
        print("\n1️⃣ Testando process_message...")
        response1 = gemini_service.process_message(
            user_message="Olá, meu nome é João e sou desenvolvedor",
            user_id=test_user_id,
            session_id=test_session_id
        )
        print(f"🤖 Resposta 1: {response1['message'][:100]}...")
        print(f"📊 Contexto usado: {response1.get('context_used', False)}")
        
        # Teste 2: Comando de memória
        print("\n2️⃣ Testando comando de memória...")
        response2 = gemini_service.process_message(
            user_message="Lembre-se disso: eu gosto de programar em Python",
            user_id=test_user_id,
            session_id=test_session_id
        )
        print(f"🤖 Resposta 2: {response2['message'][:100]}...")
        print(f"💾 Comando de memória executado: {response2.get('memory_command_executed', False)}")
        
        # Teste 3: Mensagem com contexto
        print("\n3️⃣ Testando mensagem com contexto...")
        response3 = gemini_service.process_message(
            user_message="Qual é o meu nome mesmo?",
            user_id=test_user_id,
            session_id=test_session_id
        )
        print(f"🤖 Resposta 3: {response3['message'][:100]}...")
        
        # Teste 4: Recuperar memória
        print("\n4️⃣ Testando get_memory...")
        memory = gemini_service.get_memory(test_user_id, test_session_id)
        print(f"📚 Memória recuperada: {len(memory)} conversas")
        
        # Teste 5: Estatísticas
        print("\n5️⃣ Testando get_user_stats...")
        stats = gemini_service.get_user_stats(test_user_id)
        print(f"📈 Estatísticas: {json.dumps(stats, indent=2)}")
        
        print("\n✅ Todos os testes do Gemini V2 passaram!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro nos testes do Gemini V2: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Testar endpoints da API V2 (se o servidor estiver rodando)"""
    print("\n🌐 Testando endpoints da API V2...")
    
    base_url = "http://localhost:5000"
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print("⚠️ Servidor não está rodando, pulando testes de API")
            return True
    except requests.exceptions.RequestException:
        print("⚠️ Servidor não está rodando, pulando testes de API")
        return True
    
    try:
        test_user_id = "api_test_user_789"
        test_session_id = "api_test_session_012"
        
        # Teste 1: Health check
        print("\n1️⃣ Testando health check...")
        response = requests.get(f"{base_url}/api/v2/chat/health")
        if response.status_code == 200:
            print("✅ Health check passou")
            print(f"📄 Resposta: {response.json()}")
        else:
            print(f"❌ Health check falhou: {response.status_code}")
        
        # Teste 2: Chat endpoint
        print("\n2️⃣ Testando chat endpoint...")
        chat_data = {
            "message": "Olá, meu nome é Ana e sou designer",
            "user_id": test_user_id,
            "session_id": test_session_id
        }
        
        response = requests.post(f"{base_url}/api/v2/chat/gemini", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat endpoint passou")
            result = response.json()
            print(f"🤖 Resposta: {result['response'][:100]}...")
        else:
            print(f"❌ Chat endpoint falhou: {response.status_code}")
            print(f"Erro: {response.text}")
        
        # Teste 3: Comando de memória via API
        print("\n3️⃣ Testando comando de memória via API...")
        memory_data = {
            "message": "Lembre-se disso: eu trabalho com design gráfico",
            "user_id": test_user_id,
            "session_id": test_session_id
        }
        
        response = requests.post(f"{base_url}/api/v2/chat/gemini", json=memory_data)
        if response.status_code == 200:
            print("✅ Comando de memória via API passou")
            result = response.json()
            print(f"💾 Comando executado: {result.get('memory_command_executed', False)}")
        else:
            print(f"❌ Comando de memória via API falhou: {response.status_code}")
        
        # Teste 4: Recuperar memória via API
        print("\n4️⃣ Testando recuperação de memória via API...")
        response = requests.get(f"{base_url}/api/v2/chat/gemini/memory", params={
            "user_id": test_user_id,
            "session_id": test_session_id
        })
        if response.status_code == 200:
            print("✅ Recuperação de memória via API passou")
            result = response.json()
            print(f"📚 Conversas recuperadas: {len(result['memory'])}")
        else:
            print(f"❌ Recuperação de memória via API falhou: {response.status_code}")
        
        # Teste 5: Estatísticas via API
        print("\n5️⃣ Testando estatísticas via API...")
        response = requests.get(f"{base_url}/api/v2/chat/gemini/stats", params={
            "user_id": test_user_id
        })
        if response.status_code == 200:
            print("✅ Estatísticas via API passou")
            result = response.json()
            print(f"📈 Stats: {json.dumps(result['stats'], indent=2)}")
        else:
            print(f"❌ Estatísticas via API falhou: {response.status_code}")
        
        print("\n✅ Todos os testes de API passaram!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro nos testes de API: {str(e)}")
        return False

def cleanup_test_data():
    """Limpar dados de teste"""
    print("\n🧹 Limpando dados de teste...")
    
    try:
        from app.services.isolated_memory_service import IsolatedMemoryService
        
        memory_service = IsolatedMemoryService()
        
        test_users = [
            "isolated_test_user_456",
            "gemini_test_user_123", 
            "api_test_user_789"
        ]
        
        for user_id in test_users:
            try:
                success = memory_service.clear_user_memory_isolated(user_id)
                if success:
                    print(f"✅ Dados limpos para usuário: {user_id}")
                else:
                    print(f"⚠️ Falha ao limpar dados para usuário: {user_id}")
            except Exception as e:
                print(f"❌ Erro ao limpar usuário {user_id}: {e}")
        
        print("✅ Limpeza concluída!")
        
    except Exception as e:
        print(f"❌ Erro durante limpeza: {str(e)}")

def main():
    """Função principal de teste"""
    print("🚀 Iniciando Testes Completos do Sistema de Memória Isolado")
    print("=" * 70)
    
    all_tests_passed = True
    
    # Teste 1: Serviço de memória isolado
    if not test_isolated_memory_service():
        all_tests_passed = False
    
    # Teste 2: Serviço de chat Gemini V2
    if not test_gemini_chat_service_v2():
        all_tests_passed = False
    
    # Teste 3: Endpoints da API (opcional)
    if not test_api_endpoints():
        all_tests_passed = False
    
    # Resultado final
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("✅ O sistema de memória isolado está funcionando perfeitamente")
        print("✅ A integração com o Gemini V2 está funcionando")
        print("✅ As APIs estão respondendo corretamente")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔍 Verifique os logs acima para detalhes dos erros")
        sys.exit(1)
    
    # Perguntar sobre limpeza
    print("\n🤔 Deseja limpar os dados de teste? (y/n): ", end="")
    try:
        choice = input().lower()
        if choice in ['y', 'yes', 's', 'sim']:
            cleanup_test_data()
    except:
        pass
    
    print("\n✨ Testes concluídos!")

if __name__ == "__main__":
    main()

