# --------------------------------------
# database handler on insert and query
# @author: Shi Junjie A178915
# 16 June June 2024
# --------------------------------------

from backend import db
from typing import Dict
from datetime import datetime, timedelta
from models import Course, Class, Attendance, Lecturer, \
    Student, course_student, course_lecturer

class SQLHandler:
    
    def __init__(self):
        pass
    
    # insert
    def insert_class(
        self, course_code:str, start_time:str,
        end_time:str, location:str, lecturer_id:str,
    ):
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        new_class = Class(
            course_code=course_code,
            start_time=start_time,
            end_time=end_time,
            location=location,
            Lecturer_id=lecturer_id,
        )
        db.session.add(new_class)
        db.session.commit()
        
    def insert_course(self, code:str, name:str):
        new_course = Course(code=code, name=name)
        db.session.add(new_course)
        db.session.commit()
    
    def insert_attendance(
        self, course_code:str, class_id:int,
        student_id:str, record_time:str, status:str
    ):
        record_time = datetime.strptime(record_time, '%Y-%m-%d %H:%M')
        new_attendance = Attendance(
            course_code=course_code,
            class_id=class_id,
            student_id=student_id,
            record_time=record_time,
            status=status
        )
        db.session.add(new_attendance)
        db.session.commit()
    
    def insert_student(
        self, student_id:str, first_name:str,
        last_name:str, phone_number:str, email:str, embedding:bytes
    ):
        new_student = Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            embedding=embedding
        )
        db.session.add(new_student)
        db.session.commit()
    
    def insert_lecturer(
        self, lecturer_id:str, first_name:str,
        last_name:str, phone_number:str, email:str, embedding:bytes
    ):
        new_lecturer = Lecturer(
            lecturer_id=lecturer_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            embedding=embedding
        )
        db.session.add(new_lecturer)
        db.session.commit()


    # add to course
    def add_lecturer_to_course(
        self, course_code:str, lecturer_id:str
    ):
        lecturer_to_course = course_lecturer.insert().values(
            course_code=course_code, lecturer_id=lecturer_id)
        db.session.execute(lecturer_to_course)
        db.session.commit()

    def add_student_to_course(
        self, course_code:str, student_id:str
    ):
        student_to_course = course_student.insert().values(
            course_code=course_code, student_id=student_id)
        db.session.execute(student_to_course)
        db.session.commit()
        

    # get
    def get_lecturers_by_course(self, course_code:str):
        course = Course.query.filter_by(code=course_code).first()
        return course.lecturers if course else []

    def get_classes(self, by:str, **query_params):
        # by student, lecturer, date, location
        class_query = Class.query
        
        if by == 'student':
            student_id = query_params.get('student_id')
            if student_id:
                query = query.join(Course).join(course_student).filter(
                    course_student.c.student_id == student_id)
        
        elif by == 'lecturer':
            lecturer_id = query_params.get('lecturer_id')
            if lecturer_id:
                query = query.filter_by(lecturer_id=lecturer_id)
        
        elif by == 'date':
            date = query_params.get('date')
            if date:
                start_of_day = datetime.strptime(date, '%Y-%m-%d')
                end_of_day = start_of_day + timedelta(days=1)
                query = query.filter(Class.start_time.between(start_of_day, end_of_day))
        
        elif by == 'location':
            location = query_params.get('location')
            if location:
                query = query.filter_by(location=location)

        return query.all()

    def get_courses(self, by:str, **query_params):
        # by student, lecturer, date
        query = Course.query
        
        if by == 'student':
            student_id = query_params.get('student_id')
            if student_id:
                query = query.join(course_student).filter(course_student.c.student_id == student_id)
        
        elif by == 'lecturer':
            lecturer_id = query_params.get('lecturer_id')
            if lecturer_id:
                query = query.join(course_lecturer).filter(course_lecturer.c.lecturer_id == lecturer_id)
        
        elif by == 'date':
            date = query_params.get('date')
            if date:
                start_of_day = datetime.strptime(date, '%Y-%m-%d')
                end_of_day = start_of_day + timedelta(days=1)
                query = query.join(Class).filter(Class.start_time.between(start_of_day, end_of_day))
        
        return query.all()
    
    def get_attendances(self, by: str, **query_params):
        # by student, course, class, class_date
        query = Attendance.query
        
        if by == 'student':
            student_id = query_params.get('student_id')
            if student_id:
                query = query.filter_by(student_id=student_id)
        
        elif by == 'course':
            course_code = query_params.get('course_code')
            if course_code:
                query = query.filter_by(course_code=course_code)

        return query.all()
    
    def get_student(self, id:str):
        return Student.query.get(id)
    
    def get_lecturer(self, id:str):
        return Lecturer.query.get(id)