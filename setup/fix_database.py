#!/usr/bin/env python3
"""
Script para corrigir problemas de banco de dados do Iara Flow BFF
"""
import os
import sys
import sqlite3
from pathlib import Path

def fix_database_permissions():
    """Corrige permissões e cria diretórios necessários para o banco de dados"""
    
    # Possíveis caminhos do banco de dados
    possible_paths = [
        "./iara_flow.db",
        "/app/data/iara_flow.db",
        "./data/iara_flow.db",
        os.getenv("DB_PATH", "./iara_flow.db")
    ]
    
    print("🔧 Corrigindo problemas de banco de dados...")
    
    for db_path in possible_paths:
        print(f"\n📁 Verificando caminho: {db_path}")
        
        # Criar diretório se necessário
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
                print(f"✅ Diretório criado: {db_dir}")
            except Exception as e:
                print(f"❌ Erro ao criar diretório {db_dir}: {e}")
                continue
        
        # Testar conexão com o banco
        try:
            # Criar arquivo de banco se não existir
            if not os.path.exists(db_path):
                print(f"📝 Criando arquivo de banco: {db_path}")
                Path(db_path).touch()
            
            # Testar conexão
            conn = sqlite3.connect(db_path)
            conn.execute("SELECT 1")
            conn.close()
            print(f"✅ Banco de dados acessível: {db_path}")
            
            # Definir permissões corretas
            os.chmod(db_path, 0o666)
            if db_dir:
                os.chmod(db_dir, 0o755)
            print(f"✅ Permissões configuradas para: {db_path}")
            
        except Exception as e:
            print(f"❌ Erro ao acessar banco {db_path}: {e}")
    
    print("\n🎯 Correção concluída!")

def create_test_database():
    """Cria um banco de dados de teste para verificar funcionamento"""
    test_db_path = "./test_iara_flow.db"
    
    try:
        print(f"\n🧪 Criando banco de teste: {test_db_path}")
        
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Criar tabela de teste
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                message TEXT
            )
        """)
        
        # Inserir dados de teste
        cursor.execute("INSERT INTO test_table (message) VALUES (?)", ("Teste de funcionamento",))
        
        # Verificar dados
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        if result:
            print(f"✅ Banco de teste criado com sucesso: {result}")
            os.remove(test_db_path)  # Limpar arquivo de teste
            print("🧹 Arquivo de teste removido")
        else:
            print("❌ Erro ao verificar dados no banco de teste")
            
    except Exception as e:
        print(f"❌ Erro ao criar banco de teste: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando correção de problemas de banco de dados...")
    
    fix_database_permissions()
    create_test_database()
    
    print("\n📋 Próximos passos:")
    print("1. Verifique se as variáveis de ambiente estão corretas")
    print("2. Reinicie o serviço Flask")
    print("3. Monitore os logs para verificar se o problema foi resolvido")
    print("\n💡 Dica: Use 'export DB_PATH=/caminho/completo/para/banco.db' para definir o caminho do banco")

