from flask import current_app, abort
from tests.base import BaseTestCase


class BasicTestCase(BaseTestCase):

    def test_app_exist(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_404_error(self):
        res = self.client.get('/nothing')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 404)
        self.assertIn('没有找到该网页', data)

    def test_400_error(self):
        @current_app.route('/400')
        def internal_server_error_for_test():
            abort(400)

        res = self.client.get('/400')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 400)
        self.assertIn('请求无法被服务器理解', data)

    def test_403_error(self):
        @current_app.route('/403')
        def internal_server_error_for_test():
            abort(403)

        res = self.client.get('/403')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 403)
        self.assertIn('禁止访问', data)

    def test_500_error(self):
        @current_app.route('/500')
        def internal_server_error_for_test():
            abort(500)

        res = self.client.get('/500')
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 500)
        self.assertIn('服务器错误', data)