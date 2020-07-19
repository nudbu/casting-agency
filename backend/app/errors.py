from flask import jsonify
from app import app

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error message': 'Resource Not Found'
    }), 404


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'error message': "No permission for requested action"
    }), 403


@app.errorhandler(401)
def forbidden(error):
    return jsonify({
        'error message': "Unauthenticated. Identity not verified"
    }), 401


@app.errorhandler(500)
def forbidden(error):
    return jsonify({
        'error message': "Internal Server Error"
    }), 500