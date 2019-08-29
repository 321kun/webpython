from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from doubanban.forms import MovieForm, UpgradeForm
from doubanban.models import User, Movie
from flask_login import current_user, fresh_login_required
from doubanban.utils import redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/<username>/index', methods=['GET', 'POST'])
@fresh_login_required
def index(username):
    if username == current_user.username and current_user.is_authenticated:
        return render_template('admin/index.html', username=username)
    else:
        abort(404)


# 以下全部路由是否要记录username,或者其他方式，排除潜在问题？(谁误操恶操？)
# -----/<username>/update/<movie_id>
@admin_bp.route('/update/<movie_id>', methods=['GET', 'POST'])
@fresh_login_required
def update(movie_id):
    form = MovieForm()
    movie = Movie.objects(pk=movie_id).first()
    if form.validate_on_submit():
        movie.update(
            title=form.title.data,
            rate=form.rate.data,
            people=form.people.data,
            year=form.year.data,
            country=form.country.data,
            img=form.img.data,
            url=form.url.data,
            category=form.category.data
        )
        flash('修改成功', 'success')
        return redirect(url_for('admin.update_movie'))
    form.title.data = movie.title
    form.rate.data = movie.rate
    form.people.data = movie.people
    form.year.data = movie.year
    form.country.data = movie.country
    form.img.data = movie.img
    form.url.data = movie.url
    form.category.data = movie.category
    return render_template('admin/update.html', form=form)


@admin_bp.route('/delete/<movie_id>', methods=['POST'])
@fresh_login_required
def delete(movie_id):
    movie = Movie.objects(pk=movie_id).first()
    movie.delete()
    flash('删除成功', 'success')
    return redirect_back()


@admin_bp.route('/add', methods=['GET', 'POST'])
@fresh_login_required
def add():
    form = MovieForm()
    if form.validate_on_submit():
        message = Movie(
            title=form.title.data,
            rate=form.rate.data,
            people=form.people.data,
            year=form.year.data,
            country=form.country.data,
            img=form.img.data,
            url=form.url.data,
            category=form.category.data
            )
        message.save()
        flash('增加电影成功', 'success')
        return redirect(url_for('admin.index', username=current_user.username))
    return render_template('admin/add.html', form=form)


@admin_bp.route('/update/movie', methods=['GET'])
@fresh_login_required
def update_movie():
    filter_rule = request.args.get('filter', '全部')
    if filter_rule == '热度':
        filter_movie = Movie.objects(category='热度').order_by('id')
    elif filter_rule == '时间':
        filter_movie = Movie.objects(category='时间').order_by('-year')
    elif filter_rule == '评价':
        filter_movie = Movie.objects(category='评价').order_by('-rate')
    else:
        filter_movie = Movie.objects.all().order_by('year')

    page = request.args.get('page', 1, int)
    # error_out=False 无效？
    pagination = filter_movie.paginate(page, 10)
    movies = pagination.items
    return render_template('admin/manager_movie.html', pagination=pagination, movies=movies)


@admin_bp.route('/manager_user', methods=['GET'])
@fresh_login_required
def manager_user():
    grade = request.args.get('grade', '2')
    if grade == '1':
        users = User.objects(is_admin='1').all()
    else:
        users = User.objects(is_admin='2').all()

    page = request.args.get('page', 1, int)
    pagination = users.paginate(page, 10)
    targets = pagination.items
    return render_template('admin/manager_user.html', pagination=pagination, targets=targets)


@admin_bp.route('/upgrade/<user_id>', methods=['GET', 'POST'])
@fresh_login_required
def upgrade(user_id):
    form = UpgradeForm()
    user = User.objects(pk=user_id).first()
    if form.validate_on_submit():
        user.update(is_admin=form.is_admin.data)
        flash('修改管理成功', 'success')
        return redirect(url_for('admin.manager_user'))
    form.is_admin.data = user.is_admin
    return render_template('admin/upgrade.html', form=form)
