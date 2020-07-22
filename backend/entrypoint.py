from app import create_app, db
from app.models import Actor, Movie, MovieCast

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Actor': Actor, 'Movie': Movie, 'MovieCast': MovieCast}
