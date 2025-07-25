from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services.api_key_service import APIKeyService

api_key_bp = Blueprint("api_keys", __name__)
api_key_service = APIKeyService()

@api_key_bp.route("/keys", methods=["POST"])
@cross_origin()
def save_api_key():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        service_name = data.get("service_name")
        api_key = data.get("api_key")

        if not user_id or not service_name or not api_key:
            return jsonify({"error": "user_id, service_name e api_key são obrigatórios"}), 400

        api_key_service.save_api_key(user_id, service_name, api_key)
        return jsonify({"message": "API Key salva com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_key_bp.route("/keys/<string:user_id>/<string:service_name>", methods=["GET"])
@cross_origin()
def get_api_key(user_id, service_name):
    try:
        key = api_key_service.get_api_key(user_id, service_name)
        if key:
            return jsonify({"api_key": key}), 200
        return jsonify({"error": "API Key não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_key_bp.route("/api/keys", methods=["DELETE"])
@cross_origin()
def delete_api_key():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        service_name = data.get("service_name")

        if not user_id or not service_name:
            return jsonify({"error": "user_id e service_name são obrigatórios"}), 400

        api_key_service.delete_api_key(user_id, service_name)
        return jsonify({"message": "API Key deletada com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


