#!/usr/bin/env python3
"""
Script para configurar a chave Gemini padrão para todos os usuários
"""
import os
import sys
import uuid
from datetime import datetime

# Adicionar o diretório app ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.utils.database import get_db_connection

def generate_uuid():
    """Gerar UUID simples para IDs"""
    return str(uuid.uuid4())

def setup_default_gemini_key():
    """Configurar a chave Gemini padrão para todos os usuários"""
    print("🔑 Configurando chave Gemini padrão para todos os usuários...")
    
    # Chave Gemini padrão fornecida pelo usuário
    default_gemini_key = ""
    
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            
            # Buscar todos os usuários existentes
            cur.execute("SELECT id, username FROM users")
            users = cur.fetchall()
            
            if not users:
                print("❌ Nenhum usuário encontrado no banco de dados!")
                return
            
            # Configurar a chave Gemini para cada usuário
            for user in users:
                user_id = str(user["id"])
                username = user["username"]
                
                # Verificar se já existe uma chave Gemini para este usuário
                cur.execute("""
                    SELECT id FROM api_keys 
                    WHERE user_id = ? AND service = 'gemini'
                """, (user_id,))
                
                existing_key = cur.fetchone()
                
                if existing_key:
                    # Atualizar chave existente
                    cur.execute("""
                        UPDATE api_keys 
                        SET api_key = ?, is_active = 1, created_at = ?
                        WHERE user_id = ? AND service = 'gemini'
                    """, (default_gemini_key, datetime.utcnow().isoformat(), user_id))
                    print(f"   ✅ Chave Gemini atualizada para usuário: {username} (ID: {user_id})")
                else:
                    # Inserir nova chave
                    cur.execute("""
                        INSERT INTO api_keys (id, user_id, service, api_key, is_active, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        generate_uuid(),
                        user_id,
                        "gemini",
                        default_gemini_key,
                        True,
                        datetime.utcnow().isoformat()
                    ))
                    print(f"   ✅ Chave Gemini criada para usuário: {username} (ID: {user_id})")
            
            conn.commit()
            print(f"\n🎉 Chave Gemini configurada com sucesso para {len(users)} usuários!")
            print(f"   Chave: {default_gemini_key[:20]}...")
            
    except Exception as e:
        print(f"❌ Erro ao configurar chave Gemini: {e}")

def setup_fallback_gemini_config():
    """Configurar chave Gemini como fallback no arquivo de configuração"""
    print("\n🔧 Configurando chave Gemini como fallback no sistema...")
    
    try:
        # Ler o arquivo de configuração atual
        config_path = "app/config/settings.py"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já existe uma configuração de GEMINI_API_KEY
        if "GEMINI_API_KEY" not in content:
            # Adicionar a configuração da chave Gemini
            gemini_config = '''
    # Chave Gemini padrão (fallback)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDpLNBaYVrLSzxWj0kLD3v7n75pR5O-AfM")
'''
            
            # Encontrar onde inserir (após outras configurações)
            if "class Config:" in content:
                # Inserir após a definição da classe Config
                content = content.replace(
                    "class Config:",
                    f"class Config:{gemini_config}"
                )
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("   ✅ Chave Gemini adicionada ao arquivo de configuração")
            else:
                print("   ⚠️  Não foi possível encontrar a classe Config no arquivo de configuração")
        else:
            print("   ✅ Chave Gemini já está configurada no arquivo de configuração")
            
    except Exception as e:
        print(f"   ❌ Erro ao configurar fallback: {e}")

def main():
    """Função principal"""
    print("🚀 Configurando chave Gemini padrão para o sistema...")
    print("=" * 60)
    
    try:
        # Configurar chave para usuários existentes
        setup_default_gemini_key()
        
        # Configurar fallback no sistema
        setup_fallback_gemini_config()
        
        print("\n" + "=" * 60)
        print("🎉 Configuração da chave Gemini concluída com sucesso!")
        print("\nAgora todos os usuários podem usar o chat com Gemini sem configurar chaves individuais.")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
