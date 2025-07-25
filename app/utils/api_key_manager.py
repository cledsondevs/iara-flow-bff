from app.services.api_key_service import APIKeyService

class APIKeyManager:
    def __init__(self):
        self.api_key_service = APIKeyService()
    
    def setup_default_keys(self, user_id: str, keys: dict):
        """Configurar chaves padrão para um usuário"""
        for service, key in keys.items():
            if key:
                self.api_key_service.save_api_key(user_id, service, key)
                print(f"Chave {service} configurada para usuário {user_id}")
    
    def get_all_keys(self, user_id: str) -> dict:
        """Obter todas as chaves de um usuário"""
        services = ["openai", "gemini", "groq"]
        keys = {}
        for service in services:
            key = self.api_key_service.get_api_key(user_id, service)
            keys[service] = key
        return keys
    
    def validate_keys(self, user_id: str) -> dict:
        """Validar se as chaves estão configuradas"""
        keys = self.get_all_keys(user_id)
        validation = {}
        for service, key in keys.items():
            validation[service] = bool(key)
        return validation

