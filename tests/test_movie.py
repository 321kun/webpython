from flask import url_for
from tests.base import BaseTestCase


class AdminTestCase(BaseTestCase):

    def test_base(self):
        res = self.client.get(url_for('base'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('欢迎来到豆半半电影查询网页', data)
        
    def test_redu(self):
        res = self.client.get(url_for('movie.recommed'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('以热度分类', data)

    def test_shijian(self):
        res = self.client.get(url_for('movie.time'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('以时间分类', data)

    def test_pingjia(self):
        res = self.client.get(url_for('movie.rank'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('以评价分类', data)