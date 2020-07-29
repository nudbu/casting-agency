from flask import jsonify
from app.errors import bp

@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource Not Found'
    }), 404


@bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'message': "No permission for requested action"
    }), 403


@bp.app_errorhandler(401)
def forbidden(error):
    return jsonify({
        'success': False,
        'message': "Unauthenticated. Identity not verified"
    }), 401

@bp.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'message': "Unprocessable Entity"
    }), 422

@bp.app_errorhandler(500)
def forbidden(error):
    return jsonify({
        'success': False,
        'message': "Internal Server Error"
    }), 500
    