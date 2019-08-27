from flask import Blueprint, render_template, request, flash, current_app
from doubanban.models import Movie
from flask_login import login_required, current_user
from doubanban.utils import redirect_back
from bson import ObjectId

feature_bp = Blueprint('feature', __name__)


@feature_bp.route('/collect/<movie_id>', methods=['GET', 'POST'])
@login_required
def collect(movie_id):
    if len(current_user.collections) >= current_app.config['MAX_COLLECTIONS_NUM']:
        flash('收藏电影数量已达最大，请尽量不要收藏重复的电影', 'warning')
        return redirect_back()
    movie_id = ObjectId(movie_id)
    current_user.update(push__collections=movie_id)
    current_user.reload()
    if current_user.not_collect_again():
        flash("收藏成功", 'success')
    else:
        flash("该电影重复收藏成功，尽量不要有此操作，如需删除请到个人页面", 'warning')
    return redirect_back()


@feature_bp.route('/uncollect/<movie_id>', methods=['POST'])
@login_required
def uncollect(movie_id):
    movie_id = ObjectId(movie_id)
    current_user.update(pull__collections=movie_id)
    flash('取消收藏电影成功', 'success')
    return redirect_back()


@feature_bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    if q == '':
        flash('请输入电影名称', 'warning')
        return redirect_back()
    page = request.args.get('page', 1, type=int)
    pagination = Movie.objects.filter(title__contains=q).paginate(page, 4)
    movies = pagination.items
    if movies:
        flash('搜索成功', 'success')
    else:
        flash('没有找到', 'info')
    return render_template('base.html', q=q, movies=movies, pagination=pagination)
