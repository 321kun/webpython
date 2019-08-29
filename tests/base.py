import unittest
from flask import url_for
from doubanban import create_app
from doubanban.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.user = User(email='example@163.com', username='exam')
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()
        self.context.pop()

    def login(self):
        email = self.user.email
        password = '123'
        res = self.client.post(url_for('user.login'), data=dict(email=email, 
            password=password), follow_redirects=True)
        return res

    def logout(self):
        return self.client.get(url_for('user.logout'), follow_redirects=True)
