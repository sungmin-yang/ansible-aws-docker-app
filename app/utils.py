from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import stock_api_logger

logger = stock_api_logger.log_factory().getLogger()

def get_flask_app(user: str,
                  passwd: str,
                  host: str,
                  port: int,
                  db: str,
                  app_key: str) -> Flask:
    logger.info(f"Creating flask app, user: {user}, host: {host}, port: {port}, db: {db} ...")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = app_key

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    app.register_error_handler(404, page_not_found)

    return app


def setup_database(app: Flask, db: SQLAlchemy):
    logger.info("Database is setting up.")
    with app.app_context():
        db.create_all()
    logger.info("Database is all set up.")
