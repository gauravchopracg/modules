from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm, ResetPasswordRequestForm, ResetPasswordForm, EmailForm, EmailForm2
from app.models import User, Task
from app.email import send_password_reset_email, send_todo_list_email
from overlook_utils import *

dict1 = {1 : 'High',
        2 : 'Medium',
        3 : 'Low'}

#dict2 = {'High': 'bg-danger text-white',
#         'Medium': 'bg-warning text-white',
#         'Low': 'bg-success text-white',}

dict2 = {'High': 'panel-danger',
         'Medium': 'panel-warning',
         'Low': 'panel-success',}

dict3 = {0: 'Incomplete',
         1: 'Complete'}


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    articles = get_toi_feed()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(body=form.task.data, author=current_user)
        task.priority = dict1[form.priority.data]
        task.status = dict3[form.status.data]
        task.color = dict2[task.priority]
        db.session.add(task)
        db.session.commit()
        flash('Your task is now added!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    tasks = current_user.tasks.paginate(
        page, app.config['TASKS_PER_PAGE'], False)
    next_url = url_for('index', page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('index', page=tasks.prev_num) \
        if tasks.has_prev else None
    return render_template('index.html', title='Home', articles=articles['NewsItem'],# form=form,
                           posts=tasks.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/delete/<id>')
@login_required
def delete(id):
    task = Task.query.get(id)
    if task is None:
        flash('Task not found.')
        return redirect(url_for('index'))
    if task.author.id != g.user.id:
        flash('You cannot delete this task.')
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been removed.')
    return redirect(url_for('index'))

@app.route('/del_all')
@login_required
def del_all():
    tasks = current_user.tasks.all()
    for t in tasks:
        db.session.delete(t)
    db.session.commit()
    flash('All tasks have been deleted')
    return redirect(url_for('index'))

@app.route('/export_mail', methods=['GET', 'POST'])
@login_required
def export_mail():
    form = EmailForm()
    if form.validate_on_submit():
        recipient = form.email.data
        text_body = form.msg.data
        tasks = current_user.tasks.all()
        send_todo_list_email(recipient, text_body, tasks)
        flash('Mailed Successfully!')
        return redirect(url_for('export_mail'))

    form2 = EmailForm2()
    if form2.validate_on_submit():
        recipient = current_user.email
        text_body = form2.msg.data
        tasks = current_user.tasks.all()
        send_todo_list_email(recipient, text_body, tasks)
        flash('Mailed Successfully!')
        return redirect(url_for('export_mail'))    
    return render_template('export_mail.html', form=form, form2=form2)

@app.route('/complete/<id>')
@login_required
def complete(id):
    task = Task.query.get(id)
    if task is None:
        flash('Task not found.')
    task.status = 'Complete'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/incomplete/<id>')
@login_required
def incomplete(id):
    task = Task.query.get(id)
    if task is None:
        flash('Task not found.')
    task.status = 'Incomplete'
    db.session.commit()
    return redirect(url_for('index'))