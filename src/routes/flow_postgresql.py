from flask import Blueprint, request, jsonify
from src.services.postgresql_service import PostgreSQLService

flow_postgresql_bp = Blueprint('flow_postgresql_bp', __name__)
postgresql_service = PostgreSQLService()

@flow_postgresql_bp.route('/flows', methods=['POST'])
def create_flow():
    data = request.json
    result = postgresql_service.create_flow(data)
    if result['success']:
        return jsonify(result['flow']), 201
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/flows', methods=['GET'])
def list_flows():
    result = postgresql_service.list_flows()
    if result['success']:
        return jsonify(result['flows']), 200
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/flows/<flow_id>', methods=['GET'])
def get_flow(flow_id):
    result = postgresql_service.get_flow(flow_id)
    if result['success']:
        return jsonify(result['flow']), 200
    return jsonify({'error': result['error']}), 404

@flow_postgresql_bp.route('/flows/<flow_id>', methods=['PUT'])
def update_flow(flow_id):
    data = request.json
    result = postgresql_service.update_flow(flow_id, data)
    if result['success']:
        return jsonify(result['flow']), 200
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/flows/<flow_id>', methods=['DELETE'])
def delete_flow(flow_id):
    result = postgresql_service.delete_flow(flow_id)
    if result['success']:
        return jsonify({'message': result['message']}), 200
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/executions', methods=['POST'])
def create_execution():
    data = request.json
    result = postgresql_service.create_execution(data)
    if result['success']:
        return jsonify(result['execution']), 201
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/executions/<execution_id>', methods=['PUT'])
def update_execution(execution_id):
    data = request.json
    result = postgresql_service.update_execution(execution_id, data)
    if result['success']:
        return jsonify(result['execution']), 200
    return jsonify({'error': result['error']}), 400

@flow_postgresql_bp.route('/executions/<execution_id>', methods=['GET'])
def get_execution(execution_id):
    result = postgresql_service.get_execution(execution_id)
    if result['success']:
        return jsonify(result['execution']), 200
    return jsonify({'error': result['error']}), 404

@flow_postgresql_bp.route('/flows/<flow_id>/executions', methods=['GET'])
def get_flow_executions(flow_id):
    result = postgresql_service.get_flow_executions(flow_id)
    if result['success']:
        return jsonify(result['executions']), 200
    return jsonify({'error': result['error']}), 400


