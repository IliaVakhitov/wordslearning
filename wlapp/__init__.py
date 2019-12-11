from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login = LoginManager()
bootstrap = Bootstrap()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    login.init_app(app)
    bootstrap.init_app(app)

    from wlapp.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from wlapp.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from wlapp.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
