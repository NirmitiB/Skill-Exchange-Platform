from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.profile import profile
    from app.routes.skills import skills
    from app.routes.exchanges import exchanges
    from app.routes.chatbot import chatbot

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(profile)
    app.register_blueprint(skills)
    app.register_blueprint(exchanges)
    app.register_blueprint(chatbot)

    from app.models import User, Skill, ExchangeRequest

    with app.app_context():
        db.create_all()

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        import traceback
        print("--- GLOBAL 500 ERROR ---")
        traceback.print_exc()
        print("------------------------")
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    return app
