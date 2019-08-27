from flask import Blueprint, render_template, url_for, redirect, flash, abort
from doubanban.models import User
from flask_login import login_user, logout_user, login_required, \
                        current_user, login_fresh, confirm_login, fresh_login_required
from doubanban.utils import generate_token, validate_token, redirect_back
from doubanban.forms import LoginForm, RegisterForm, ForgetPasswordForm,\
                         ResetPasswordForm, ChangeEmailForm, ChangePasswordForm
from doubanban.emails import send_confirm_email, send_reset_password_email, send_change_email_email


user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            if user.validate_password(form.password.data):
                login_user(user, form.remember_me.data)
                flash('欢迎回来.', 'info')
                return redirect_back()
            else:
                flash('密码错误', 'warning')
                return redirect(url_for('user.login'))
        else:
            flash('帐号不存在', 'warning')
            return redirect(url_for('user.login'))
    return render_template('user/login.html', form=form)


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功登出', 'info')
    return redirect(url_for('base'))


@user_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        flash('活跃用户不需要重新登录', 'info')
        return redirect(url_for('base'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('user/login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        user = User(email=email, username=username)
        user.set_password(form.password.data)
        user.judge_is_admin()
        user.save()
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('确认邮件已发送，请检查您的收件箱', 'info')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('base'))

    if validate_token(user=current_user, token=token, operation='confirm'):
        flash('确认成功', 'success')
        return redirect(url_for('base'))
    else:
        flash('无效或者过期的链接', 'danger')
        return redirect(url_for('user.resend_confirm_email'))


@user_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        flash('帐号已认证', 'info')
        return redirect(url_for('base'))

    token = generate_token(user=current_user, operation='confirm')
    send_confirm_email(user=current_user, token=token)
    flash('新的确认邮件已发送，请及时确认', 'info')
    return redirect(url_for('base'))


@user_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('base'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation='reset-password')
            send_reset_password_email(user=user, token=token)
            flash('重置密码邮件已发送，请到邮箱中确认', 'info')
            return redirect(url_for('user.login'))
        flash('该邮箱不存在', 'warning')
        return redirect(url_for('user.forget_password'))
    return render_template('user/reset_password.html', form=form)


@user_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('base'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data.lower()).first()
        if user is None:
            flash('邮箱不存在', 'warning')
            return redirect(url_for('base'))
        if validate_token(user=user, token=token, operation='reset-password',
                          new_password=form.password.data):
            flash('重置密码成功', 'success')
            return redirect(url_for('user.login'))
        else:
            flash('无效或者过期的链接', 'danger')
            return redirect(url_for('user.forget_password'))
    return render_template('user/reset_password.html', form=form)


@user_bp.route('/index/<username>', methods=['GET', 'POST'])
@login_required
def index(username):
    if username == current_user.username and current_user.is_authenticated:
        return render_template('user/index.html')
    else:
        abort(404)


@user_bp.route('<username>/change-password', methods=['GET', 'POST'])
@fresh_login_required
def change_password(username):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.validate_password(form.old_password.data):
            current_user.set_password(form.password.data)
            current_user.save()
            flash('密码修改成功', 'success')
            return redirect(url_for('user.index', username=current_user.username))
        else:
            flash('旧密码不正确', 'warning')
    return render_template('user/change_password.html', form=form)


@user_bp.route('<username>/change-email', methods=['GET', 'POST'])
@fresh_login_required
def change_email_request(username):
    form = ChangeEmailForm()
    if form.validate_on_submit():
        token = generate_token(user=current_user, operation='change_email', new_email=form.email.data.lower())
        send_change_email_email(user=current_user, token=token, to=form.email.data)
        flash('重置邮箱邮件已发送，请到邮箱中确认', 'info')
        return redirect(url_for('user.index', username=current_user.username))
    return render_template('user/change_email.html', form=form)


@user_bp.route('/change-email/<token>')
@login_required
def change_email(token):
    if validate_token(user=current_user, token=token, operation='change_email'):
        flash('邮箱更新成功', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    else:
        flash('无效或者过期的链接', 'warning')
        return redirect(url_for('user.change_email_request', username=current_user.username))
