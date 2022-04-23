from app import create_app, socketio
from app.models import initialize

if __name__ == '__main__':
    app = create_app()
    initialize()
    socketio.run(app, host='0.0.0.0', port=5004)

else:
    gunicorn = create_app()
