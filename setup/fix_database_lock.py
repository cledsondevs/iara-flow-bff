#!/usr/bin/env python3
"""
Script para corrigir problemas de bloqueio do banco de dados SQLite
"""
import os
import sys
import sqlite3
import time
import signal
import psutil

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from app.config.settings import Config

def kill_processes_using_db(db_path):
    """Mata processos que estão usando o banco de dados"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                if proc.info['open_files']:
                    for file in proc.info['open_files']:
                        if file.path == db_path:
                            print(f"Matando processo {proc.info['pid']} ({proc.info['name']}) que está usando o banco")
                            proc.kill()
                            time.sleep(1)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"Erro ao verificar processos: {e}")

def fix_database_lock():
    """Corrigir problemas de bloqueio do banco de dados"""
    try:
        db_path = Config.DATABASE_PATH
        print(f"Verificando banco de dados: {db_path}")
        
        # Garantir que o diretório existe
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Diretório criado: {db_dir}")
        
        # Verificar se o arquivo existe
        if not os.path.exists(db_path):
            print("Banco de dados não existe, será criado na próxima inicialização")
            return
        
        # Matar processos que podem estar usando o banco
        kill_processes_using_db(db_path)
        
        # Tentar remover arquivos de lock
        lock_files = [
            db_path + "-wal",
            db_path + "-shm",
            db_path + ".lock"
        ]
        
        for lock_file in lock_files:
            if os.path.exists(lock_file):
                try:
                    os.remove(lock_file)
                    print(f"Arquivo de lock removido: {lock_file}")
                except Exception as e:
                    print(f"Erro ao remover {lock_file}: {e}")
        
        # Testar conexão com o banco
        try:
            conn = sqlite3.connect(db_path, timeout=10)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA cache_size=10000;")
            conn.execute("PRAGMA temp_store=memory;")
            conn.execute("PRAGMA mmap_size=268435456;")  # 256MB
            
            # Testar uma query simples
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tabelas encontradas: {[table[0] for table in tables]}")
            
            cursor.close()
            conn.close()
            print("Conexão com banco de dados testada com sucesso")
            
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("Banco ainda está bloqueado, tentando forçar desbloqueio...")
                
                # Tentar abrir em modo exclusivo para forçar desbloqueio
                try:
                    conn = sqlite3.connect(db_path, timeout=30)
                    conn.execute("BEGIN IMMEDIATE;")
                    conn.rollback()
                    conn.close()
                    print("Desbloqueio forçado com sucesso")
                except Exception as e2:
                    print(f"Erro ao forçar desbloqueio: {e2}")
                    
                    # Como último recurso, fazer backup e recriar
                    backup_path = db_path + ".backup"
                    try:
                        import shutil
                        shutil.copy2(db_path, backup_path)
                        print(f"Backup criado: {backup_path}")
                        
                        # Remover banco original
                        os.remove(db_path)
                        print("Banco original removido")
                        
                        # Restaurar do backup
                        shutil.copy2(backup_path, db_path)
                        print("Banco restaurado do backup")
                        
                    except Exception as e3:
                        print(f"Erro ao fazer backup/restore: {e3}")
            else:
                raise e
                
    except Exception as e:
        print(f"Erro ao corrigir bloqueio do banco: {e}")
        raise

if __name__ == "__main__":
    fix_database_lock()

