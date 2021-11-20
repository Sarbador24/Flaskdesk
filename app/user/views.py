from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from app.models import User
from app.decorators import login_required
from app import db, bcrypt

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/dashboard')
@login_required(role='user')
def dashboard():
	return render_template('user/dashboard.html')