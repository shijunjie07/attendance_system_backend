# --------------------------
# db tables
# @author: Shi Junjie
# Fri 7 June 2024
# --------------------------

from .app import db

# # tables for many-to-many relationships
course_lecturer = db.Table('course_lecturer',
    db.Column('course_code', db.String(10), db.ForeignKey('courses.code'), primary_key=True),
    db.Column('lecturer_id', db.String(10), db.ForeignKey('lecturers.lecturer_id'), primary_key=True)
)

course_student = db.Table('course_student',
    db.Column('course_code', db.String(10), db.ForeignKey('courses.code'), primary_key=True),
    db.Column('student_id', db.String(10), db.ForeignKey('students.student_id'), primary_key=True)
)


class Lecturer(db.Model):
    __tablename__ = 'lecturers'
    lecturer_id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    embedding = db.Column(db.LargeBinary, nullable=False)  # Binary to store facial embedding
    # Relationship back to courses
    courses = db.relationship('Course', secondary=course_lecturer, back_populates='lecturers')

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    embedding = db.Column(db.LargeBinary, nullable=False)  # Binary to store facial embedding
    # Relationship back to courses
    courses = db.relationship('Course', secondary=course_student, back_populates='students')

class Course(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lecturers = db.relationship('Lecturer', secondary=course_lecturer, back_populates='courses')
    students = db.relationship('Student', secondary=course_student, back_populates='courses')

class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    lecturer_id = db.Column(db.String(10), db.ForeignKey('lecturers.lecturer_id'), nullable=False)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('students.student_id'), nullable=False)
    record_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'present', 'late', 'absent', 'excused'

class Device(db.Model):
    __tablename__ = 'device'
    ip = db.Column(db.String(15), primary_key=True, unique=True)
    port = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), db.ForeignKey('classes.location'), nullable=False, unique=True)