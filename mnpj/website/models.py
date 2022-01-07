from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text)
	university_roll = db.Column(db.Text)
	password = db.Column(db.String(800))
	position = db.Column(db.Text)
	date_created = db.Column(db.DateTime(timezone=True), default=func.now())
	semester = db.relationship('Semester', backref='user', passive_deletes=True)
	subject = db.relationship('Subject', backref='user', passive_deletes=True)

class Semester(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	semester = db.Column(db.Text)
	sgpa = db.Column(db.Integer)
	date_created = db.Column(db.DateTime(timezone=True), default=func.now())
	author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # store user table's id
	subject = db.relationship('Subject', backref='semester', passive_deletes=True)

class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subject_name = db.Column(db.Text)
	marks_obtained = db.Column(db.Integer)
	credit = db.Column(db.Integer)
	date_created = db.Column(db.DateTime(timezone=True), default=func.now())
	author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
	semester_id = db.Column(db.Integer, db.ForeignKey('semester.id', ondelete='CASCADE'), nullable=False)