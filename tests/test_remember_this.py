#!/usr/bin/env python3
import requests
import json
import uuid
import time

# Configurações
BASE_URL = "http://localhost:5000/api"
USER_ID = "test_remember_user_789"

def test_remember_this_functionality():
    """Testar funcionalidade 'Lembre-se disso' com diferentes provedores"""
    print("🧠 Testando Funcionalidade 'Lembre-se disso'")
    print("=" * 60)
    
    # Teste com diferentes palavras-chave
    test_phrases = [
        "lembre-se disso: eu andei de bicicleta no sábado",
        "salvar para depois: minha cor favorita é azul",
        "importante: tenho alergia a amendoim",
        "não esqueça: meu aniversário é em dezembro",
        "anotar: gosto de café sem açúcar"
    ]
    
    # Testar com Gemini
    print("\n🤖 Testando com Gemini")
    print("-" * 30)
    
    session_id = str(uuid.uuid4())
    
    for i, phrase in enumerate(test_phrases):
        print(f"\n{i+1}. Salvando: '{phrase}'")
        
        payload = {
            "message": phrase,
            "user_id": USER_ID + "_gemini",
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/gemini/chat", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resposta: {result.get('response', 'N/A')[:100]}...")
            print(f"Fato salvo: {result.get('fact_saved', False)}")
        else:
            print(f"Erro: {response.text}")
        
        time.sleep(1)
    
    # Testar recuperação em nova sessão
    print(f"\n📋 Testando recuperação em nova sessão")
    new_session_id = str(uuid.uuid4())
    
    payload = {
        "message": "Você pode me lembrar de todas as coisas importantes que eu te disse?",
        "user_id": USER_ID + "_gemini",
        "session_id": new_session_id
    }
    
    response = requests.post(f"{BASE_URL}/gemini/chat", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")
    else:
        print(f"Erro: {response.text}")

def test_remember_this_openai():
    """Testar funcionalidade com OpenAI"""
    print("\n🤖 Testando com OpenAI")
    print("-" * 30)
    
    session_id = str(uuid.uuid4())
    
    # Salvar alguns fatos
    facts_to_save = [
        "lembrar: trabalho na empresa XYZ",
        "importante: tenho reunião às 15h toda terça"
    ]
    
    for fact in facts_to_save:
        print(f"\nSalvando: '{fact}'")
        
        payload = {
            "message": fact,
            "user_id": USER_ID + "_openai",
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/openai/chat", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Fato salvo: {result.get('fact_saved', False)}")
        else:
            print(f"Erro: {response.text}")
        
        time.sleep(1)
    
    # Testar recuperação
    print(f"\n📋 Testando recuperação")
    payload = {
        "message": "Onde eu trabalho e quando tenho reunião?",
        "user_id": USER_ID + "_openai",
        "session_id": str(uuid.uuid4())  # Nova sessão
    }
    
    response = requests.post(f"{BASE_URL}/openai/chat", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")

def test_remember_this_groq():
    """Testar funcionalidade com Groq"""
    print("\n🤖 Testando com Groq")
    print("-" * 30)
    
    session_id = str(uuid.uuid4())
    
    # Salvar fato
    payload = {
        "message": "lembre-se disso: meu hobby é tocar violão",
        "user_id": USER_ID + "_groq",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/groq/chat", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Fato salvo: {result.get('fact_saved', False)}")
        print(f"Resposta: {result.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response.text}")
    
    time.sleep(2)
    
    # Testar recuperação
    payload = {
        "message": "Qual é o meu hobby?",
        "user_id": USER_ID + "_groq",
        "session_id": str(uuid.uuid4())  # Nova sessão
    }
    
    response = requests.post(f"{BASE_URL}/groq/chat", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")

def test_remember_this_langchain():
    """Testar funcionalidade com LangChain"""
    print("\n🤖 Testando com LangChain")
    print("-" * 30)
    
    session_id = str(uuid.uuid4())
    
    # Salvar fato
    payload = {
        "message": "importante: moro na cidade de São Paulo",
        "user_id": USER_ID + "_langchain",
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/agent/chat", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Fato salvo: {result.get('fact_saved', False)}")
        print(f"Resposta: {result.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response.text}")
    
    time.sleep(2)
    
    # Testar recuperação
    payload = {
        "message": "Em qual cidade eu moro?",
        "user_id": USER_ID + "_langchain",
        "session_id": str(uuid.uuid4())  # Nova sessão
    }
    
    response = requests.post(f"{BASE_URL}/agent/chat", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")

def test_memory_service_directly():
    """Testar MemoryService diretamente"""
    print("\n🔧 Testando MemoryService Diretamente")
    print("-" * 40)
    
    try:
        import sys
        sys.path.append('/home/ubuntu/iara-flow-bff/src')
        from services.memory_service import MemoryService
        
        memory_service = MemoryService()
        
        # Testar detecção de fatos
        test_messages = [
            "lembre-se disso: eu gosto de pizza",
            "salvar para depois: tenho um gato chamado Mimi",
            "importante: trabalho das 9h às 18h",
            "Olá, como você está?",  # Sem palavra-chave
            "não esqueça: meu filme favorito é Matrix"
        ]
        
        user_id = "test_direct_user"
        
        for msg in test_messages:
            processed_msg, fact_saved = memory_service.detect_and_save_user_fact(msg, user_id)
            print(f"Mensagem: '{msg}'")
            print(f"Processada: '{processed_msg}'")
            print(f"Fato salvo: {fact_saved}")
            print()
        
        # Verificar fatos salvos
        facts = memory_service.get_user_facts(user_id)
        print(f"Fatos salvos para {user_id}: {facts}")
        
        # Verificar contexto
        context = memory_service.get_user_context_for_chat(user_id)
        print(f"Contexto para chat: {context}")
        
    except Exception as e:
        print(f"Erro ao testar diretamente: {e}")

def test_edge_cases():
    """Testar casos extremos"""
    print("\n⚠️  Testando Casos Extremos")
    print("-" * 30)
    
    try:
        import sys
        sys.path.append('/home/ubuntu/iara-flow-bff/src')
        from services.memory_service import MemoryService
        
        memory_service = MemoryService()
        user_id = "test_edge_user"
        
        # Teste 1: Palavra-chave sem conteúdo
        msg1 = "lembre-se disso:"
        processed1, saved1 = memory_service.detect_and_save_user_fact(msg1, user_id)
        print(f"Teste 1 - Sem conteúdo: '{msg1}' -> Salvo: {saved1}")
        
        # Teste 2: Múltiplas palavras-chave
        msg2 = "lembre-se disso: gosto de café importante: trabalho cedo"
        processed2, saved2 = memory_service.detect_and_save_user_fact(msg2, user_id)
        print(f"Teste 2 - Múltiplas: '{msg2}' -> Salvo: {saved2}")
        
        # Teste 3: Palavra-chave no meio da frase
        msg3 = "Hoje eu quero lembre-se disso: comprar leite no mercado"
        processed3, saved3 = memory_service.detect_and_save_user_fact(msg3, user_id)
        print(f"Teste 3 - No meio: '{msg3}' -> Salvo: {saved3}")
        
        # Verificar fatos
        facts = memory_service.get_user_facts(user_id)
        print(f"Fatos salvos nos testes: {facts}")
        
    except Exception as e:
        print(f"Erro nos testes extremos: {e}")

if __name__ == "__main__":
    try:
        test_remember_this_functionality()
        test_remember_this_openai()
        test_remember_this_groq()
        test_remember_this_langchain()
        test_memory_service_directly()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ Testes da funcionalidade 'Lembre-se disso' concluídos!")
        
    except Exception as e:
        print(f"Erro durante os testes: {e}")

