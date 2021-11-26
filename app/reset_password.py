from flask import url_for
from flask_mail import Message
from app import app, mail

def send_reset_email(user):
	token = user.get_reset_token()
	message = Message(
		'Password Reset Request',
		sender=app.config['MAIL_USERNAME'],
		recipients=[user.email]
	)
	message.body = f'''Dear {user.name},

To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

This link will expire within 30 minutes. If you do not wish to reset your password, ignore this email and nothing will be changed.
'''
	mail.send(message)