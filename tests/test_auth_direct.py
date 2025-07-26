#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

import sqlite3
import bcrypt
from app.config.settings import Config

def test_auth_direct():
    """Testar autenticação diretamente no banco"""
    print("=== Teste Direto de Autenticação ===")
    
    try:
        db_path = Config.DATABASE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Buscar usuário admin
        username = "admin"
        password = "admin"
        
        cur.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cur.fetchone()
        
        if not user:
            print("❌ Usuário não encontrado")
            return False
        
        print(f"✅ Usuário encontrado: ID {user['id']}")
        print(f"Hash armazenado: {user['password_hash'][:50]}...")
        
        # Testar verificação de senha
        try:
            stored_hash = user['password_hash']
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            
            password_check = bcrypt.checkpw(password.encode("utf-8"), stored_hash)
            
            if password_check:
                print("✅ Senha verificada com sucesso!")
                return True
            else:
                print("❌ Senha incorreta")
                return False
                
        except (ValueError, TypeError) as e:
            print(f"❌ Erro ao verificar senha: {e}")
            return False
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_auth_direct()
