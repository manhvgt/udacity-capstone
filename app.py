## Imports
from flask import Flask
from flask_cors import CORS
from .database.models import setup_db


## Create app and config
app = Flask(__name__)
with app.app_context():
    setup_db(app)

# Set up CORS. Allow '*' for origins.
CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    app.run()
