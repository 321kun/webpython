from flask import url_for
from tests.base import BaseTestCase
from doubanban.models import User, Movie


class FeatureTestCase(BaseTestCase):

    def test_collect(self):
        self.login()
        movie = Movie.objects(category='热度').order_by('id').first()
        res = self.client.post(url_for('feature.collect', movie_id=str(movie.id)), follow_redirects=True)
        data = res.get_data(as_text=True)

        movie1 = Movie.objects(category='时间', title=movie.title).first()
        res1 = self.client.post(url_for('feature.collect', movie_id=str(movie1.id)), follow_redirects=True)
        data1 = res1.get_data(as_text=True)

        movie2 = Movie.objects(category='评价').order_by('-rate').first()
        res2 = self.client.post(url_for('feature.collect', movie_id=str(movie2.id)), follow_redirects=True)
        data2 = res2.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('收藏成功', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('该电影重复收藏成功', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('收藏电影数量已达最大', data2)

    def test_uncollect(self):
        self.login()
        movie = Movie.objects(category='热度').order_by('id').first()
        res = self.client.post(url_for('feature.uncollect', movie_id=str(movie.id)), follow_redirects=True)
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('取消收藏电影成功', data)

    def test_search(self):
        movie = Movie.objects(category='热度').first()
        res = self.client.get(url_for('feature.search', q=movie.title[0:2]), follow_redirects=True)
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('feature.search', q=''), follow_redirects=True)
        data1 = res1.get_data(as_text=True)
        res2 = self.client.get(url_for('feature.search', q='找不到找不到'), follow_redirects=True)
        data2 = res2.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('搜索成功', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('请输入电影名称', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('没有找到', data2)