from app import app, db
from app.models import Actor, Movie, MovieCast

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Actor': Actor, 'Movie': Movie, 'MovieCast': MovieCast}
