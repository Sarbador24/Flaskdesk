from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from sqlalchemy import or_
from app.agent.forms import TicketForm, TicketUpdateForm, EmailUpdateForm, PasswordChangeForm
from app.models import User, Ticket, Comment
from app.decorators import login_required
from app import db, bcrypt
import uuid

agent_blueprint = Blueprint('agent', __name__)

@agent_blueprint.route('/dashboard')
@login_required(role='agent')
def dashboard():
	open = Ticket.query.filter_by(owner_id=current_user.id).filter_by(status_id=1).all()
	resolved = Ticket.query.filter_by(owner_id=current_user.id).filter_by(status_id=2).all()
	pending = Ticket.query.filter_by(owner_id=current_user.id).filter_by(status_id=3).all()
	closed = Ticket.query.filter_by(owner_id=current_user.id).filter_by(status_id=4).all()
	
	return render_template('agent/dashboard.html', open=open, resolved=resolved, pending=pending, closed=closed)

@agent_blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required(role='agent')
def ticket():
	tickets = Ticket.query.order_by(Ticket.id.desc()).all()
	form = TicketForm()
	if form.validate_on_submit():
		public_id = str(uuid.uuid4())
		author_id = current_user.id
		owner_id = None
		priority = 1 # Low priority
		status = 1 # Open status

		ticket = Ticket(
			public_id=public_id,
			subject=form.subject.data,
			body=form.body.data,
			author_id=author_id,
			owner_id=owner_id,
			category_id=int(form.category.data),
			priority_id=priority,
			status_id=status
		)
		
		db.session.add(ticket)
		db.session.commit()
		flash('Ticket has been created.', 'primary')
		return redirect(url_for('agent.ticket'))
	return render_template('agent/ticket.html', tickets=tickets, form=form)

@agent_blueprint.route('/ticket/update/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='agent')
def update_ticket(id, public_id):
	users = User.query.filter(or_(User.role=='admin', User.role=='agent')).all()
	ticket = Ticket.query.filter_by(id=id, public_id=public_id)
	
	category = 0
	priority = 0
	status = 0
	for i in ticket:
		category = i.category_id
		priority = i.priority_id
		status = i.status_id

	form = TicketUpdateForm(
		category=category,
		priority=priority,
		status=status
	)
	if form.validate_on_submit():
		ticket_id = Ticket.query.get_or_404(id)
		if not request.form['owner_id']:
			ticket_id.owner_id = None
		else:
			ticket_id.owner_id = int(request.form['owner_id'])
		
		ticket_id.category_id = int(form.category.data)
		ticket_id.priority_id = int(form.priority.data)
		ticket_id.status_id = int(form.status.data)
		db.session.commit()
		flash('Ticket has been updated.', 'primary')
		return redirect(url_for('agent.update_ticket', id=id, public_id=public_id))
	return render_template('agent/ticket_update.html', form=form, users=users, ticket=ticket)

@agent_blueprint.route('/ticket/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='agent')
def delete_ticket(id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		db.session.delete(ticket_id)
		db.session.commit()
		flash('Ticket has been deleted.', 'primary')
		return redirect(url_for('agent.ticket'))
	return redirect(url_for('agent.ticket'))

@agent_blueprint.route('/ticket/comments/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='agent')
def comment(id, public_id):
	ticket = Ticket.query.filter_by(id=id, public_id=public_id)
	comments = Comment.query.filter(Comment.ticket_id == id).all()
	if request.method == 'POST':
		comment = request.form['comment']
		author_id = int(request.form['author_id'])
		ticket_id = int(request.form['ticket_id'])

		db.session.add(Comment(comment=comment, author_id=author_id, ticket_id=ticket_id))
		db.session.commit()
		flash('Your comment has been sent.', 'primary')
		return redirect(url_for('agent.comment', id=id, public_id=public_id))
	return render_template('agent/ticket_comment.html', ticket=ticket, comments=comments)

@agent_blueprint.route('/ticket/open/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='agent')
def open_ticket(id, public_id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		ticket_id.status_id = int(request.form['status_id'])

		db.session.commit()
		flash('Ticket has been re-opened.', 'primary')
		return redirect(url_for('agent.comment', id=id, public_id=public_id))
	return redirect(url_for('agent.ticket'))

@agent_blueprint.route('/ticket/close/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='agent')
def close_ticket(id, public_id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		ticket_id.status_id = int(request.form['status_id'])

		db.session.commit()
		flash('Ticket has been closed.', 'primary')
		return redirect(url_for('agent.comment', id=id, public_id=public_id))
	return redirect(url_for('agent.ticket'))

@agent_blueprint.route('/account_settings', methods=['GET', 'POST'])
@login_required(role='agent')
def account_settings():
	user = User.query.filter(User.id == current_user.id)
	email_form = EmailUpdateForm()
	password_form = PasswordChangeForm()
	if email_form.validate_on_submit():
		user_id = User.query.get_or_404(request.form.get('id'))
		user_id.email = email_form.email.data
		db.session.commit()

		flash('Email has been updated.', 'primary')
		redirect(url_for('agent.account_settings'))
	if password_form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(password_form.password.data).decode('utf-8')
		user_id = User.query.get_or_404(request.form.get('id'))
		user_id.password = hashed_password
		db.session.commit()

		flash('Password has been changed.', 'primary')
		redirect(url_for('agent.account_settings'))
	return render_template('agent/account_settings.html', user=user, email_form=email_form, password_form=password_form)

@agent_blueprint.route('/account/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='agent')
def delete_account(id):
	if request.method == 'POST':
		user_id = User.query.get_or_404(id)
		db.session.delete(user_id)
		db.session.commit()
		flash('Your account has been permanently deleted.', 'warning')
		return redirect(url_for('auth.logout'))
	return redirect(url_for('agent.account_settings'))