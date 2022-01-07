from flask import Blueprint, redirect, url_for, render_template, request, flash
from . import db
from .models import User, Semester, Subject
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth=Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET','POST'])
def signup():
	if request.method=='POST':
		name = request.form.get('name')
		university_roll = request.form.get('uRoll')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		# print(university_roll)
		# print(enrollment_roll)
		# print(password)

		university_roll_exists = User.query.filter_by(university_roll=university_roll).first()

		if university_roll_exists:
			flash('University Roll Number already registered!')
		elif password1!=password2:
			flash('Please Confirm Your Password Properly!')
		else:
			new_user = User(
				username=name,
				university_roll=university_roll,
				password=generate_password_hash(password1, method='sha256'),
				position="student"
				)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			flash('User Created!')

			# return redirect(url_for('views.home'))

	return render_template('signup.html', user=current_user)

@auth.route('/admin-login', methods=['GET','POST'])
def admin_login():
	if request.method=='POST':
		username = request.form.get('username')
		password = request.form.get('password')

		# print(username)
		# print(password)

		user = User.query.filter_by(username=username).first()  # database then program

		if user:
			if check_password_hash(user.password,password):
				login_user(user, remember=True)
				flash('Logged in!')
				return redirect(url_for('views.admin'))
			else:
				flash('Incorrect Password!')
		else:
			flash('No such admin!')

	return render_template('admin_login.html', user = current_user)

@auth.route('/admin-signup-sauravtripathi123', methods=['GET','POST'])
def admin_signup():
	if request.method=='POST':
		username = request.form.get('userName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		# print(username)
		# print(password1)
		# print(password2)

		username_exists = User.query.filter_by(username=username).first()

		if username_exists:
			flash('Username already in use!')
		elif password1!=password2:
			flash('Please Confirm Your Password Properly!')
		else:
			new_user = User(
				username=username,
				university_roll=None,
				password=generate_password_hash(password1, method='sha256'),
				position="admin"
				)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			flash('New Admin Added!')

			return redirect(url_for('views.admin'))

	return render_template('admin_signup.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('views.home'))

@auth.route('/delete-user/<id>')
@login_required
def delete_user(id):
	if current_user.position == "admin":
		user = User.query.filter_by(id=id).first()
		semester = Semester.query.filter_by(id=user.semester.id).first()
		subject = Subject.query.filter_by(id=user.subject.id).first()
		if not user:
			flash('User does not exists!')
		else:
			db.session.delete(user)
			db.session.commit()
			db.session.delete(semester)
			db.session.commit()
			db.session.delete(subject)
			db.session.commit()
			flash('User Data deleted!')
	else:
		flash('No funny businesses please ;-)')

	return redirect(url_for('views.admin'))