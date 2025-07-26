#!/usr/bin/env python3
"""
Script de teste de integração para verificar se as novas APIs estão funcionando na estrutura modular
"""
import sys
import os
import importlib.util

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

def test_modular_imports():
    """Testar se todos os módulos podem ser importados na estrutura modular"""
    print("🔍 Testando importações modulares...")
    
    try:
        # Testar importação do chat_routes modular
        from app.api.routes.chat_routes import chat_bp
        print("✅ app.api.routes.chat_routes importado com sucesso")
        
        # Testar importação dos serviços modulares
        from app.services.memory_service import MemoryService
        print("✅ app.services.memory_service importado com sucesso")
        
        from app.services.gemini_chat_service import GeminiChatService
        print("✅ app.services.gemini_chat_service importado com sucesso")
        
        from app.services.openai_chat_service import OpenAIChatService
        print("✅ app.services.openai_chat_service importado com sucesso")
        
        from app.services.groq_chat_service import GroqChatService
        print("✅ app.services.groq_chat_service importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_modular_app_creation():
    """Testar se a aplicação pode ser criada com estrutura modular"""
    print("\n🔍 Testando criação da aplicação modular...")
    
    try:
        from app.main import create_app
        app = create_app()
        print("✅ Aplicação modular criada com sucesso")
        
        # Verificar se as rotas estão registradas
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        chat_routes = [route for route in routes if '/api/gemini/chat' in route or '/api/openai/chat' in route or '/api/groq/chat' in route]
        
        if chat_routes:
            print(f"✅ Rotas de chat modulares encontradas: {len(chat_routes)} rotas")
            for route in chat_routes:
                print(f"   - {route}")
        else:
            print("❌ Nenhuma rota de chat modular encontrada")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação modular: {e}")
        return False

def test_modular_memory_service():
    """Testar se o MemoryService pode ser inicializado na estrutura modular"""
    print("\n🔍 Testando MemoryService modular...")
    
    try:
        from app.services.memory_service import MemoryService
        memory_service = MemoryService()
        print("✅ MemoryService modular inicializado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar MemoryService modular: {e}")
        return False

def test_service_instantiation():
    """Testar se os serviços de chat podem ser instanciados"""
    print("\n🔍 Testando instanciação dos serviços de chat...")
    
    try:
        # Criar arquivo .env temporário para teste
        with open('.env', 'w') as f:
            f.write("""
OPENAI_API_KEY=test_key
GEMINI_API_KEY=test_key
GROQ_API_KEY=test_key
DB_PATH=./test_iara_flow.db
HOST=0.0.0.0
PORT=5000
FLASK_ENV=production
DEBUG=False
SECRET_KEY=test_secret_key_here
CORS_ORIGINS=*
""")
        
        from app.services.gemini_chat_service import GeminiChatService
        from app.services.openai_chat_service import OpenAIChatService
        from app.services.groq_chat_service import GroqChatService
        
        gemini_service = GeminiChatService()
        print("✅ GeminiChatService instanciado com sucesso")
        
        openai_service = OpenAIChatService()
        print("✅ OpenAIChatService instanciado com sucesso")
        
        groq_service = GroqChatService()
        print("✅ GroqChatService instanciado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao instanciar serviços: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 Iniciando testes de integração modular...\n")
    
    tests = [
        test_modular_imports,
        test_modular_app_creation,
        test_modular_memory_service,
        test_service_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes modulares passaram! A estrutura modular está funcionando.")
        return 0
    else:
        print("❌ Alguns testes modulares falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit(main())

