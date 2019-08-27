from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_sslify import SSLify


bootstrap = Bootstrap()
db = MongoEngine()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
cache = Cache()
toolbar = DebugToolbarExtension()
# sslify = SSLify()


@login_manager.user_loader
def load_user(user_id):
    from doubanban.models import User
    user = User.objects.get(pk=user_id)
    return user


login_manager.login_view = 'user.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'user.re_authenticate'
login_manager.needs_refresh_message = '为了保护你的账户安全，请重新登录'
login_manager.needs_refresh_message_category = 'warning'
