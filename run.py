from fortunesite import create_app, db
from fortunesite.models import User, Fortune

application = create_app()
app = application


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Fortune': Fortune}
