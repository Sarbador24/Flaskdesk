from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.auth.forms import LoginForm, SignupForm, RequestResetForm, ResetPasswordForm
from app.reset_password import send_reset_email
from app.url_endpoint import redirect_dest
from app.models import User
from app import db, bcrypt
import uuid

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	# If user is already authenticated redirect to designated page
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role == 'admin':
			login_user(user, remember=form.remember.data)
			return redirect_dest(fallback=url_for('admin.dashboard'))
		elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.role == 'user':
			login_user(user, remember=form.remember.data)
			return redirect_dest(fallback=url_for('user.dashboard'))
		else:
			flash('Your email or password is incorrect, please try again.', 'danger')
	return render_template('auth/login.html', form=form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))
		
	form = SignupForm()
	if form.validate_on_submit():
		public_id = str(uuid.uuid4())
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		role = 'user'
		user = User(
			public_id=public_id,
			name=form.name.data,
			email=form.email.data,
			password=hashed_password,
			role=role
		)
		db.session.add(user)
		db.session.commit()

		flash('Success! Your account has been created.', 'primary')
		return redirect(url_for('auth.login'))
	return render_template('auth/signup.html', form=form)

@auth_blueprint.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('A message has been sent to your email with instructions to reset your password.', 'primary')
		return redirect(url_for('auth.login'))
	return render_template('auth/forgot_password.html', form=form)

@auth_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token, please try again!', 'warning')
		return redirect(url_for('auth.reset_request'))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()

		flash('Success! Your password has been updated.', 'primary')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)