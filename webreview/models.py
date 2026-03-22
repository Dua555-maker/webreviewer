from webreview.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, ForeignKey, Column, Table, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  avatar: Mapped[str] = mapped_column(String(25), nullable=True, default='avatar.png')
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  
  game_reviews: Mapped[List['GameReview']] = relationship(back_populates='user')
  movie_reviews: Mapped[List['MovieReview']] = relationship(back_populates='user')
  def __repr__(self):
    return f'<User: {self.username}>'

game_genre = Table(
  'game_genre',
  db.metadata,
  Column('game_genre_id', Integer, ForeignKey('type_game.id'), primary_key=True),
  Column('game_review_id', Integer, ForeignKey('game_review.id'), primary_key=True)
)

movie_genre = Table(
  'movie_genre',
  db.metadata,
  Column('movie_genre_id', Integer, ForeignKey('type_movie.id'), primary_key=True),
  Column('movie_review_id', Integer, ForeignKey('movie_review.id'), primary_key=True)
)

class TypeGame(db.Model):
  __tablename__ = 'type_game'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(35), nullable=False,)

  game_reviews: Mapped[List['GameReview']] = relationship(back_populates='types', secondary=game_genre)
  def __repr__(self):
    return f'<Type: {self.name}>'

class GameReview(db.Model):
  __tablename__ = 'game_review'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  game_name: Mapped[str] = mapped_column(Text, nullable=False,)
  topic: Mapped[str] = mapped_column(Text, nullable=False)
  review: Mapped[str] = mapped_column(Text, nullable=False)
  recommended: Mapped[str] = mapped_column(Text, nullable=False)
  store_page: Mapped[str] = mapped_column(Text, nullable=False)
  img_url: Mapped[str] = mapped_column(Text, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

  user: Mapped[User] = relationship(back_populates='game_reviews')
  types: Mapped[List['TypeGame']] = relationship(back_populates='game_reviews', secondary=game_genre)
  
  def __repr__(self):
    return f'<GameReview: {self.game_name}>'

class TypeMovie(db.Model):
  __tablename__ = 'type_movie'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(35), nullable=False)

  movie_reviews: Mapped[List['MovieReview']] = relationship(back_populates='types', secondary=movie_genre)
  def __repr__(self):
    return f'<Type: {self.name}>'

class MovieReview(db.Model):
  __tablename__ = 'movie_review'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  movie_name: Mapped[str] = mapped_column(Text, nullable=False)
  topic: Mapped[str] = mapped_column(Text, nullable=False)
  review: Mapped[str] = mapped_column(Text, nullable=False)
  recommended: Mapped[str] = mapped_column(Text, nullable=False)
  movie_page: Mapped[str] = mapped_column(Text, nullable=False)
  img_url: Mapped[str] = mapped_column(Text, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

  user: Mapped[User] = relationship(back_populates='movie_reviews')
  types: Mapped[List['TypeMovie']] = relationship(back_populates='movie_reviews', secondary=movie_genre)
  
  def __repr__(self):
    return f'<MovieReview: {self.movie_name}>'
