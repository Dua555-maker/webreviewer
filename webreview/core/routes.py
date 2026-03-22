import random

from flask import Blueprint, render_template, request, url_for, redirect, flash
from webreview.extensions import db, bcrypt
from webreview.models import TypeMovie, User, TypeGame, GameReview, MovieReview
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timezone
from sqlalchemy import func

from webreview.review.routes import game_reviews, movie_reviews, movie_reviews


core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
  games = db.session.scalars(db.select(GameReview)).all()
  movies = db.session.scalars(db.select(MovieReview)).all()

  all_reviews = games + movies
  random.shuffle(all_reviews)

  reviews = all_reviews[:3] 
  return render_template('core/index.html',title='Home Page', reviews=reviews)