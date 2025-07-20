"""
Modelos de dados para o sistema de análise de reviews
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class SentimentType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class StoreType(Enum):
    GOOGLE_PLAY = "google_play"
    APP_STORE = "app_store"

@dataclass
class Review:
    """Modelo para um review de aplicativo"""
    id: Optional[str] = None
    package_name: str = ""
    store: StoreType = StoreType.GOOGLE_PLAY
    review_id: str = ""
    user_name: str = ""
    rating: int = 0
    content: str = ""
    date: Optional[datetime] = None
    sentiment: Optional[SentimentType] = None
    topics: List[str] = None
    keywords: List[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()

@dataclass
class BacklogItem:
    """Modelo para um item de backlog gerado automaticamente"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    priority: int = 1  # 1-5, sendo 5 a maior prioridade
    category: str = ""  # bug, feature, improvement, etc.
    source_reviews: List[str] = None  # IDs dos reviews que geraram este item
    sentiment_score: float = 0.0
    frequency: int = 1  # Quantas vezes este problema foi mencionado
    status: str = "pending"  # pending, in_progress, done
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.source_reviews is None:
            self.source_reviews = []
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

@dataclass
class SentimentPattern:
    """Modelo para padrões de sentimento aprendidos"""
    id: Optional[str] = None
    package_name: str = ""
    topic: str = ""
    sentiment_trend: List[Dict[str, Any]] = None  # Histórico de sentimento ao longo do tempo
    keywords: List[str] = None
    frequency: int = 0
    last_seen: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.sentiment_trend is None:
            self.sentiment_trend = []
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}
        if self.last_seen is None:
            self.last_seen = datetime.utcnow()

@dataclass
class AppConfig:
    """Configuração para coleta de reviews de um aplicativo"""
    id: Optional[str] = None
    package_name: str = ""
    app_name: str = ""
    stores: List[StoreType] = None
    collection_frequency: int = 6  # horas
    is_active: bool = True
    last_collection: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.stores is None:
            self.stores = [StoreType.GOOGLE_PLAY]
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()

