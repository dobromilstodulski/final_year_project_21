import os
from app import create_app, socketio
from app.models import initialize

if __name__ == '__main__':
    app = create_app()
    initialize()
    socketio.run(app, cors_allowed_origins=['http://url', 'https://url'])

else:
    gunicorn = create_app()
