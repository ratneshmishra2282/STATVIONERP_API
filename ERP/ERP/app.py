
from flask import Flask
from config import Config
from extensions import db, jwt, mongo
from resources.auth_resource import auth_bp
from resources.student_resource import student_bp
from resources.fee_resource import fee_bp
from resources.organization_resource import org_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mongo.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(student_bp, url_prefix="/api")
    app.register_blueprint(fee_bp, url_prefix="/api")
    app.register_blueprint(org_bp, url_prefix="/api")

    # with app.app_context():
    #     db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
