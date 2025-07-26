#!/usr/bin/env python3
"""
Script de exemplo para configurar chaves de API no banco de dados.
Copie este arquivo para setup_api_keys.py e configure suas chaves reais.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.api_key_service import APIKeyService

def setup_api_keys():
    """Configurar as chaves de API fornecidas pelo usuário"""
    
    # SUBSTITUA PELAS SUAS CHAVES REAIS
    api_keys = {
        "gemini": "",
        "openai": "", 
        "groq": ""
    }
    
    # Usuário padrão para testes
    default_user_id = "1"
    
    print("Configurando chaves de API no banco de dados...")
    
    api_key_service = APIKeyService()
    
    # Configurar cada chave
    for service_name, api_key in api_keys.items():
        if api_key and api_key != f"YOUR_{service_name.upper()}_API_KEY_HERE":
            try:
                api_key_service.save_api_key(default_user_id, service_name, api_key)
                print(f"Chave {service_name} configurada para usuário {default_user_id}")
            except Exception as e:
                print(f"Erro ao configurar chave {service_name}: {e}")
        else:
            print(f"⚠️  Chave {service_name} não configurada (usando placeholder)")
    
    # Verificar status das chaves
    print("\nStatus das chaves configuradas:")
    for service_name in api_keys.keys():
        try:
            key = api_key_service.get_api_key(default_user_id, service_name)
            if key:
                print(f"  {service_name}: ✅ Configurada")
            else:
                print(f"  {service_name}: ❌ Não encontrada")
        except Exception as e:
            print(f"  {service_name}: ❌ Erro: {e}")
    
    print(f"\nChaves de API configuradas com sucesso!")
    print(f"Usuário padrão: {default_user_id}")

if __name__ == "__main__":
    setup_api_keys()

