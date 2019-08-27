import os
from flask import Flask, render_template, request

from doubanban.blueprints.admin import admin_bp
from doubanban.blueprints.movie import movie_bp
from doubanban.blueprints.user import user_bp
from doubanban.blueprints.feature import feature_bp

from doubanban.extensions import db, bootstrap, login_manager, mail, csrf, cache, toolbar  # sslify
from doubanban.settings import config

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('doubanban')
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config['MONGODB_SETTINGS'] = {'host': os.getenv('DATABASE_URL')}
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_base(app)
    register_filters(app)
    register_errorhandlers(app)
    register_logging(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    toolbar.init_app(app)
    # sslify.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(movie_bp, url_prefix='/movie')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(feature_bp, url_prefix='/feature')


def register_base(app):
    @app.route('/', methods=['GET', 'POST'])
    def base():
        return render_template('base.html')


def register_filters(app):
    @app.template_filter()
    def chinese(s):
        S = s[:(s.index(' '))] if s.count(' ') else s
        return S


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['ADMIN_EMAIL'],
        subject='豆半半错误',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
