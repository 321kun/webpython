from doubanban.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


CHOICES = ('热度', '时间', '评价')


class Movie(db.Document):
    title = db.StringField(max_length=50, required=True)
    rate = db.StringField()
    people = db.IntField()
    year = db.StringField(index=True)
    country = db.StringField(max_length=50)
    img = db.StringField(max_length=250, required=True)
    url = db.StringField(max_length=300, required=True)
    category = db.StringField(required=True, choices=CHOICES)

    meta = {'indexes': ['title']}


class User(db.Document, UserMixin):
    email = db.StringField(max_length=50, required=True, unique=True)
    username = db.StringField(max_length=30, required=True, unique=True)
    password_hash = db.StringField(max_length=128, required=True)
    confirmed = db.BooleanField(default=False)
    collections = db.ListField(db.ReferenceField(Movie, reverse_delete_rule=db.PULL))
    is_admin = db.IntField(default=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def no_repeat(self):
        titles = []
        imgs = []
        urls = []
        ids = []
        collections = reversed(self.collections)
        for each in collections:
            if each.title not in titles:
                titles.append(each.title)
                imgs.append(each.img)
                urls.append(each.url)
                ids.append(each.id)
        target = zip(titles, imgs, urls, ids)
        return target

    def collection_num(self):
        titles = []
        for each in self.collections:
            titles.append(each.title)
        titles_set = set(titles)
        whole_num = len(titles)
        repeat_num = len(titles) - len(titles_set)
        return whole_num, repeat_num

    def not_collect_again(self):
        titles = []
        for each in self.collections:
            titles.append(each.title)
        title = titles[-1]
        if titles.count(title) == 1:
            return True

    # 可以写的更复杂点，现在简略判断
    def judge_is_admin(self):
        if self.username == 'admin':
            self.is_admin = 3
