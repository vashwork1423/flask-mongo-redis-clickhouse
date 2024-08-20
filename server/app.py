from flask import Flask
from config import Config
from controllers.book_controller import book_bp
from middleware.validation_middleware import validation_middleware
from extensions import cache

def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config.from_object(Config)
    cache.init_app(app)

    # Регистрация Blueprints
    app.register_blueprint(book_bp, url_prefix='/book')

    # Middleware
    app.before_request(validation_middleware)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
