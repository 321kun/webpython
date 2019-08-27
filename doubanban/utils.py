from urllib.parse import urlparse, urljoin
from flask import current_app, request, url_for, redirect
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from doubanban.models import User


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': str(user.pk), 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or str(user.pk) != data.get('id'):
        return False

    if operation == 'confirm':
        user.confirmed = True
    elif operation == 'reset-password':
        user.set_password(new_password)
    elif operation == 'change_email':
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.objects(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    user.save()
    return True


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default_endpoint='base', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default_endpoint, **kwargs))
