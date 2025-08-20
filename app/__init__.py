from flask import Flask, jsonify
from .config import get_config
from .extensions import db, ma, migrate, jwt, cache, limiter


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # Extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Blueprints
    from .auth.routes import bp as auth_bp
    from .api.routes import bp as api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Healthcheck
    @app.get('/health')
    @cache.cached(timeout=30)
    def health():
        return jsonify(status='ok'), 200

    # Errores comunes
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error='Not Found'), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify(error='Too Many Requests'), 429

    return app