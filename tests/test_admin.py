from flask import url_for
from doubanban.models import Movie, User
from tests.base import BaseTestCase


class AdminTestCase(BaseTestCase):

    def test_houtaizhuye_button(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()
        res = self.client.get(url_for('base', username='exam'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('管理后台', data)

    def test_admin2_index(self):
        self.user.is_admin = 2
        self.user.save()
        self.login()

        res = self.client.get(url_for('admin.index', username='exam'))
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('admin.index', username='examfghgf'))
        data1 = res1.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('修改电影', data)
        self.assertEqual(res1.status_code, 404)
        self.assertIn('没有找到该网页', data1)


    def test_admin3_index(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()
        res = self.client.get(url_for('admin.index', username='exam'))
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('升级管理', data)

    def test_add(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()

        res = self.client.get(url_for('admin.add'))
        data = res.get_data(as_text=True)

        movie = Movie.objects(category='热度').order_by('id').first()
        res1 = self.client.post(url_for('admin.add'), 
                                data=dict(
                                          title='exameaxm',
                                          rate='100.0',
                                          people='123456789',
                                          year='2019',
                                          country='wuwuwu',
                                          img=movie.img,
                                          url=movie.url,
                                          category='热度'
                                          ), 
                                follow_redirects=True)
        data1 = res1.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('电影链接', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('增加电影成功', data1)

    def test_delete(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()

        movie = Movie.objects(title='exameaxm').first()
        res = self.client.get(url_for('admin.update', movie_id=str(movie.id)), 
                              follow_redirects=True
                              )
        data = res.get_data(as_text=True)
        res1 = self.client.post(url_for('admin.update', movie_id=str(movie.id)), 
                                data=dict(
                                          title='kunkun',
                                          rate='100.0',
                                          people='123456789',
                                          year='2019',
                                          country='wuwuwu',
                                          img=movie.img,
                                          url=movie.url,
                                          category='热度'
                                          ),
                                follow_redirects=True
                                )
        data1 = res1.get_data(as_text=True)
        movie1 = Movie.objects(title='kunkun').first()
        res2 = self.client.post(url_for('admin.delete', movie_id=str(movie1.id)), follow_redirects=True)
        data2 = res2.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('电影链接', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('修改成功', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('删除成功', data2)

    def test_manager_movie(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()

        res = self.client.get(url_for('admin.update_movie', filter='全部'))
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('admin.update_movie', filter='热度'))
        data1 = res1.get_data(as_text=True)
        res2 = self.client.get(url_for('admin.update_movie', filter='时间'))
        data2 = res2.get_data(as_text=True)
        res3 = self.client.get(url_for('admin.update_movie', filter='评价'))
        data3 = res3.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('全部', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('热度', data1)
        self.assertEqual(res2.status_code, 200)
        self.assertIn('时间', data2)
        self.assertEqual(res3.status_code, 200)
        self.assertIn('评价', data3)

    def test_manager_user(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()
        res = self.client.get(url_for('admin.manager_user', grade='2'))
        data = res.get_data(as_text=True)
        res1 = self.client.get(url_for('admin.manager_user', grade='1'))
        data1 = res1.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('普通管理员', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('普通会员', data1)

    def test_upgrade(self):
        self.user.is_admin = 3
        self.user.save()
        self.login()
        user = User(email='exam456@163.com', username='exam456')
        user.set_password('123456789a')
        user.save()

        res = self.client.get(url_for('admin.upgrade', user_id=user.id))
        data = res.get_data(as_text=True)
        res1 = self.client.post(url_for('admin.upgrade', user_id=user.id),
                               data=dict(is_admin=2),
                               follow_redirects=True
                               )
        data1 = res1.get_data(as_text=True)
        user.delete()

        self.assertEqual(res.status_code, 200)
        self.assertIn('升级或降级管理员', data)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('修改管理成功', data1)
