from flask import Blueprint, render_template, request, url_for, redirect, flash
from sqlalchemy import func
from webreview.extensions import db, bcrypt
from webreview.models import TypeMovie, User, TypeGame, GameReview, MovieReview
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timezone

review_bp = Blueprint('review', __name__, template_folder='templates')

@review_bp.route('/')
def index():
  if current_user.is_authenticated:
    game_reviews = db.session.scalars(db.select(GameReview)).all()
    game_reviews = db.session.scalars(db.select(GameReview).order_by(func.random()).limit(10)).all()
    movie_reviews = db.session.scalars(db.select(MovieReview).order_by(func.random()).limit(10)).all()
    return render_template('review/index.html',title='Home Page', game_reviews=game_reviews, movie_reviews=movie_reviews)
  else:
    flash('Please login to write a review.', 'warning')
    return redirect(url_for('users.login'))
  
@review_bp.route('/my_reviews')
def my_reviews():
  if current_user.is_authenticated:
    game_reviews = db.session.scalars(db.select(GameReview).where(GameReview.user_id == current_user.id)).all()
    movie_reviews = db.session.scalars(db.select(MovieReview).where(MovieReview.user_id == current_user.id)).all()
    return render_template('review/my_reviews.html',title='My Reviews', game_reviews=game_reviews, movie_reviews=movie_reviews)
  else:
    flash('Please login to write a review.', 'warning')
    return redirect(url_for('users.login'))
  
@review_bp.route('/new_game', methods=['GET','POST'])
@login_required
def new_game():
  query = db.select(TypeGame)
  genres = db.session.scalars(query).all()
  if request.method == 'POST':
    game_name = request.form.get('game_name')
    topic_name = request.form.get('topic_name')
    recommended = request.form.get('recommended')
    review = request.form.get('user_review')
    store = request.form.get('store_page')
    img_url = request.form.get('img_url')
    user_id = request.form.get('user_id')
    user_id = current_user.id
    game_genres = request.form.getlist('game_genres')
    
    game_types = []
    for id in game_genres:
        game_types.append(db.session.get(TypeGame,id))
        game_review = GameReview(
        game_name=game_name,
        topic=topic_name,
        recommended=recommended,
        review=review,
        store_page=store,
        img_url=img_url,
        user_id=user_id,
        types=game_types
        )
    
    existing_game = db.session.scalar(db.select(GameReview).where(GameReview.game_name == game_name,GameReview.user_id == user_id))
    if existing_game and existing_game.user_id == user_id:
        flash('You have already reviewed this game!', 'warning')
        return redirect(url_for('review.new_game'))
    else:
        db.session.add(game_review)
        db.session.commit()
        flash('Add new game review successful','success')
  return render_template('review/new_game.html',title='New Game Page',genres=genres)

@review_bp.route('/new_movie', methods=['GET','POST'])
@login_required
def new_movie():
  query = db.select(TypeMovie)
  genres = db.session.scalars(query).all()
  if request.method == 'POST':
    movie_name = request.form.get('movie_name')
    topic_name = request.form.get('topic_name')
    recommended = request.form.get('recommended')
    review = request.form.get('user_review')
    movie_page = request.form.get('movie_page')
    img_url = request.form.get('img_url')
    user_id = request.form.get('user_id')
    user_id = current_user.id
    movie_genres = request.form.getlist('movie_genres')
    
    movie_types = []
    for id in movie_genres:
        movie_types.append(db.session.get(TypeMovie,id))
        movie_review = MovieReview(
        movie_name=movie_name,
        topic=topic_name,
        recommended=recommended,
        review=review,
        movie_page=movie_page,
        img_url=img_url,
        user_id=user_id,
        types=movie_types
        )

    existing_movie = db.session.scalar(db.select(MovieReview).where(MovieReview.movie_name == movie_name,MovieReview.user_id == user_id))
    if existing_movie:
        flash('You have already reviewed this movie!', 'warning')
        return redirect(url_for('review.new_movie'))
    else:
        db.session.add(movie_review)
        db.session.commit()
        flash('Add new movie review successful','success')
  return render_template('review/new_movie.html',title='New Movie Page',genres=genres)

@review_bp.route('/game_review/<int:id>/edit',methods=['GET','POST'])
@login_required
def update_game(id):
  game = db.session.get(GameReview,id)
  query = db.select(TypeGame)
  genres = db.session.scalars(query).all()
  if request.method == 'POST':
    game_name = request.form.get('game_name')
    topic_name = request.form.get('topic_name')
    recommended = request.form.get('recommended')
    review = request.form.get('user_review')
    store = request.form.get('store_page')
    img_url = request.form.get('img_url')
    game_genres = request.form.getlist('game_genres')
    created_at = datetime.now(timezone.utc)

    game.game_name = game_name
    game.topic = topic_name
    game.recommended = recommended
    game.review = review
    game.store_page = store
    game.img_url = img_url
    game.created_at = created_at

    game.types.clear()
    for id in game_genres:
        genre = db.session.get(TypeGame, id)
        if genre:
            game.types.append(genre)

    db.session.add(game)
    db.session.commit()
    flash('Edit game successfully','success')
    return redirect(url_for('review.my_reviews'))
  return render_template('review/edit_game.html',title='Edit Game Page',game=game,genres=genres)

@review_bp.route('/game_review/<int:id>/delete')
@login_required
def delete_game(id):
    game = db.session.get(GameReview, id)
    
    if game.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('review.my_reviews'))

    db.session.delete(game)
    db.session.commit()
    
    flash('Game review deleted successfully', 'success')
    return redirect(url_for('review.my_reviews'))

@review_bp.route('/movie_review/<int:id>/edit',methods=['GET','POST'])
@login_required
def update_movie(id):
  movie = db.session.get(MovieReview,id)
  query = db.select(TypeMovie)
  genres = db.session.scalars(query).all()
  if request.method == 'POST':
    movie_name = request.form.get('movie_name')
    topic_name = request.form.get('topic_name')
    recommended = request.form.get('recommended')
    review = request.form.get('user_review')
    movie_page = request.form.get('movie_page')
    img_url = request.form.get('img_url')
    movie_genres = request.form.getlist('movie_genres')
    created_at = datetime.now(timezone.utc)

    movie.movie_name = movie_name
    movie.topic = topic_name
    movie.recommended = recommended
    movie.review = review
    movie.movie_page = movie_page    
    movie.img_url = img_url
    movie.created_at = created_at

    movie.types.clear()
    for id in movie_genres:
        genre = db.session.get(TypeMovie, id)
        if genre:
            movie.types.append(genre)

    db.session.add(movie)
    db.session.commit()
    flash('Edit movie successfully','success')
    return redirect(url_for('review.my_reviews'))
  return render_template('review/edit_movie.html',title='Edit Movie Page',movie=movie,genres=genres)

@review_bp.route('/movie_review/<int:id>/delete')
@login_required
def delete_movie(id):
    movie = db.session.get(MovieReview, id)

    if movie.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('review.my_reviews'))

    db.session.delete(movie)
    db.session.commit()

    flash('Movie review deleted successfully', 'success')
    return redirect(url_for('review.my_reviews'))

@review_bp.route('/my_reviews/search', methods=['POST'])
@login_required
def search_my_reviews():
    name = request.form.get('name')

    searchs_games = db.session.scalars(db.select(GameReview).where(GameReview.user_id == current_user.id,GameReview.game_name.ilike(f'%{name}%'))).all()
    searchs_movies = db.session.scalars(db.select(MovieReview).where(MovieReview.user_id == current_user.id,MovieReview.movie_name.ilike(f'%{name}%'))).all()

    return render_template('review/search_my_reviews.html',search_games=searchs_games,search_movies=searchs_movies,title='Search My Reviews')

@review_bp.route('/game_reviews')
def game_reviews():
    game_reviews = db.session.scalars(db.select(GameReview)).all()
    page = request.args.get('page',type=int)
    query = db.select(GameReview)
    review = db.paginate(query, page=page, per_page=4)
    return render_template('review/game_reviews.html',title='Game Reviews', game_reviews=game_reviews, reviews=review)

@review_bp.route('/movie_reviews')
def movie_reviews():
    movie_reviews = db.session.scalars(db.select(MovieReview)).all()
    page = request.args.get('page',type=int)
    query = db.select(MovieReview)
    review = db.paginate(query, page=page, per_page=4)
    return render_template('review/movie_reviews.html',title='Movie Reviews', movie_reviews=movie_reviews, reviews=review)

@review_bp.route('/game_reviews/search', methods=['GET','POST'])
def search_game_reviews():
    name = request.args.get('name') or request.form.get('name')
    page = request.args.get('page',type=int)
    if name is None:
        return redirect(url_for('review.game_reviews', page=page))
    query = db.select(GameReview).where(GameReview.game_name.ilike(f'%{name}%')
    )
    review = db.paginate(query, page=page, per_page=4)
    searchs_games = db.session.scalars(db.select(GameReview).where(GameReview.game_name.ilike(f'%{name}%'))).all()

    return render_template('review/search_games.html',search_games=searchs_games,title='Search Games', reviews=review,name=name)

@review_bp.route('/movie_reviews/search', methods=['GET','POST'])
def search_movie_reviews():
    name = request.args.get('name') or request.form.get('name')
    page = request.args.get('page',type=int)
    if name is None:
        return redirect(url_for('review.movie_reviews', page=page))
    query = db.select(MovieReview).where(MovieReview.movie_name.ilike(f'%{name}%')
    )
    review = db.paginate(query, page=page, per_page=4)
    searchs_movies = db.session.scalars(db.select(MovieReview).where(MovieReview.movie_name.ilike(f'%{name}%'))).all()

    return render_template('review/search_movies.html',search_movies=searchs_movies,title='Search Movies', reviews=review,name=name)

@review_bp.route('/game_reviews/<int:id>/detail')
def game_review_detail(id):
    game = db.session.get(GameReview, id)
    return render_template('review/game_detail_reviews.html', title='Game Detail Page', game=game)

@review_bp.route('/movie_reviews/<int:id>/detail')
def movie_review_detail(id):
    movie = db.session.get(MovieReview, id)
    return render_template('review/movie_detail_reviews.html', title='Movie Detail Page', movie=movie)