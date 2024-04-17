from flask import request, abort, jsonify

def parse_request(required_fields):
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Missing JSON data")
    missing_fields = [field for field in required_fields if field not in json_data or not json_data[field]]
    if missing_fields:
        abort(400, description=f"Missing fields: {', '.join(missing_fields)}")
    return json_data

def standard_response(status_code, message, data=None):
    response = {
        'status': 'success' if 200 <= status_code < 300 else 'error',
        'type': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def get_jwt_from_request(request):
    auth_header = request.headers.get('Authorization', None)
    print(f"auth_header {auth_header} ------------------")
    if not auth_header:
        raise ValueError("No Authorization header provided")

    parts = auth_header.split()
    if parts[0].lower() != "bearer":
        raise ValueError("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise ValueError("Token not found")
    elif len(parts) > 2:
        raise ValueError("Authorization header must be Bearer token")

    token = parts[1]
    return token
