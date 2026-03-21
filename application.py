from flask import Flask
from config import Config
from extensions import db, mongo
from flask_restful import Api
from resources.resource_routes import register_resources
from resources.organization_resource import OrganizationRegisterResource
print("Loaded resource:", OrganizationRegisterResource)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mongo.init_app(app)

    api = Api(app)

    register_resources(api)

    with app.app_context():
        db.create_all()

    print(app.url_map)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)