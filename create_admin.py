from app import app, db, bcrypt
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
import uuid

name = 'John Johnson'
email = 'admin@flaskdesk.com'
password = 'flaskdesk'
role = 'admin'

public_id = str(uuid.uuid4())
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

user = User(
	public_id=public_id,
	name=name,
	email=email,
	password=hashed_password,
	role=role
)

def db_commit():
	try:
		db.session.commit()
		print('{} has been created!'.format(email))
		return True
	except SQLAlchemyError:
		result = str(SQLAlchemyError)
		print(result)
		return False

with app.app_context():
	if db_commit():
		db.session.add(user)
		db.session.commit()