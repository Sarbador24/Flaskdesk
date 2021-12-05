from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from sqlalchemy import or_
from app.admin.forms import UserForm, TicketForm, TicketUpdateForm, CategoryForm, PriorityForm, StatusForm, EmailUpdateForm, PasswordChangeForm
from app.models import User, Ticket, Category, Priority, Status, Comment
from app.decorators import login_required
from app import db, bcrypt
import uuid

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/dashboard')
@login_required(role='admin')
def dashboard():
	return render_template('admin/dashboard.html')

@admin_blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required(role='admin')
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
		return redirect(url_for('admin.ticket'))
	return render_template('admin/ticket.html', tickets=tickets, form=form)

@admin_blueprint.route('/ticket/update/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='admin')
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
		return redirect(url_for('admin.update_ticket', id=id, public_id=public_id))
	return render_template('admin/ticket_update.html', form=form, users=users, ticket=ticket)

@admin_blueprint.route('/ticket/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_ticket(id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		db.session.delete(ticket_id)
		db.session.commit()
		flash('Ticket has been deleted.', 'primary')
		return redirect(url_for('admin.ticket'))
	return redirect(url_for('admin.ticket'))

@admin_blueprint.route('/ticket/comments/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='admin')
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
		return redirect(url_for('admin.comment', id=id, public_id=public_id))
	return render_template('admin/ticket_comment.html', ticket=ticket, comments=comments)

@admin_blueprint.route('/ticket/open/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def open_ticket(id, public_id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		ticket_id.status_id = int(request.form['status_id'])

		db.session.commit()
		flash('Ticket has been re-opened.', 'primary')
		return redirect(url_for('admin.comment', id=id, public_id=public_id))
	return redirect(url_for('admin.ticket'))

@admin_blueprint.route('/ticket/close/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def close_ticket(id, public_id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		ticket_id.status_id = int(request.form['status_id'])

		db.session.commit()
		flash('Ticket has been closed.', 'primary')
		return redirect(url_for('admin.comment', id=id, public_id=public_id))
	return redirect(url_for('admin.ticket'))

@admin_blueprint.route('/categories', methods=['GET', 'POST'])
@login_required(role='admin')
def category():
	categories = Category.query.order_by(Category.id.desc()).all()
	form = CategoryForm()
	if form.validate_on_submit():
		category = Category(category=form.category.data)
		db.session.add(category)
		db.session.commit()
		flash('Category has been created.', 'primary')
		return redirect(url_for('admin.category'))
	return render_template('admin/category.html', categories=categories, form=form)

@admin_blueprint.route('/category/update', methods=['GET', 'POST'])
@login_required(role='admin')
def update_category():
	form = CategoryForm()
	if form.validate_on_submit():
		category_id = Category.query.get_or_404(request.form.get('id'))
		category_id.category = form.category.data
		db.session.commit()
		flash('Category has been updated.', 'primary')
		return redirect(url_for('admin.category'))
	return render_template('admin/category.html', form=form)

@admin_blueprint.route('/category/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_category(id):
	if request.method == 'POST':
		category_id = Category.query.get_or_404(id)
		db.session.delete(category_id)
		db.session.commit()
		flash('Category has been deleted.', 'primary')
		return redirect(url_for('admin.category'))
	return redirect(url_for('admin.category'))

@admin_blueprint.route('/priorities', methods=['GET', 'POST'])
@login_required(role='admin')
def priority():
	priorities = Priority.query.order_by(Priority.id.desc()).all()
	form = PriorityForm()
	if form.validate_on_submit():
		priority = Priority(priority=form.priority.data)
		db.session.add(priority)
		db.session.commit()
		flash('Priority has been created.', 'primary')
		return redirect(url_for('admin.priority'))
	return render_template('admin/priority.html', priorities=priorities, form=form)

@admin_blueprint.route('/priority/update', methods=['GET', 'POST'])
@login_required(role='admin')
def update_priority():
	form = PriorityForm()
	if form.validate_on_submit():
		priority_id = Priority.query.get_or_404(request.form.get('id'))
		priority_id.priority = form.priority.data
		db.session.commit()
		flash('Priority has been updated.', 'primary')
		return redirect(url_for('admin.priority'))
	return render_template('admin/priority.html', form=form)

@admin_blueprint.route('/priority/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_priority(id):
	if request.method == 'POST':
		priority_id = Priority.query.get_or_404(id)
		db.session.delete(priority_id)
		db.session.commit()
		flash('Priority has been deleted.', 'primary')
		return redirect(url_for('admin.priority'))
	return redirect(url_for('admin.priority'))

@admin_blueprint.route('/statuses', methods=['GET', 'POST'])
@login_required(role='admin')
def status():
	statuses = Status.query.order_by(Status.id.desc()).all()
	form = StatusForm()
	if form.validate_on_submit():
		status = Status(status=form.status.data)
		db.session.add(status)
		db.session.commit()
		flash('Status has been created.', 'primary')
		return redirect(url_for('admin.status'))
	return render_template('admin/status.html', statuses=statuses, form=form)

@admin_blueprint.route('/status/update', methods=['GET', 'POST'])
@login_required(role='admin')
def update_status():
	form = StatusForm()
	if form.validate_on_submit():
		status_id = Status.query.get_or_404(request.form.get('id'))
		status_id.status = form.status.data
		db.session.commit()
		flash('Status has been updated.', 'primary')
		return redirect(url_for('admin.status'))
	return render_template('admin/status.html', form=form)

@admin_blueprint.route('/status/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_status(id):
	if request.method == 'POST':
		status_id = Status.query.get_or_404(id)
		db.session.delete(status_id)
		db.session.commit()
		flash('Status has been deleted.', 'primary')
		return redirect(url_for('admin.status'))
	return redirect(url_for('admin.status'))

@admin_blueprint.route('/user_management', methods=['GET', 'POST'])
def user():
	users = User.query.order_by(User.id.desc()).all()
	form = UserForm()
	if form.validate_on_submit():
		public_id = str(uuid.uuid4())
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(
			public_id=public_id,
			name=form.name.data,
			email=form.email.data,
			password=hashed_password,
			role=form.role.data
		)
		db.session.add(user)
		db.session.commit()

		flash('User has been created.', 'primary')
		return redirect(url_for('admin.user'))
	return render_template('admin/user_management.html', users=users, form=form)

@admin_blueprint.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_user(id):
	if request.method == 'POST':
		user_id = User.query.get_or_404(id)
		db.session.delete(user_id)
		db.session.commit()
		flash('User has been deleted.', 'primary')
		return redirect(url_for('admin.user'))
	return redirect(url_for('admin.user'))

@admin_blueprint.route('/account_settings', methods=['GET', 'POST'])
@login_required(role='admin')
def account_settings():
	user = User.query.filter(User.id == current_user.id)
	email_form = EmailUpdateForm()
	password_form = PasswordChangeForm()
	if email_form.validate_on_submit():
		user_id = User.query.get_or_404(request.form.get('id'))
		user_id.email = email_form.email.data
		db.session.commit()

		flash('Email has been updated.', 'primary')
		redirect(url_for('admin.account_settings'))
	if password_form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(password_form.password.data).decode('utf-8')
		user_id = User.query.get_or_404(request.form.get('id'))
		user_id.password = hashed_password
		db.session.commit()

		flash('Password has been changed.', 'primary')
		redirect(url_for('admin.account_settings'))
	return render_template('admin/account_settings.html', user=user, email_form=email_form, password_form=password_form)

@admin_blueprint.route('/account/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_account(id):
	if request.method == 'POST':
		user_id = User.query.get_or_404(id)
		db.session.delete(user_id)
		db.session.commit()
		flash('Your account has been permanently deleted.', 'warning')
		return redirect(url_for('auth.logout'))
	return redirect(url_for('admin.account_settings'))