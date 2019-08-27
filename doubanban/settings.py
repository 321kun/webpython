import os


class BaseConfig(object):
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('doubanban', MAIL_USERNAME)
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

    DOUBANBAN_SUBJECT_PREFIX = '[doubanban]'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    BOOTSTRAP_SERVE_LOCAL = True

    MAX_COLLECTIONS_NUM = 200

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SSL_DISABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(BaseConfig):
    CACHE_NO_NULL_WARNING = True
    CACHE_TYPE = 'simple'


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAX_COLLECTIONS_NUM = 2
    CACHE_NO_NULL_WARNING = True


class ProductionConfig(BaseConfig):
    CACHE_TYPE = 'simple'
    SSL_DISABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
