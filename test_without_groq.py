#!/usr/bin/env python3
"""
Script de teste para validar a aplicação sem a funcionalidade Groq
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Testar se todas as importações funcionam sem o Groq"""
    print("🔍 Testando importações sem Groq...")
    
    try:
        from app.main import create_app
        print("✅ app.main.create_app importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar app.main.create_app: {e}")
        return False
    
    try:
        from app.api.routes.chat_routes import chat_bp
        print("✅ app.api.routes.chat_routes.chat_bp importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar chat_bp: {e}")
        return False
    
    try:
        from app.services.gemini_chat_service import GeminiChatService
        print("✅ app.services.gemini_chat_service importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar GeminiChatService: {e}")
        return False
    
    try:
        from app.services.openai_chat_service import OpenAIChatService
        print("✅ app.services.openai_chat_service importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar OpenAIChatService: {e}")
        return False
    
    # Verificar se o Groq NÃO está sendo importado
    try:
        from app.services.groq_chat_service import GroqChatService
        print("⚠️  AVISO: GroqChatService ainda está sendo importado (deveria estar comentado)")
        return False
    except ImportError:
        print("✅ GroqChatService corretamente isolado (ImportError esperado)")
    except Exception as e:
        print(f"❌ Erro inesperado ao tentar importar GroqChatService: {e}")
        return False
    
    return True

def test_app_creation():
    """Testar se a aplicação Flask pode ser criada sem erros"""
    print("\n🔍 Testando criação da aplicação Flask...")
    
    try:
        from app.main import create_app
        app = create_app()
        print("✅ Aplicação Flask criada com sucesso")
        
        # Verificar se o blueprint chat_bp está registrado
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        if 'chat' in blueprint_names:
            print("✅ Blueprint 'chat' registrado com sucesso")
        else:
            print("❌ Blueprint 'chat' não encontrado")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar aplicação Flask: {e}")
        return False

def test_routes():
    """Testar se as rotas estão funcionando corretamente"""
    print("\n🔍 Testando rotas disponíveis...")
    
    try:
        from app.main import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Testar health check
            response = client.get('/api/chat/health')
            if response.status_code == 200:
                data = response.get_json()
                if 'services' in data and 'gemini' in data['services'] and 'openai' in data['services']:
                    print("✅ Health check funcionando - Gemini e OpenAI disponíveis")
                    if 'groq' not in data['services']:
                        print("✅ Groq corretamente removido do health check")
                    else:
                        print("⚠️  AVISO: Groq ainda aparece no health check")
                        return False
                else:
                    print("❌ Health check não retornou serviços esperados")
                    return False
            else:
                print(f"❌ Health check falhou com status {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        return False

def test_services():
    """Testar se os serviços podem ser instanciados"""
    print("\n🔍 Testando instanciação dos serviços...")
    
    try:
        from app.services.gemini_chat_service import GeminiChatService
        gemini_service = GeminiChatService()
        print("✅ GeminiChatService instanciado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao instanciar GeminiChatService: {e}")
        return False
    
    try:
        from app.services.openai_chat_service import OpenAIChatService
        openai_service = OpenAIChatService()
        print("✅ OpenAIChatService instanciado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao instanciar OpenAIChatService: {e}")
        return False
    
    return True

def main():
    """Função principal do teste"""
    print("🚀 Iniciando testes da aplicação sem Groq...")
    
    tests = [
        ("Importações", test_imports),
        ("Criação da aplicação", test_app_creation),
        ("Rotas", test_routes),
        ("Serviços", test_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Teste: {test_name}")
        print('='*50)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSOU")
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print(f"\n{'='*50}")
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A aplicação está funcionando sem Groq.")
        return True
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

