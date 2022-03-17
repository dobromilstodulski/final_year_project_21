from app import create_app, socketio
from app.models import initialize

if __name__ == '__main__':
    app = create_app()
    initialize()
    socketio.run(app, debug=True)