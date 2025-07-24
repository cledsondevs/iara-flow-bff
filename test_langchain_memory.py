#!/usr/bin/env python3
import requests
import json
import uuid

# Configurações
BASE_URL = "http://localhost:5000/api"
USER_ID = "test_langchain_user_123"
SESSION_ID = str(uuid.uuid4())

def test_langchain_memory():
    """Testar o endpoint do LangChain Agent com memória de longo prazo"""
    print("=== Teste do LangChain Agent com Memória de Longo Prazo ===")
    
    # Primeira mensagem
    print("\n1. Enviando primeira mensagem...")
    payload1 = {
        "message": "Olá! Meu nome é Maria e eu trabalho como desenvolvedora Python. Como você está?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response1 = requests.post(f"{BASE_URL}/agent/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')}")
        print(f"Session ID: {result1.get('session_id', 'N/A')}")
        print(f"Provider: {result1.get('provider', 'N/A')}")
    else:
        print(f"Erro: {response1.text}")
    
    # Segunda mensagem (testando memória)
    print("\n2. Enviando segunda mensagem para testar memória...")
    payload2 = {
        "message": "Você lembra qual é o meu nome e minha profissão?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response2 = requests.post(f"{BASE_URL}/agent/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
    else:
        print(f"Erro: {response2.text}")
    
    # Terceira mensagem (usando ferramentas)
    print("\n3. Enviando terceira mensagem para testar uso de ferramentas...")
    payload3 = {
        "message": "Faça uma busca na web sobre as últimas novidades em Python 3.12",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response3 = requests.post(f"{BASE_URL}/agent/chat", json=payload3)
    print(f"Status: {response3.status_code}")
    if response3.status_code == 200:
        result3 = response3.json()
        print(f"Resposta: {result3.get('response', 'N/A')}")
    else:
        print(f"Erro: {response3.text}")
    
    # Verificar memória
    print("\n4. Verificando memória da conversa...")
    memory_response = requests.get(f"{BASE_URL}/agent/memory", params={
        "user_id": USER_ID,
        "session_id": SESSION_ID
    })
    print(f"Status: {memory_response.status_code}")
    if memory_response.status_code == 200:
        memory_data = memory_response.json()
        print(f"Número de mensagens na memória: {len(memory_data.get('memory', []))}")
        for i, msg in enumerate(memory_data.get('memory', [])[:3]):  # Mostrar apenas as 3 primeiras
            print(f"  Mensagem {i+1}: {msg.get('message', 'N/A')[:50]}...")
            print(f"  Resposta {i+1}: {msg.get('response', 'N/A')[:50]}...")
    else:
        print(f"Erro ao recuperar memória: {memory_response.text}")

def test_new_session():
    """Testar nova sessão para verificar isolamento"""
    print("\n=== Teste de Nova Sessão (LangChain) ===")
    
    new_session_id = str(uuid.uuid4())
    
    payload = {
        "message": "Você lembra qual é o meu nome e profissão?",
        "user_id": USER_ID,
        "session_id": new_session_id
    }
    
    response = requests.post(f"{BASE_URL}/agent/chat", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")
        print("(Esta resposta deve indicar que o agente não lembra, pois é uma nova sessão)")
    else:
        print(f"Erro: {response.text}")

if __name__ == "__main__":
    try:
        test_langchain_memory()
        test_new_session()
        print("\n=== Testes do LangChain concluídos ===")
    except Exception as e:
        print(f"Erro durante o teste: {e}")

