from flask import Blueprint, request, jsonify
from app.modules.scraping.google_play import GooglePlayScrapingService
from app.modules.scraping.apple_store import AppleAppStoreScrapingService
from app.modules.sentiment.analysis import SentimentAnalysisService
from app.auth.middleware import require_auth
import os

data_analysis_bp = Blueprint("data_analysis", __name__)

# Inicializa os serviços
google_play_scraper = GooglePlayScrapingService()
apple_store_scraper = AppleAppStoreScrapingService()
sentiment_analyzer = SentimentAnalysisService(api_key=os.getenv("GEMINI_API_KEY"))

@data_analysis_bp.route("/scraping/google-play/<string:app_id>", methods=["POST"])
@require_auth
def scrape_google_play(app_id):
    """Endpoint para fazer scraping de reviews do Google Play"""
    try:
        reviews, _ = google_play_scraper.get_app_reviews(app_id, count=100) # Coleta 100 reviews
        return jsonify({"app_id": app_id, "store": "google_play", "reviews_count": len(reviews), "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_analysis_bp.route("/scraping/apple-store/<string:app_id>", methods=["POST"])
@require_auth
def scrape_apple_store(app_id):
    """Endpoint para fazer scraping de reviews da Apple Store"""
    try:
        reviews = apple_store_scraper.get_app_reviews(app_id, count=100) # Coleta 100 reviews
        return jsonify({"app_id": app_id, "store": "apple_store", "reviews_count": len(reviews), "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_analysis_bp.route("/sentiment/analyze", methods=["POST"])
@require_auth
def analyze_sentiment():
    """Endpoint para analisar sentimentos de reviews"""
    try:
        data = request.get_json()
        if not data or "reviews" not in data:
            return jsonify({"error": "Dados JSON com 'reviews' são obrigatórios"}), 400
        
        reviews_to_analyze = data["reviews"]
        if not isinstance(reviews_to_analyze, list):
            return jsonify({"error": "'reviews' deve ser uma lista de objetos com 'id' e 'content'"}), 400

        # Adiciona um ID se não existir (para o caso de reviews virem sem ID)
        for i, review in enumerate(reviews_to_analyze):
            if "id" not in review:
                review["id"] = f"review_{i}"
            if "content" not in review:
                return jsonify({"error": f"Review {review.get('id', i)} não possui 'content'"}), 400

        analyzed_reviews = sentiment_analyzer.analyze_batch_reviews(reviews_to_analyze)
        
        return jsonify({"analyzed_reviews": analyzed_reviews}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


