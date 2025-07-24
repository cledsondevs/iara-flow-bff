#!/usr/bin/env python3
"""
Script de teste de integração para verificar se as novas APIs estão funcionando
"""
import sys
import os
import importlib.util

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Testar se todos os módulos podem ser importados"""
    print("🔍 Testando importações...")
    
    try:
        # Testar importação do chat_routes
        from src.routes.chat_routes import chat_bp
        print("✅ src.routes.chat_routes importado com sucesso")
        
        # Testar importação dos serviços
        from src.services.memory_service import MemoryService
        print("✅ src.services.memory_service importado com sucesso")
        
        from src.services.gemini_chat_service import GeminiChatService
        print("✅ src.services.gemini_chat_service importado com sucesso")
        
        from src.services.openai_chat_service import OpenAIChatService
        print("✅ src.services.openai_chat_service importado com sucesso")
        
        from src.services.groq_chat_service import GroqChatService
        print("✅ src.services.groq_chat_service importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_app_creation():
    """Testar se a aplicação pode ser criada"""
    print("\n🔍 Testando criação da aplicação...")
    
    try:
        from app.main import create_app
        app = create_app()
        print("✅ Aplicação criada com sucesso")
        
        # Verificar se as rotas estão registradas
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        chat_routes = [route for route in routes if '/api/gemini/chat' in route or '/api/openai/chat' in route or '/api/groq/chat' in route]
        
        if chat_routes:
            print(f"✅ Rotas de chat encontradas: {len(chat_routes)} rotas")
            for route in chat_routes:
                print(f"   - {route}")
        else:
            print("❌ Nenhuma rota de chat encontrada")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False

def test_memory_service():
    """Testar se o MemoryService pode ser inicializado"""
    print("\n🔍 Testando MemoryService...")
    
    try:
        from src.services.memory_service import MemoryService
        memory_service = MemoryService()
        print("✅ MemoryService inicializado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar MemoryService: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 Iniciando testes de integração...\n")
    
    tests = [
        test_imports,
        test_app_creation,
        test_memory_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! As correções estão funcionando.")
        return 0
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit(main())

