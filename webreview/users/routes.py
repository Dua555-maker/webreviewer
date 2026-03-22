from flask import Blueprint, render_template, request, url_for, redirect, flash
from webreview.extensions import db, bcrypt
from webreview.models import User
from flask_login import login_user, logout_user, current_user, login_required

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    query = db.select(User).where(User.username==username)
    user = db.session.scalar(query)
    if user:
      flash('Username is already exists!', 'warning')
      return redirect(url_for('users.register'))
    else:
      query = db.select(User).where(User.email==email)
      user = db.session.scalar(query)
      if user:
        flash('Email is already exists!', 'warning')
        return redirect(url_for('users.register'))
      else:
        if password==confirm_password:
          pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')
          user = User(username=username, 
                      email=email,
                      password=pwd_hash)
          
          db.session.add(user)
          db.session.commit()
          login_user(user)
          flash('Register sucessful!', 'success')
          return redirect(url_for('core.index'))
        
        else:
          flash('Password not match!', 'warning')
          return redirect(url_for('users.register'))
      
  return render_template('users/register.html', title='Register Page')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    query = db.select(User).where(User.username==username)
    user = db.session.scalar(query)
    if user and bcrypt.check_password_hash(user.password, password):
      login_user(user)
      return redirect(url_for('core.index'))
    elif not user:
      flash('Username is not exists!', 'warning')
      return redirect(url_for('users.login'))
    else:
      flash('Password is not correct!', 'warning')
      return redirect(url_for('users.login'))
  return render_template('users/login.html', title='Login Page')

@users_bp.route('/')
@login_required
def index():
  return render_template('core/index.html', title='User Page')

@users_bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('core.index'))  

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  user = current_user
  review = user.game_reviews + user.movie_reviews
  user.review_count = len(review)
  return render_template('users/profile.html', title='Profile Page',user=user)

@users_bp.route('/change_password/<int:id>',methods=['GET','POST'])
@login_required
def change_password(id):
  user = db.session.get(User,id)
  if request.method == 'POST':
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    new_password = request.form['new_password']
    if bcrypt.check_password_hash(user.password, password) and new_password == confirm_password:
      pwd_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
      user.password = pwd_hash
      db.session.add(user)
      db.session.commit()
      flash('Change password successfully!','success')
      return redirect(url_for('core.index'))
    elif not bcrypt.check_password_hash(user.password, password) and new_password == confirm_password:
      flash('Old Password not match!', 'warning')
      return redirect(url_for('users.change_password', id=user.id))
    else:
      flash('New Password not match!', 'warning')
      return redirect(url_for('users.change_password', id=user.id))
  return render_template('users/change.html',title='Change Password Page',user=user)