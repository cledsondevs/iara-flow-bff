#!/usr/bin/env python3
import requests
import json
import uuid

# Configurações
BASE_URL = "http://localhost:5000/api"
USER_ID = "test_user_123"
SESSION_ID = str(uuid.uuid4())

def test_gemini_chat():
    """Testar o endpoint do chat Gemini"""
    print("=== Teste do Chat Gemini ===")
    
    # Primeira mensagem
    print("\n1. Enviando primeira mensagem...")
    payload1 = {
        "message": "Olá! Meu nome é João. Como você está?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response1 = requests.post(f"{BASE_URL}/gemini/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    print(f"Resposta: {json.dumps(response1.json(), indent=2, ensure_ascii=False)}")
    
    # Segunda mensagem (testando memória)
    print("\n2. Enviando segunda mensagem para testar memória...")
    payload2 = {
        "message": "Você lembra qual é o meu nome?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response2 = requests.post(f"{BASE_URL}/gemini/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    print(f"Resposta: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}")
    
    # Terceira mensagem (continuando conversa)
    print("\n3. Enviando terceira mensagem...")
    payload3 = {
        "message": "Conte-me uma piada sobre programação",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response3 = requests.post(f"{BASE_URL}/gemini/chat", json=payload3)
    print(f"Status: {response3.status_code}")
    print(f"Resposta: {json.dumps(response3.json(), indent=2, ensure_ascii=False)}")
    
    # Verificar memória
    print("\n4. Verificando memória da conversa...")
    memory_response = requests.get(f"{BASE_URL}/gemini/memory", params={
        "user_id": USER_ID,
        "session_id": SESSION_ID
    })
    print(f"Status: {memory_response.status_code}")
    print(f"Memória: {json.dumps(memory_response.json(), indent=2, ensure_ascii=False)}")

def test_new_session():
    """Testar nova sessão para verificar isolamento"""
    print("\n=== Teste de Nova Sessão ===")
    
    new_session_id = str(uuid.uuid4())
    
    payload = {
        "message": "Você lembra qual é o meu nome?",
        "user_id": USER_ID,
        "session_id": new_session_id
    }
    
    response = requests.post(f"{BASE_URL}/gemini/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    try:
        test_gemini_chat()
        test_new_session()
        print("\n=== Testes concluídos ===")
    except Exception as e:
        print(f"Erro durante o teste: {e}")

