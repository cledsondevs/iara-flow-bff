#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/ubuntu/iara-flow-bff')

import sqlite3
import bcrypt
from app.config.settings import Config

def fix_user_passwords():
    """Verificar e corrigir usuários com hashes de senha inválidos"""
    print("=== Verificando e Corrigindo Hashes de Senha ===")
    
    try:
        db_path = Config.DATABASE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Buscar todos os usuários
        cur.execute("SELECT id, username, password_hash FROM users")
        users = cur.fetchall()
        
        print(f"Encontrados {len(users)} usuários no banco")
        
        for user in users:
            user_id = user['id']
            username = user['username']
            password_hash = user['password_hash']
            
            print(f"\nVerificando usuário: {username} (ID: {user_id})")
            print(f"Hash atual: {password_hash[:50]}...")
            
            # Tentar verificar se o hash é válido
            try:
                # Testar com uma senha dummy para ver se o hash é válido
                test_password = "test123"
                if isinstance(password_hash, str):
                    password_hash_bytes = password_hash.encode('utf-8')
                else:
                    password_hash_bytes = password_hash
                
                # Se conseguir fazer checkpw sem erro, o hash é válido
                bcrypt.checkpw(test_password.encode('utf-8'), password_hash_bytes)
                print(f"✅ Hash válido para {username}")
                
            except (ValueError, TypeError) as e:
                print(f"❌ Hash inválido para {username}: {e}")
                
                # Recriar hash com senha padrão (admin)
                new_password = "admin"  # Senha padrão
                new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Atualizar no banco
                cur.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (new_hash, user_id)
                )
                
                print(f"✅ Hash corrigido para {username} com senha padrão 'admin'")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Verificação e correção concluída!")
        
    except Exception as e:
        print(f"❌ Erro durante a correção: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_user_passwords()
