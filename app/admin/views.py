from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from sqlalchemy import or_
from app.admin.forms import TicketForm, CategoryForm, PriorityForm, StatusForm
from app.models import User, Ticket, Category, Priority, Status
from app.decorators import login_required
from app import db
import uuid

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/dashboard')
@login_required(role='admin')
def dashboard():
	return render_template('admin/dashboard.html')

@admin_blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required(role='admin')
def ticket():
	# users = User.query.filter(or_(User.role=='admin', User.role=='agent')).all()
	tickets = Ticket.query.all()
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
			category_id=form.category.data,
			priority_id=priority,
			status_id=status
		)
		
		db.session.add(ticket)
		db.session.commit()
		flash('Category has been created.', 'success')
		return redirect(url_for('admin.ticket'))
	return render_template('admin/ticket.html', tickets=tickets, form=form)

@admin_blueprint.route('/ticket/update/<int:id>/<public_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def update_ticket(id, public_id):
	users = User.query.filter(or_(User.role=='admin', User.role=='agent')).all()
	ticket = Ticket.query.filter_by(id=id)
	categories = Category.query.all()
	priorities = Priority.query.all()
	statuses = Status.query.all()
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		ticket_id.subject = request.form['subject']
		ticket_id.body = request.form['body']
		
		if not request.form['owner_id']:
			ticket_id.owner_id = None
		else:
			ticket_id.owner_id = request.form['owner_id']

		ticket_id.category_id = request.form['category']
		ticket_id.priority_id = request.form['priority']
		ticket_id.status_id = request.form['status']
		db.session.commit()
		flash('Ticket has been updated.', 'success')
		return redirect(url_for('admin.update_ticket', id=id, public_id=public_id))
	return render_template('admin/ticket_update.html', users=users, ticket=ticket, categories=categories, priorities=priorities, statuses=statuses)

@admin_blueprint.route('/ticket/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_ticket(id):
	if request.method == 'POST':
		ticket_id = Ticket.query.get_or_404(id)
		db.session.delete(ticket_id)
		db.session.commit()
		flash('Ticket has been deleted.', 'success')
		return redirect(url_for('admin.ticket'))
	return redirect(url_for('admin.ticket'))

@admin_blueprint.route('/categories', methods=['GET', 'POST'])
@login_required(role='admin')
def category():
	categories = Category.query.all()
	form = CategoryForm()
	if form.validate_on_submit():
		category = Category(category=form.category.data)
		db.session.add(category)
		db.session.commit()
		flash('Category has been created.', 'success')
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
		flash('Category has been updated.', 'success')
		return redirect(url_for('admin.category'))
	return render_template('admin/category.html', form=form)

@admin_blueprint.route('/category/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_category(id):
	if request.method == 'POST':
		category_id = Category.query.get_or_404(id)
		db.session.delete(category_id)
		db.session.commit()
		flash('Category has been deleted.', 'success')
		return redirect(url_for('admin.category'))
	return redirect(url_for('admin.category'))

@admin_blueprint.route('/priorities', methods=['GET', 'POST'])
@login_required(role='admin')
def priority():
	priorities = Priority.query.all()
	form = PriorityForm()
	if form.validate_on_submit():
		priority = Priority(priority=form.priority.data)
		db.session.add(priority)
		db.session.commit()
		flash('Priority has been created.', 'success')
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
		flash('Priority has been updated.', 'success')
		return redirect(url_for('admin.priority'))
	return render_template('admin/priority.html', form=form)

@admin_blueprint.route('/priority/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_priority(id):
	if request.method == 'POST':
		priority_id = Priority.query.get_or_404(id)
		db.session.delete(priority_id)
		db.session.commit()
		flash('Priority has been deleted.', 'success')
		return redirect(url_for('admin.priority'))
	return redirect(url_for('admin.priority'))

@admin_blueprint.route('/statuses', methods=['GET', 'POST'])
@login_required(role='admin')
def status():
	statuses = Status.query.all()
	form = StatusForm()
	if form.validate_on_submit():
		status = Status(status=form.status.data)
		db.session.add(status)
		db.session.commit()
		flash('Status has been created.', 'success')
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
		flash('Status has been updated.', 'success')
		return redirect(url_for('admin.status'))
	return render_template('admin/status.html', form=form)

@admin_blueprint.route('/status/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_status(id):
	if request.method == 'POST':
		status_id = Status.query.get_or_404(id)
		db.session.delete(status_id)
		db.session.commit()
		flash('Status has been deleted.', 'success')
		return redirect(url_for('admin.status'))
	return redirect(url_for('admin.status'))