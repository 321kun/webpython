from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from doubanban.models import User


class MovieForm(FlaskForm):
    title = StringField('电影名称：', validators=[DataRequired(message='不能为空'), Length(1, 50)],
                        render_kw={'placeholder': '电影名称，不能有空格，不然会被截断'})
    rate = StringField('评价分数：', render_kw={'placeholder': '评价分数，小数点最多一位'})
    year = StringField('电影年份：', render_kw={'placeholder': '格式为（xxxx），如（2019）'})
    people = IntegerField('评价人数：', render_kw={'placeholder': '评价人数，正整数，不能带其他'})
    country = StringField('出版国家：', validators=[Length(0, 50)], render_kw={'placeholder': '国家，可以带空格'})
    img = StringField('电影图片：', validators=[DataRequired(message='不能为空'), Length(1, 50)],
                      render_kw={'placeholder': '格式为pxxxxxxxxxx.jpg，x为数字0～9'})
    url = StringField('电影链接：', validators=[DataRequired(message='不能为空'), Length(1, 300)],
                      render_kw={'placeholder': '复制电影链接，来源不限'})
    category = StringField('分类：', render_kw={'placeholder': '只允许填写以下三种之一：热度，时间，评价'})
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email(message='请输入邮箱格式')])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email(message='请输入邮箱格式')])
    username = StringField('帐号', validators=[DataRequired(), Length(1, 20),
                           Regexp('^[a-zA-Z0-9]*$', message='帐号只能包含字母和数字')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.objects(email=field.data.lower()).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.objects(username=field.data).first():
            raise ValidationError('帐号已经存在')


class ForgetPasswordForm(FlaskForm):
    email = StringField('请输入邮箱', validators=[DataRequired(), Length(1, 254), Email(message='请输入邮箱格式')])
    submit = SubmitField('提交')


class ResetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email(message='请输入邮箱格式')])
    password = PasswordField('新密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired(), Length(1, 254), Email(message='请输入邮箱格式')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.objects(email=field.data.lower()).first():
            raise ValidationError('该邮箱已被注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class UpgradeForm(FlaskForm):
    is_admin = IntegerField('帐号级别：', validators=[DataRequired()], render_kw={'placeholder': '1为普通会员，2为普通管理员，3为高级管理员'})
    submit = SubmitField('修改')
