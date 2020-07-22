from flask import Blueprint

bp = Blueprint('auth', __name__)

# can i also call this just auth?
from app.auth import authenti