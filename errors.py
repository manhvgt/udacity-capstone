## Import
import os
from flask import jsonify
from .main import app
from .auth.auth import AuthError

## General Error handling
# error handler for 400 (Bad Request)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

# error handler for 401 (unauthorized)
@app.errorhandler(401)
def handle_unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401, 
        "message": "unauthorized"
    }), 401
    
# error handler for 403 (forbidden)
@app.errorhandler(403)
def handle_forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403, 
        "message": "forbidden"
    }), 403

# error handler for 404 (Not Found)
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

# error handler for 422 (Unprocessable Entity)
@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity'
    }), 422

# error handler for 500 (Internal Server Error)
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

# error handler for AuthError
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response