from app import create_app
from app.models import initialize

if __name__ == '__main__':
    app = create_app()
    initialize()
    app.run(debug=True)