#!/usr/bin/env python3
import requests
import json

def test_gemini_endpoint():
    print("=== Teste do Endpoint Gemini ===")
    
    url = "http://localhost:5000/api/gemini/chat"
    payload = {
        "message": "Olá, qual é o meu nome?",
        "user_id": "test_user_123",
        "session_id": "test_session_456",
        "api_key": "AIzaSyDpLNBaYVrLSzxWj0kLD3v7n75pR5O-AfM"
    }
    
    try:
        print(f"Fazendo requisição para: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sucesso!")
            print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print("❌ Erro!")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout na requisição")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor pode não estar rodando")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_gemini_endpoint()
