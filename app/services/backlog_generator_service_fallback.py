"""
Serviço fallback para geração automática de itens de backlog baseado em análise de reviews
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict

class BacklogGeneratorServiceFallback:
    def __init__(self):
        self.database_path = os.getenv("DB_PATH", "./iara_flow.db")
    
    def generate_fallback_backlog(self, package_name: str = None) -> Dict[str, Any]:
        """Gerar backlog básico usando dados mock"""
        try:
            # Dados mock baseados em problemas comuns de apps
            mock_backlog_items = [
                {
                    "title": "Corrigir travamento durante login",
                    "description": "Usuários relatam travamento frequente ao tentar fazer login. Problema crítico que afeta a experiência do usuário.",
                    "priority": 5,
                    "category": "bug",
                    "frequency": 15,
                    "sentiment_score": -0.8,
                    "status": "pending"
                },
                {
                    "title": "Melhorar velocidade de carregamento",
                    "description": "App demora muito para carregar, especialmente na tela inicial. Usuários reclamam da lentidão.",
                    "priority": 4,
                    "category": "performance",
                    "frequency": 12,
                    "sentiment_score": -0.6,
                    "status": "pending"
                },
                {
                    "title": "Adicionar modo escuro",
                    "description": "Múltiplos usuários solicitaram a implementação de modo escuro para melhor experiência noturna.",
                    "priority": 3,
                    "category": "feature",
                    "frequency": 8,
                    "sentiment_score": 0.2,
                    "status": "pending"
                },
                {
                    "title": "Corrigir erro de sincronização",
                    "description": "Dados não sincronizam corretamente entre dispositivos, causando perda de informações.",
                    "priority": 4,
                    "category": "bug",
                    "frequency": 10,
                    "sentiment_score": -0.7,
                    "status": "pending"
                },
                {
                    "title": "Melhorar interface do usuário",
                    "description": "Interface confusa e pouco intuitiva. Usuários têm dificuldade para navegar.",
                    "priority": 3,
                    "category": "ui/ux",
                    "frequency": 7,
                    "sentiment_score": -0.4,
                    "status": "pending"
                }
            ]
            
            return {
                "generated_items": len(mock_backlog_items),
                "saved_items": len(mock_backlog_items),
                "backlog_items": mock_backlog_items,
                "summary": {
                    "total_items": len(mock_backlog_items),
                    "high_priority": len([item for item in mock_backlog_items if item["priority"] >= 4]),
                    "categories": {
                        "bug": len([item for item in mock_backlog_items if item["category"] == "bug"]),
                        "feature": len([item for item in mock_backlog_items if item["category"] == "feature"]),
                        "performance": len([item for item in mock_backlog_items if item["category"] == "performance"]),
                        "ui/ux": len([item for item in mock_backlog_items if item["category"] == "ui/ux"])
                    }
                },
                "package_name": package_name or "com.itau.investimentos",
                "analysis_period_days": 7,
                "fallback_mode": True,
                "message": "Backlog gerado usando dados de fallback devido a problemas na análise de reviews"
            }
            
        except Exception as e:
            return {
                "error": f"Erro no fallback de geração de backlog: {str(e)}",
                "generated_items": 0,
                "saved_items": 0,
                "backlog_items": [],
                "fallback_mode": True
            }
    
    def process_reviews_to_backlog(self, package_name: str = None, 
                                 days: int = 7) -> Dict[str, Any]:
        """Processo completo usando fallback"""
        return self.generate_fallback_backlog(package_name)

