from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import Category

class TicketForm(FlaskForm):
	subject = StringField('Subject',
		validators=[DataRequired(), Length(max=128)])
	category = SelectField('Category',
		coerce=int,
		validators=[DataRequired()])
	body = TextAreaField('Body',
		validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		super(TicketForm, self).__init__(*args, **kwargs)
		self.category.choices = [(category.id, category.category) for category in Category.query.all()]

class CategoryForm(FlaskForm):
	category = StringField('Category',
		validators=[DataRequired(), Length(max=32)])

class PriorityForm(FlaskForm):
	priority = StringField('Priority',
		validators=[DataRequired(), Length(max=32)])

class StatusForm(FlaskForm):
	status = StringField('Status',
		validators=[DataRequired(), Length(max=32)])