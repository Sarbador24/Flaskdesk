from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# Configuration
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
mail = Mail(app)
csrf = CSRFProtect(app)

from app.auth.views import auth_blueprint
from app.admin.views import admin_blueprint
from app.agent.views import agent_blueprint
from app.user.views import user_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(agent_blueprint, url_prefix='/agent')
app.register_blueprint(user_blueprint, url_prefix='/user')

@app.route('/')
def root():
	return(redirect(url_for('auth.login')))