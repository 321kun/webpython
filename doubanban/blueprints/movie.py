from flask import Blueprint, render_template, request
from flask_login import current_user
from doubanban.models import Movie
from doubanban.extensions import cache

movie_bp = Blueprint('movie', __name__)


@movie_bp.route('/recommed', methods=['GET', 'POST'])
@cache.cached(query_string=True, unless=lambda: current_user.is_authenticated)
def recommed():
    category = "热度"
    page = request.args.get('page', 1, type=int)
    pagination = Movie.objects(category=category).all().order_by('id').paginate(page, per_page=12)
    movies = pagination.items
    return render_template('movie/movie.html', pagination=pagination, movies=movies, category=category)


@movie_bp.route('/time', methods=['GET', 'POST'])
@cache.cached(query_string=True, unless=lambda: current_user.is_authenticated)
def time():
    category = "时间"
    page = request.args.get('page', 1, type=int)
    pagination = Movie.objects(category=category).all().order_by('-year').paginate(page, per_page=12)
    movies = pagination.items
    return render_template('movie/movie.html', pagination=pagination, movies=movies, category=category)


@movie_bp.route('/rank', methods=['GET', 'POST'])
@cache.cached(query_string=True, unless=lambda: current_user.is_authenticated)
def rank():
    category = "评价"
    page = request.args.get('page', 1, type=int)
    pagination = Movie.objects(category=category).all().order_by('-rate').paginate(page, per_page=12)
    movies = pagination.items
    return render_template('movie/movie.html', pagination=pagination, movies=movies, category=category)
