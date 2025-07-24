#!/usr/bin/env python3
import requests
import json
import uuid

# Configurações
BASE_URL = "http://localhost:5000/api"
USER_ID = "test_groq_user_123"
SESSION_ID = str(uuid.uuid4())

def test_groq_chat():
    """Testar o endpoint do chat Groq"""
    print("=== Teste do Chat Groq ===")
    
    # Primeira mensagem
    print("\n1. Enviando primeira mensagem...")
    payload1 = {
        "message": "Olá! Meu nome é Carlos e eu sou engenheiro de software. Como você está?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response1 = requests.post(f"{BASE_URL}/groq/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')}")
        print(f"Session ID: {result1.get('session_id', 'N/A')}")
        print(f"Modelo: {result1.get('model', 'N/A')}")
        print(f"Usage: {result1.get('usage', 'N/A')}")
    else:
        print(f"Erro: {response1.text}")
    
    # Segunda mensagem (testando memória)
    print("\n2. Enviando segunda mensagem para testar memória...")
    payload2 = {
        "message": "Você lembra qual é o meu nome e minha profissão?",
        "user_id": USER_ID,
        "session_id": SESSION_ID
    }
    
    response2 = requests.post(f"{BASE_URL}/groq/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
    else:
        print(f"Erro: {response2.text}")
    
    # Terceira mensagem (testando modelo específico)
    print("\n3. Enviando terceira mensagem com modelo específico...")
    payload3 = {
        "message": "Conte-me uma curiosidade sobre inteligência artificial",
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "model": "mixtral-8x7b-32768"
    }
    
    response3 = requests.post(f"{BASE_URL}/groq/chat", json=payload3)
    print(f"Status: {response3.status_code}")
    if response3.status_code == 200:
        result3 = response3.json()
        print(f"Resposta: {result3.get('response', 'N/A')}")
        print(f"Modelo usado: {result3.get('model', 'N/A')}")
    else:
        print(f"Erro: {response3.text}")
    
    # Verificar memória
    print("\n4. Verificando memória da conversa...")
    memory_response = requests.get(f"{BASE_URL}/groq/memory", params={
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

def test_groq_models():
    """Testar endpoint de modelos disponíveis"""
    print("\n=== Teste de Modelos Groq ===")
    
    response = requests.get(f"{BASE_URL}/groq/models")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Modelos disponíveis: {result.get('models', [])}")
    else:
        print(f"Erro: {response.text}")

def test_new_session():
    """Testar nova sessão para verificar isolamento"""
    print("\n=== Teste de Nova Sessão (Groq) ===")
    
    new_session_id = str(uuid.uuid4())
    
    payload = {
        "message": "Você lembra qual é o meu nome e profissão?",
        "user_id": USER_ID,
        "session_id": new_session_id
    }
    
    response = requests.post(f"{BASE_URL}/groq/chat", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Resposta: {result.get('response', 'N/A')}")
        print("(Esta resposta deve indicar que o agente não lembra, pois é uma nova sessão)")
    else:
        print(f"Erro: {response.text}")

def test_health_check():
    """Testar endpoint de saúde"""
    print("\n=== Teste de Health Check ===")
    
    response = requests.get(f"{BASE_URL}/chat/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Mensagem: {result.get('message', 'N/A')}")
        print(f"Serviços: {result.get('services', [])}")
    else:
        print(f"Erro: {response.text}")

if __name__ == "__main__":
    try:
        test_health_check()
        test_groq_models()
        test_groq_chat()
        test_new_session()
        print("\n=== Testes do Groq concluídos ===")
    except Exception as e:
        print(f"Erro durante o teste: {e}")

