from app import create_app
from app.extensions import db
from app.models import User, Item

app = create_app()

# Ej: flask shell
@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User, 'Item': Item}