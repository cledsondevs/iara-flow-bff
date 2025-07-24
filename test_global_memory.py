#!/usr/bin/env python3
import requests
import json
import uuid
import time

# Configurações
BASE_URL = "http://localhost:5000/api"
USER_ID = "test_global_user_456"

def test_global_memory_gemini():
    """Testar memória global com Gemini"""
    print("=== Teste de Memória Global - Gemini ===")
    
    # Primeira sessão - apresentar nome
    session1_id = str(uuid.uuid4())
    print(f"\n1. Primeira sessão ({session1_id[:8]}...) - Apresentando nome")
    
    payload1 = {
        "message": "Olá! Meu nome é João e eu sou desenvolvedor Python. Como você está?",
        "user_id": USER_ID,
        "session_id": session1_id
    }
    
    response1 = requests.post(f"{BASE_URL}/gemini/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response1.text}")
    
    # Aguardar um pouco para simular tempo real
    time.sleep(2)
    
    # Segunda sessão - testar se lembra do nome
    session2_id = str(uuid.uuid4())
    print(f"\n2. Segunda sessão ({session2_id[:8]}...) - Testando memória global")
    
    payload2 = {
        "message": "Você lembra qual é o meu nome e minha profissão?",
        "user_id": USER_ID,
        "session_id": session2_id
    }
    
    response2 = requests.post(f"{BASE_URL}/gemini/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
        
        # Verificar se mencionou o nome
        response_text = result2.get('response', '').lower()
        if 'joão' in response_text:
            print("✅ SUCESSO: O assistente lembrou do nome!")
        else:
            print("❌ FALHA: O assistente não lembrou do nome.")
    else:
        print(f"Erro: {response2.text}")

def test_global_memory_openai():
    """Testar memória global com OpenAI"""
    print("\n=== Teste de Memória Global - OpenAI ===")
    
    # Primeira sessão - apresentar informações
    session1_id = str(uuid.uuid4())
    print(f"\n1. Primeira sessão ({session1_id[:8]}...) - Apresentando informações")
    
    payload1 = {
        "message": "Oi! Eu me chamo Maria e tenho 28 anos. Trabalho como designer gráfica.",
        "user_id": USER_ID + "_openai",
        "session_id": session1_id
    }
    
    response1 = requests.post(f"{BASE_URL}/openai/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response1.text}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Segunda sessão - testar memória
    session2_id = str(uuid.uuid4())
    print(f"\n2. Segunda sessão ({session2_id[:8]}...) - Testando memória global")
    
    payload2 = {
        "message": "Você se lembra de mim? Qual é o meu nome e profissão?",
        "user_id": USER_ID + "_openai",
        "session_id": session2_id
    }
    
    response2 = requests.post(f"{BASE_URL}/openai/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
        
        # Verificar se mencionou o nome
        response_text = result2.get('response', '').lower()
        if 'maria' in response_text:
            print("✅ SUCESSO: O assistente lembrou do nome!")
        else:
            print("❌ FALHA: O assistente não lembrou do nome.")
    else:
        print(f"Erro: {response2.text}")

def test_global_memory_groq():
    """Testar memória global com Groq"""
    print("\n=== Teste de Memória Global - Groq ===")
    
    # Primeira sessão - apresentar informações
    session1_id = str(uuid.uuid4())
    print(f"\n1. Primeira sessão ({session1_id[:8]}...) - Apresentando informações")
    
    payload1 = {
        "message": "Olá! Sou o Carlos, tenho 35 anos e sou engenheiro de software especializado em IA.",
        "user_id": USER_ID + "_groq",
        "session_id": session1_id
    }
    
    response1 = requests.post(f"{BASE_URL}/groq/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response1.text}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Segunda sessão - testar memória
    session2_id = str(uuid.uuid4())
    print(f"\n2. Segunda sessão ({session2_id[:8]}...) - Testando memória global")
    
    payload2 = {
        "message": "Você lembra de mim? Como eu me chamo e qual é minha área de especialização?",
        "user_id": USER_ID + "_groq",
        "session_id": session2_id
    }
    
    response2 = requests.post(f"{BASE_URL}/groq/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
        
        # Verificar se mencionou o nome
        response_text = result2.get('response', '').lower()
        if 'carlos' in response_text:
            print("✅ SUCESSO: O assistente lembrou do nome!")
        else:
            print("❌ FALHA: O assistente não lembrou do nome.")
    else:
        print(f"Erro: {response2.text}")

def test_global_memory_langchain():
    """Testar memória global com LangChain"""
    print("\n=== Teste de Memória Global - LangChain ===")
    
    # Primeira sessão - apresentar informações
    session1_id = str(uuid.uuid4())
    print(f"\n1. Primeira sessão ({session1_id[:8]}...) - Apresentando informações")
    
    payload1 = {
        "message": "Oi! Eu sou a Ana, tenho 30 anos e trabalho como cientista de dados em uma startup de fintech.",
        "user_id": USER_ID + "_langchain",
        "session_id": session1_id
    }
    
    response1 = requests.post(f"{BASE_URL}/agent/chat", json=payload1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Resposta: {result1.get('response', 'N/A')[:100]}...")
    else:
        print(f"Erro: {response1.text}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Segunda sessão - testar memória
    session2_id = str(uuid.uuid4())
    print(f"\n2. Segunda sessão ({session2_id[:8]}...) - Testando memória global")
    
    payload2 = {
        "message": "Você se lembra de mim? Qual é o meu nome, idade e onde trabalho?",
        "user_id": USER_ID + "_langchain",
        "session_id": session2_id
    }
    
    response2 = requests.post(f"{BASE_URL}/agent/chat", json=payload2)
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"Resposta: {result2.get('response', 'N/A')}")
        
        # Verificar se mencionou o nome
        response_text = result2.get('response', '').lower()
        if 'ana' in response_text:
            print("✅ SUCESSO: O assistente lembrou do nome!")
        else:
            print("❌ FALHA: O assistente não lembrou do nome.")
    else:
        print(f"Erro: {response2.text}")

def test_user_profile_api():
    """Testar API de perfil do usuário (se implementada)"""
    print("\n=== Teste de API de Perfil do Usuário ===")
    
    # Tentar acessar perfil via MemoryService diretamente
    try:
        import sys
        sys.path.append('/home/ubuntu/iara-flow-bff/src')
        from services.memory_service import MemoryService
        
        memory_service = MemoryService()
        
        # Verificar perfil do usuário Gemini
        profile = memory_service.get_user_profile(USER_ID)
        print(f"Perfil do usuário {USER_ID}: {profile}")
        
        # Verificar perfil do usuário OpenAI
        profile_openai = memory_service.get_user_profile(USER_ID + "_openai")
        print(f"Perfil do usuário OpenAI: {profile_openai}")
        
        # Verificar perfil do usuário Groq
        profile_groq = memory_service.get_user_profile(USER_ID + "_groq")
        print(f"Perfil do usuário Groq: {profile_groq}")
        
        # Verificar perfil do usuário LangChain
        profile_langchain = memory_service.get_user_profile(USER_ID + "_langchain")
        print(f"Perfil do usuário LangChain: {profile_langchain}")
        
    except Exception as e:
        print(f"Erro ao acessar perfis: {e}")

if __name__ == "__main__":
    try:
        print("🧠 Testando Memória Global por Usuário")
        print("=" * 50)
        
        test_global_memory_gemini()
        test_global_memory_openai()
        test_global_memory_groq()
        test_global_memory_langchain()
        test_user_profile_api()
        
        print("\n" + "=" * 50)
        print("✅ Testes de memória global concluídos!")
        
    except Exception as e:
        print(f"Erro durante os testes: {e}")

