from flask import url_for
from tests.base import BaseTestCase
from doubanban.models import User, Movie
from doubanban.utils import generate_token, validate_token

class AdminTestCase(BaseTestCase):

    def test_login_page(self):
        res = self.client.get(url_for('user.login'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('忘记密码', data)

    def test_login(self):
        res = self.login()
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('欢迎回来', data)

    def test_wrong_login(self):
        email = 'example@163.com'
        email1 = 'exampleexample@163.com'
        password = '456789'

        res = self.client.post(url_for('user.login'), 
                               data=dict(email=email, password=password), 
                               follow_redirects=True
                               )
        data = res.get_data(as_text=True)
        res1 = self.client.post(url_for('user.login'), 
                               data=dict(email=email1, password=password), 
                               follow_redirects=True
                               )
        data1 = res1.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('密码错误', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('帐号不存在', data1)

    def test_logout(self):
        self.login()
        res = self.logout()
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('成功登出', data)

    def test_user_index(self):
        movie = Movie.objects(category='热度').order_by('id').first()
        self.user.is_admin = 1
        self.user.update(push__collections=movie.id)
        self.user.save()
        self.login()
        res = self.client.get(url_for('user.index', username='exam'))
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('user.index', username='examexamexam'))
        data1 = res1.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(movie.img, data)
        self.assertEqual(res1.status_code, 404)
        self.assertIn('没有找到该网页', data1)

    def test_register(self):
        self.logout()
        email = 'exam123@163.com'
        username = 'admin'
        password = '1234567a'
        password2 = '1234567a'
        res = self.client.post(url_for('user.register'), 
                               data=dict(email=email,
                                         username=username,
                                         password=password, 
                                         password2=password2
                                         ), 
                               follow_redirects=True
                               )
        data = res.get_data(as_text=True)
        user = User.objects(username='admin').first()
        user.delete()
        self.assertEqual(res.status_code, 200)
        self.assertIn('确认邮件已发送，请检查您的收件箱', data)

    def test_register_exist(self):
        self.logout()
        email = 'exam123@163.com'
        email1 = 'example@163.com'
        username = 'exam123'
        username1 = 'exam'
        password = '1234567a'
        password2 = '1234567a'

        res = self.client.post(url_for('user.register'), 
                               data=dict(email=email1,
                                         username=username,
                                         password=password, 
                                         password2=password2
                                         ), 
                               follow_redirects=True
                               )
        data = res.get_data(as_text=True)

        res1 = self.client.post(url_for('user.register'), 
                               data=dict(email=email,
                                         username=username1,
                                         password=password, 
                                         password2=password2
                                         ), 
                               follow_redirects=True
                               )
        data1 = res1.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('该邮箱已被注册', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('帐号已经存在', data1)

    def test_user_to_admin_index(self):
        self.user.is_admin = 1
        self.user.save()
        self.login()
        res = self.client.get(url_for('admin.index', username='exam'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('首页', data)

    def test_admin_button(self):
        self.user.is_admin = 1
        self.user.save()
        self.login()
        res = self.client.get(url_for('base', username='exam'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('管理后台', data)

    def test_reconfirmed(self):
        self.user.is_admin = 1
        self.user.confirmed = False
        self.user.save()
        self.login()
        res = self.client.get(url_for('user.resend_confirm_email'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.logout()
        self.assertEqual(res.status_code, 200)
        self.assertIn('新的确认邮件已发送，请及时确认', data)


    def test_reconfirmed_again(self):
        self.user.confirmed = True
        self.user.save()
        self.login()
        res1 = self.client.get(url_for('user.resend_confirm_email'), follow_redirects=True)
        data1 = res1.get_data(as_text=True)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('帐号已认证', data1)

    def test_change_passsword(self):
        self.user.is_admin = 1
        self.user.save()
        self.login()
        res = self.client.get(url_for('user.change_password', username=self.user.username),
                              follow_redirects=True
                              )
        data = res.get_data(as_text=True)
        password='1234567a'
        res1 = self.client.post(url_for('user.change_password', username=self.user.username),
                                data=dict(old_password='123',
                                          password=password,
                                          password2=password
                                          ),
                                follow_redirects=True
                                )
        data1 = res1.get_data(as_text=True)
        res2 = self.client.post(url_for('user.change_password', username=self.user.username),
                                data=dict(old_password='123456',
                                          password=password,
                                          password2=password
                                          ),
                                follow_redirects=True
                                )
        data2 = res2.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('新密码', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('密码修改成功', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('旧密码不正确', data2)


    def test_change_email(self):
        self.user.is_admin = 1
        self.user.save()
        self.login()
        res = self.client.get(url_for('user.change_email_request', username=self.user.username),
                              follow_redirects=True
                              )
        data = res.get_data(as_text=True)
        res1 = self.client.post(url_for('user.change_email_request', username=self.user.username),
                                data=dict(email=self.user.email),
                                follow_redirects=True
                                )
        data1 = res1.get_data(as_text=True)
        res2 = self.client.post(url_for('user.change_email_request', username=self.user.username),
                                data=dict(email='exam1exam@163.com'),
                                follow_redirects=True
                                )
        data2 = res2.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('新邮箱', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('该邮箱已被注册', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('重置邮箱邮件', data2)

    def test_forget_passsword(self):
        self.logout()
        res = self.client.get(url_for('user.forget_password'), follow_redirects=True)
        data = res.get_data(as_text=True)
        res1 = self.client.post(url_for('user.forget_password'),
                                data=dict(email=self.user.email),
                                follow_redirects=True
                                )
        data1 = res1.get_data(as_text=True)
        res2 = self.client.post(url_for('user.forget_password'),
                                data=dict(email='321exam123@163.com'),
                                follow_redirects=True
                                )
        data2 = res2.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('请输入邮箱', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('重置密码邮件已发送，请到邮箱中确认', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('该邮箱不存在', data2)

    def test_login_to_NOloginRequired(self):
        self.user.confirmed = True
        self.user.save()
        self.login()
        res = self.client.get(url_for('user.login'), follow_redirects=True)
        data = res.get_data(as_text=True)
        res2 = self.client.get(url_for('user.forget_password'), follow_redirects=True)
        data2 = res2.get_data(as_text=True)
        res3 = self.client.get(url_for('user.register'), follow_redirects=True)
        data3 = res3.get_data(as_text=True)
        res4 = self.client.get(url_for('user.reset_password', token=False), follow_redirects=True)
        data4 = res4.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('欢迎来到豆半半', data)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('欢迎来到豆半半', data2)
        self.assertEqual(res3.status_code, 200)
        self.assertIn('欢迎来到豆半半', data3)
        self.assertEqual(res4.status_code, 200)
        self.assertIn('欢迎来到豆半半', data4)

    def test_register_token(self):
        self.user.confirmed = False
        self.user.save()
        self.login()
        token = generate_token(self.user, 'confirm')
        res = self.client.get(url_for('user.confirm', token=token), follow_redirects=True)
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('user.confirm', token=token), follow_redirects=True)
        data1 = res1.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('确认成功', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('欢迎来到豆半半', data1)

    def test_reset_password_token(self):
        user = User(email='exam789ple@163.com', username='ex789am')
        user.set_password('123')
        user.save()

        res = self.client.get(url_for('user.reset_password', token=False), follow_redirects=True)
        data = res.get_data(as_text=True)

        token = generate_token(user, 'reset-password')
        res1 = self.client.post(url_for('user.reset_password', token=token),
                                data=dict(email=user.email,
                                          password='12345678',
                                          password2='12345678'
                                          ),
                                follow_redirects=True
                                )
        data1 = res1.get_data(as_text=True)

        token = generate_token(user, 'reset')
        res2 = self.client.post(url_for('user.reset_password', token=token),
                                data=dict(email=user.email,
                                          password='1234567a',
                                          password2='1234567a'
                                          ),
                                follow_redirects=True
                                )
        data2 = res2.get_data(as_text=True)

        token = generate_token(user, 'reset-password')
        res3 = self.client.post(url_for('user.reset_password', token=token),
                                data=dict(email='exam777ple@163.com',
                                          password='12345678',
                                          password2='12345678'
                                          ),
                                follow_redirects=True
                                )
        data3 = res3.get_data(as_text=True)

        user.delete()
        self.assertEqual(res.status_code, 200)
        self.assertIn('重置密码', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('重置密码成功', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('无效或者过期的链接', data2)
        self.assertEqual(res3.status_code, 200)
        self.assertIn('邮箱不存在', data3)
        
    def test_change_email_token(self):
        self.user.confirmed = True
        self.user.save()
        self.login()
        token = generate_token(self.user, 'change_email', new_email='exam1234ple@163.com')
        res = self.client.get(url_for('user.change_email', token=token), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('邮箱更新成功', data)

    def test_useless_operation(self):
        self.user.confirmed = False
        self.user.save()
        self.login()
        user = User(email='exam123ple@163.com', username='ex123am')
        user.set_password('123')
        user.save()

        token = generate_token(user, 'confirm')
        res = self.client.get(url_for('user.confirm', token=token), follow_redirects=True)
        data = res.get_data(as_text=True)

        token = generate_token(user, 'change_email', new_email='exam12345ple@163.com')
        res1 = self.client.get(url_for('user.change_email', token=token), follow_redirects=True)
        data1 = res1.get_data(as_text=True)

        res2 = self.client.get(url_for('user.change_email', token=False), follow_redirects=True)
        data2 = res2.get_data(as_text=True)

        token = generate_token(self.user, 'confirmconfirm')
        res3 = self.client.get(url_for('user.confirm', token=token), follow_redirects=True)
        data3 = res3.get_data(as_text=True)

        user.delete()
        self.assertEqual(res.status_code, 200)
        self.assertIn('无效或者过期的链接', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('无效或者过期的链接', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('无效或者过期的链接', data2)
        self.assertEqual(res3.status_code, 200)
        self.assertIn('无效或者过期的链接', data3)

    def test_re_authenticate(self):
        self.login()
        res = self.client.get(url_for('user.re_authenticate'), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('活跃用户不需要重新登录', data)
