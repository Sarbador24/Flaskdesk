from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User, Category, Priority, Status

class TicketForm(FlaskForm):
	subject = StringField('Subject',
		validators=[DataRequired(), Length(max=128)])
	category = SelectField('Category',
		# coerce=int,
		validators=[DataRequired()])
	body = TextAreaField('Body',
		validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		super(TicketForm, self).__init__(*args, **kwargs)
		self.category.choices = [("", "--- Please select category ---")]+[(category.id, category.category) for category in Category.query.all()]

class TicketUpdateForm(FlaskForm):
	category = SelectField('Category',
		validators=[DataRequired()])
	priority = SelectField('Priority',
		validators=[DataRequired()])
	status = SelectField('Status',
		validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		super(TicketUpdateForm, self).__init__(*args, **kwargs)
		self.category.choices = [('', '--- Please select category ---')]+[(category.id, category.category)
			for category in Category.query.all()]
		self.priority.choices = [('', '--- Please select priority ---')]+[(priority.id, priority.priority)
			for priority in Priority.query.all()]
		self.status.choices = [('', '--- Please select status ---')]+[(status.id, status.status)
			for status in Status.query.all()]

class CategoryForm(FlaskForm):
	category = StringField('Category',
		validators=[DataRequired(), Length(max=32)])

class PriorityForm(FlaskForm):
	priority = StringField('Priority',
		validators=[DataRequired(), Length(max=32)])

class StatusForm(FlaskForm):
	status = StringField('Status',
		validators=[DataRequired(), Length(max=32)])