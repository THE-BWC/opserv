import time
from datetime import timedelta

import arrow
from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    jsonify,
    session,
    g,
)

from flask_cors import CORS
from flask_login import current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from app.auth.base import auth_bp
from app.config import BaseConfig
from app.dashboard import dashboard_bp
from app.database.models import Session, db
from app.storage.storage import storage
from flask_migrate import Migrate
from app.auth.auth import login_manager, oauth
from app.limiter import limiter
from app.log import LOG


def create_app() -> Flask:
    app = Flask(__name__)
    # Deployed behind NGINX
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    app.url_map.strict_slashes = False

    app.config["SQLALCHEMY_DATABASE_URI"] = BaseConfig.DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # enable to print all queries generated by SQLAlchemy
    app.config["SQLALCHEMY_ECHO"] = False

    app.secret_key = BaseConfig.FLASK_SECRET

    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.config["SESSION_COOKIE_NAME"] = BaseConfig.SESSION_COOKIE_NAME
    if BaseConfig.URL.startswith("https"):
        app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    limiter.init_app(app)

    setup_error_page(app)

    init_extensions(app)
    register_blueprints(app)
    set_index_page(app)
    jinja2_filter(app)

    setup_favicon_route(app)

    init_storage()
    init_database(app, db)
    register_custom_commands(app)

    # Enable CORS on /api endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Set session to permanent so user stays signed in after quitting browser
    # Cookie is valid for 7 days
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permenant_session_lifetime = timedelta(days=7)

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    @app.route("/health", methods=["GET"])
    def healthcheck():
        return "success", 200

    return app


def init_database(app, database):
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, database)


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)


def set_index_page(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        else:
            return redirect(url_for("auth.login"))

    @app.before_request
    def before_request():
        if not request.path.startswith("/static") and not request.path.startswith(
            "/admin/static"
        ):
            g.start_time = time.time()

    @app.after_request
    def after_request(res):
        if (
            not request.path.startswith("/static")
            and not request.path.startswith("/admin/static")
            and not request.path.startswith("/git")
            and not request.path.startswith("/favicon.ico")
            and not request.path.startswith("/health")
        ):
            start_time = g.start_time or time.time()
            LOG.d(
                "%s %s %s %s %s, takes %s",
                request.remote_addr,
                request.method,
                request.path,
                request.args,
                res.status_code,
                time.time() - start_time,
            )

        return res


def get_current_user():
    try:
        return g.user
    except AttributeError:
        return current_user


def setup_error_page(app):
    @app.errorhandler(400)
    def bad_request(e):
        if request.path.startswith("/api/"):
            return jsonify(error="Bad Request"), 400
        else:
            return render_template("error/400.html"), 400


def setup_favicon_route(app):
    @app.route("/favicon.ico")
    def favicon():
        return redirect(url_for("static", filename="favicon.ico"))


def jinja2_filter(app):
    def format_datetime(value):
        dt = arrow.get(value).to("America/New_York")
        return dt.format("YYYY-MM-DD HH:mm ZZZ")

    app.jinja_env.filters["dt"] = format_datetime

    @app.context_processor
    def inject_stage_and_region():
        now = arrow.now()
        return dict(
            YEAR=now.year,
            NOW=now,
            URL=BaseConfig.URL,
            LANDING_PAGE_URL=BaseConfig.LANDING_PAGE_URL,
            STATUS_PAGE_URL=BaseConfig.STATUS_PAGE_URL,
            CANONICAL_URL=f"{BaseConfig.URL}{request.path}",
            BRAND_NAME=BaseConfig.BRAND_NAME,
            BRAND_URL=BaseConfig.BRAND_URL,
            SOCIALS=BaseConfig.SOCIALS,
            IMAGE_URL=BaseConfig.IMAGE_URL,
            IMAGE_PATHS=BaseConfig.IMAGE_PATHS,
        )


def init_storage():
    stor = storage(BaseConfig.STORAGE_TYPE)
    stor.init()


def init_extensions(app: Flask):
    login_manager.init_app(app)
    oauth.init_app(app)


def register_custom_commands(app):
    @app.cli.command("seed")
    def seed():
        from seeders import ranks, users, games, operations

        ranks.seed_ranks()
        users.seed_users()
        games.seed_games()
        games.seed_member_games()
        operations.seed_operation_types()
        operations.seed_operations()


def local_main():
    BaseConfig.COLOR_LOG = True
    app = create_app()

    app.debug = True

    app.run(debug=True, port=5000, host="0.0.0.0")

    # LOG.d("Enable HTTPS")
    # import ssl
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain("local_date/cert.pem", "local_data/key.pem")
    # app.run(debug=True, port=5000, host="0.0.0.0", ssl_context=context)


if __name__ == "__main__":
    local_main()
