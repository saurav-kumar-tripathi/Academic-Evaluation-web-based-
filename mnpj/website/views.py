from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User, Semester, Subject
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
'''
Todo :
	- home page
	- admin page
	- student page
'''
# login_required -> decoration. To make sure user is logged in before accessing the said page(@) and decorations require @


views=Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
	if request.method=='POST':
		university_roll = request.form.get('uRoll')
		password = request.form.get('password')

		# print(university_roll)
		# print(password+'.')

		user = User.query.filter_by(university_roll=university_roll).first()
		if user:
			if check_password_hash(user.password,password):
				if user.position=="admin":
					flash("Can't login!")
				else:
					login_user(user, remember=True)
					flash('Logged in!')
					return redirect(url_for('views.student'))
			else:
				flash('Incorrect Password!')
		else:
			flash('Incorrect student university roll number!')

	return render_template('home.html', user = current_user)

@views.route('/admin', methods=['GET','POST'])
@login_required
def admin():
	if request.method == 'POST':
		university_roll = request.form.get('uRoll')
		semester = request.form.get('semester').lower()
		subject1 = int(request.form.get('subject1'))
		subject2 = int(request.form.get('subject2'))
		subject3 = int(request.form.get('subject3'))
		subject4 = int(request.form.get('subject4'))
		subject5 = int(request.form.get('subject5'))
		subject6 = int(request.form.get('subject6'))
		credit1 = int (request.form.get('credit1'))
		credit2 = int (request.form.get('credit2'))
		credit3 = int (request.form.get('credit3'))
		credit4 = int (request.form.get('credit4'))
		credit5 = int (request.form.get('credit5'))
		credit6 = int (request.form.get('credit6'))

		subject_name = ["CAREER SKILLS", "OPERATING SYSTEM", "SYSTEM SOFTWARE", "DBMS", "ELECTIVE", "DAA"]

		s_list = [subject1, subject2, subject3, subject4, subject5, subject6]
		c_list = [credit1, credit2, credit3, credit4, credit5, credit6]

		student_exists = User.query.filter_by(university_roll=university_roll).first()
		if student_exists:
			new_semester = Semester(semester=semester, sgpa=(sum(s_list)/sum(c_list)), author=student_exists.id)
			db.session.add(new_semester)
			db.session.commit()

			semester_d=Semester.query.filter_by(semester=semester).first()
			for i in range(1,7):
				subject_details = Subject(subject_name = subject_name[i-1],
						marks_obtained = s_list[i-1], credit=c_list[i-1], author=student_exists.id, semester_id=semester_d.id)
				db.session.add(subject_details)
				db.session.commit()


	return render_template('admin.html', user = current_user, users = User.query.all())

@views.route('/student')
@login_required
def student():
	semesters=Semester.query.all()
	subjects=Subject.query.all()
	l = []
	for semester in semesters:
		if semester.author == current_user.id:
			l.append(semester.sgpa)
	try:
		cgpa=round(sum(l)/len(l),2)
	except:
		cgpa=None
	return render_template('student.html', user = current_user, semesters=semesters, subjects=subjects, cgpa=cgpa)