from app import app, db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# Database models
class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(255), unique=True, nullable=False)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	# Relationship
	author_tickets = db.relationship('Ticket', foreign_keys='Ticket.author_id',
		backref='author', cascade='all, delete-orphan', lazy=True)
	owner_tickets = db.relationship('Ticket', foreign_keys='Ticket.owner_id',
		backref='owner', passive_deletes=True, lazy=True)
	comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
		return serializer.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		serializer = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = serializer.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __init__(self, public_id, name, email, password, role):
		self.public_id = public_id
		self.name = name
		self.email = email
		self.password = password
		self.role = role

class Ticket(db.Model):
	__tablename__ = 'tickets'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(255), unique=True, nullable=False)
	subject = db.Column(db.String(255), nullable=False)
	body = db.Column(db.Text, nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
	priority_id = db.Column(db.Integer, db.ForeignKey('priorities.id', ondelete='SET NULL'), nullable=True)
	status_id = db.Column(db.Integer, db.ForeignKey('statuses.id', ondelete='SET NULL'), nullable=True)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	# Relationship
	comments = db.relationship('Comment', backref='ticket', cascade='all, delete-orphan', lazy=True)

	def __init__(self, public_id, subject, body, author_id, owner_id, category_id, priority_id, status_id):
		self.public_id = public_id
		self.subject = subject
		self.body = body
		self.author_id = author_id
		self.owner_id = owner_id
		self.category_id = category_id
		self.priority_id = priority_id
		self.status_id = status_id

class Category(db.Model):
	__tablename__ = 'categories'

	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	# Relationship
	tickets = db.relationship('Ticket', backref='category', passive_deletes=True, lazy=True)

	def __init__(self, category):
		self.category = category

class Priority(db.Model):
	__tablename__ = 'priorities'

	id = db.Column(db.Integer, primary_key=True)
	priority = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	# Relationship
	tickets = db.relationship('Ticket', backref='priority', passive_deletes=True, lazy=True)

	def __init__(self, priority):
		self.priority = priority

class Status(db.Model):
	__tablename__ = 'statuses'

	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	# Relationship
	tickets = db.relationship('Ticket', backref='status', passive_deletes=True, lazy=True)

	def __init__(self, status):
		self.status = status

class Comment(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.Text, nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	def __init__(self, comment, author_id, ticket_id):
		self.comment = comment
		self.author_id = author_id
		self.ticket_id = ticket_id