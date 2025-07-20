#!/usr/bin/env python3
"""
Script de teste para a API de autenticação do Iara Flow BFF
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Testar endpoint de health check"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health Check - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Erro ao testar health check: {e}")
        return False

def test_register_user(username, password, email=None):
    """Testar registro de usuário"""
    try:
        data = {
            "username": username,
            "password": password
        }
        if email:
            data["email"] = email
            
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Register - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 201, response.json()
    except Exception as e:
        print(f"Erro ao testar registro: {e}")
        return False, None

def test_login_user(username, password):
    """Testar login de usuário"""
    try:
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Login - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except Exception as e:
        print(f"Erro ao testar login: {e}")
        return False, None

def test_verify_session(session_token):
    """Testar verificação de sessão"""
    try:
        data = {
            "session_token": session_token
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/verify",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Verify Session - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200, response.json()
    except Exception as e:
        print(f"Erro ao testar verificação de sessão: {e}")
        return False, None

def test_get_user(user_id, session_token):
    """Testar obtenção de informações do usuário"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/user/{user_id}",
            headers={
                "Authorization": f"Bearer {session_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"Get User - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200, response.json()
    except Exception as e:
        print(f"Erro ao testar obtenção de usuário: {e}")
        return False, None

def test_list_users(session_token):
    """Testar listagem de usuários"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/users",
            headers={
                "Authorization": f"Bearer {session_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"List Users - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200, response.json()
    except Exception as e:
        print(f"Erro ao testar listagem de usuários: {e}")
        return False, None

def main():
    """Função principal de teste"""
    print("=== Teste da API de Autenticação ===\n")
    
    # Testar health check
    print("1. Testando Health Check...")
    if not test_health_check():
        print("Falha no health check. Verifique se o servidor está rodando.")
        sys.exit(1)
    print()
    
    # Dados do usuário de teste
    test_username = "usuario_teste"
    test_password = "senha123"
    test_email = "teste@exemplo.com"
    
    # Testar registro
    print("2. Testando Registro de Usuário...")
    success, register_response = test_register_user(test_username, test_password, test_email)
    if not success:
        print("Falha no registro de usuário.")
        # Pode ser que o usuário já existe, vamos tentar fazer login
    print()
    
    # Testar login
    print("3. Testando Login de Usuário...")
    success, login_response = test_login_user(test_username, test_password)
    if not success:
        print("Falha no login de usuário.")
        sys.exit(1)
    
    session_token = login_response.get("session_token")
    user_id = login_response.get("user_id")
    print()
    
    # Testar verificação de sessão
    print("4. Testando Verificação de Sessão...")
    success, verify_response = test_verify_session(session_token)
    if not success:
        print("Falha na verificação de sessão.")
    print()
    
    # Testar obtenção de usuário
    print("5. Testando Obtenção de Informações do Usuário...")
    success, user_response = test_get_user(user_id, session_token)
    if not success:
        print("Falha na obtenção de informações do usuário.")
    print()
    
    # Testar listagem de usuários
    print("6. Testando Listagem de Usuários...")
    success, list_users_response = test_list_users(session_token)
    if not success:
        print("Falha na listagem de usuários.")
    print()
    
    print("=== Testes Concluídos ===")
    print(f"Usuário de teste criado/logado: {test_username}")
    print(f"Token de sessão: {session_token}")
    print(f"ID do usuário: {user_id}")

if __name__ == "__main__":
    main()

