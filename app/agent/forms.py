from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email
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

class EmailUpdateForm(FlaskForm):
	email = EmailField('Email Address',
		validators=[DataRequired(), Email(), Length(max=64)])

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email address is already taken')

class PasswordChangeForm(FlaskForm):
	password = PasswordField('New Password',
		validators=[DataRequired(), Length(min=6, max=32)])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(), EqualTo('password')])