from flask import request, jsonify

def validation_middleware():
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'message': 'Invalid input'}), 400
