from flask import jsonify
from app.errors import bp
from app.auth.auth import AuthError

@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'status': 404,
        'description': 'Resource Not Found'
    }), 404


@bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'status': 403,
        'description': "No permission for requested action"
    }), 403


@bp.app_errorhandler(401)
def forbidden(error):
    return jsonify({
        'success': False,
        'status': 401,
        'description': "Unauthenticated. Identity not verified"
    }), 401

@bp.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'status': 422,
        'description': "Unprocessable Entity"
    }), 422

@bp.app_errorhandler(500)
def forbidden(error):
    return jsonify({
        'success': False,
        'status': 500,
        'description': "Internal Server Error"
    }), 500
    

@bp.app_errorhandler(AuthError)
def auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response