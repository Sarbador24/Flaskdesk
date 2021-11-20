from app import app, db
from app.models import Category, Priority, Status
from sqlalchemy.exc import SQLAlchemyError

category = 'Uncategorized'
priorities = ['Low', 'Medium', 'High', 'Urgent']
statuses = ['Open', 'Resolved', 'Pending', 'Closed']

def db_commit():
	try:
		db.session.commit()
		print('Category, priorities, and statuses has been created.')
		return True
	except SQLAlchemyError:
		result = str(SQLAlchemyError)
		print(result)
		return False

with app.app_context():
	if db_commit():
		for priority, status in zip(priorities, statuses):
			db.session.add(Priority(priority=priority))
			db.session.add(Status(status=status))
		db.session.add(Category(category=category))
		db.session.commit()