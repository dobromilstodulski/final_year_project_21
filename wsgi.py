import os
from app import create_app, socketio
from app.models import initialize

if __name__ == '__main__':
    app = create_app()
    initialize()
    socketio.run(app, port=int(os.environ.get('PORT', '5000')))

else:
    gunicorn = create_app()
