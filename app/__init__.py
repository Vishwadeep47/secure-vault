"""SecureVault application factory."""
from flask import Flask, jsonify

from app.config import Config


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    # Keys are loaded once at startup and kept in memory (never in the database).
    from app.crypto import keys

    secrets_dir = app.config["SECRETS_DIR"]
    app.config["JWT_SECRET"] = keys.load_or_create_secret("jwt_secret", secrets_dir)
    app.config["AES_KEY"] = keys.load_or_create_secret("vault_key", secrets_dir)

    from app import db

    db.init_app(app)

    from app.auth.routes import auth_bp

    from app.admin.routes import admin_bp
    from app.vault.cards import cards_bp
    from app.vault.images import images_bp
    from app.vault.notes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(cards_bp)
    app.register_blueprint(admin_bp)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(error="File too large"), 413

    return app
