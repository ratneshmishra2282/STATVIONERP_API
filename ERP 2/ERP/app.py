from flask import Flask
from config import Config
from extensions import db, jwt, mongo, api
from resources.resource_routes import register_resources


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mongo.init_app(app)

    api.init_app(app)

    register_resources(api)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)