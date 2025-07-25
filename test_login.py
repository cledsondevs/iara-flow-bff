#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

import requests
import json

def test_login():
    """Testar a funcionalidade de login"""
    print("=== Teste de Login ===")
    
    try:
        # URL do endpoint de login
        url = "http://localhost:5000/api/auth/login"
        
        # Dados de login
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        
        print(f"Testando login com: {login_data}")
        
        # Fazer requisição de login
        response = requests.post(url, json=login_data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login realizado com sucesso!")
            print(f"Session Token: {result.get('session_token', 'N/A')}")
            print(f"User ID: {result.get('user_id', 'N/A')}")
            return True
        else:
            print("❌ Falha no login")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor pode não estar rodando")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    test_login()
