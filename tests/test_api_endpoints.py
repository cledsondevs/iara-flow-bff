#!/usr/bin/env python3
"""
Script para testar os endpoints da API
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Testar endpoint de health check"""
    print("🔍 Testando health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_gemini_chat():
    """Testar endpoint de chat com Gemini"""
    print("🔍 Testando chat com Gemini...")
    payload = {
        "message": "Olá! Como você está?",
        "user_id": "1",
        "session_id": "test_session_123"
    }
    response = requests.post(f"{BASE_URL}/api/gemini/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_openai_chat():
    """Testar endpoint de chat com OpenAI"""
    print("🔍 Testando chat com OpenAI...")
    payload = {
        "message": "Olá! Qual é o seu nome?",
        "user_id": "1"
    }
    response = requests.post(f"{BASE_URL}/api/openai/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_memory():
    """Testar endpoint de memória"""
    print("🔍 Testando memória...")
    response = requests.get(f"{BASE_URL}/api/gemini/memory", params={
        "user_id": "1",
        "session_id": "test_session_123"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_api_keys():
    """Testar endpoints de API keys"""
    print("🔍 Testando API keys...")
    
    # Salvar uma chave
    payload = {
        "user_id": "test_user",
        "service_name": "openai",
        "api_key": "test_key_123"
    }
    response = requests.post(f"{BASE_URL}/api/api/keys", json=payload)
    print(f"Save API Key - Status: {response.status_code}")
    print(f"Save API Key - Response: {response.json()}")
    
    # Recuperar a chave
    response = requests.get(f"{BASE_URL}/api/api/keys/test_user/openai")
    print(f"Get API Key - Status: {response.status_code}")
    print(f"Get API Key - Response: {response.json()}")
    print()

def test_login():
    """Testar endpoint de login"""
    print("🔍 Testando login...")
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Executar todos os testes"""
    print("🚀 Iniciando testes dos endpoints da API\n")
    
    try:
        test_health_check()
        test_gemini_chat()
        test_openai_chat()
        test_memory()
        test_api_keys()
        test_login()
        
        print("✅ Testes concluídos!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()

