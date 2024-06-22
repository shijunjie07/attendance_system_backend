# --------------------------------------
# database handler on insert and query
# @author: Shi Junjie A178915
# Sun 16 June 2024
# --------------------------------------

from functools import wraps

from .app import app, db
from datetime import datetime, timedelta
from .models import Course, Class, Attendance, Lecturer, Device, \
    Student, course_student, course_lecturer


class SQLHandler:

    def __init__(self):
        pass

    def with_app_context(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with app.app_context():
                return func(self, *args, **kwargs)
        return wrapper
    
    # insert
    @with_app_context
    def insert_class(
        self, course_code:str, start_time:str,
        end_time:str, location:str, lecturer_id:str,
    ):
        """insert class

        Args:
            course_code (str): _description_
            start_time (str): _description_
            end_time (str): _description_
            location (str): _description_
            lecturer_id (str): _description_
        """
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
        
    @with_app_context
    def insert_course(self, code:str, name:str):
        """insert course

        Args:
            code (str): _description_
            name (str): _description_
        """
        new_course = Course(code=code, name=name)
        db.session.add(new_course)
        db.session.commit()
    
    @with_app_context
    def insert_attendance(
        self, course_code:str, class_id:int,
        student_id:str, record_time:str, status:str
    ):
        """insert attendance

        Args:
            course_code (str): _description_
            class_id (int): _description_
            student_id (str): _description_
            record_time (str): _description_
            status (str): _description_
        """
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
    
    @with_app_context
    def insert_student(
        self, student_id:str, first_name:str,
        last_name:str, phone_number:str, email:str, embedding:bytes
    ):
        """insert student

        Args:
            student_id (str): _description_
            first_name (str): _description_
            last_name (str): _description_
            phone_number (str): _description_
            email (str): _description_
            embedding (bytes): _description_
        """
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

    @with_app_context
    def insert_lecturer(
        self, lecturer_id:str, first_name:str,
        last_name:str, phone_number:str, email:str, embedding:bytes
    ):
        """insert lecturer

        Args:
            lecturer_id (str): _description_
            first_name (str): _description_
            last_name (str): _description_
            phone_number (str): _description_
            email (str): _description_
            embedding (bytes): _description_
        """
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
    @with_app_context
    def add_lecturer_to_course(
        self, course_code:str, lecturer_id:str
    ):
        """create relationship between lecturer and course

        Args:
            course_code (str): _description_
            lecturer_id (str): _description_
        """
        lecturer_to_course = course_lecturer.insert().values(
            course_code=course_code, lecturer_id=lecturer_id)
        db.session.execute(lecturer_to_course)
        db.session.commit()

    @with_app_context
    def add_student_to_course(
        self, course_code:str, student_id:str
    ):
        """create relationship between student and course

        Args:
            course_code (str): _description_
            student_id (str): _description_
        """
        student_to_course = course_student.insert().values(
            course_code=course_code, student_id=student_id)
        db.session.execute(student_to_course)
        db.session.commit()

    @with_app_context
    def insert_device(
        self, ip:str, port:int, location:str
    ):
        """insert attendance device

        Args:
            ip (str): device ip
            port (int): port to listen
            location (str): device classroom location

        Returns:
            _type_: List | Query
        """
        new_device = Device(
            ip=ip,
            port=port,
            location=location,
        )
        db.session.add(new_device)
        db.session.commit()


    # get
    @with_app_context
    def get_lecturers_by_course(self, course_code:str):
        """get lecturers of course

        Args:
            course_code (str): _description_

        Returns:
            _type_: List | Query
        """
        course = Course.query.filter_by(code=course_code).first()
        return course.lecturers if course else []

    @with_app_context
    def get_classes(self, by:str, **query_params):
        """get classes

        Args:
            by (str): student, lecturer, date, location

        Returns:
            _type_: List | Query
        """

        query = Class.query
        
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

    @with_app_context
    def get_courses(self, by:str, **query_params):
        """get courses

        Args:
            by (str): student, lecturer, date

        Returns:
            _type_: List | Query
        """

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
    
    @with_app_context
    def get_attendances(self, by: str, **query_params):
        """get attendances

        Args:
            by (str): student, course, class, class_date

        Returns:
            _type_: List | Query
        """
        query = Attendance.query
        
        if by == 'student':
            student_id = query_params.get('student_id')
            if student_id:
                query = query.filter_by(student_id=student_id)
        
        elif by == 'course':
            course_code = query_params.get('course_code')
            if course_code:
                query = query.join(Class).filter(Class.course_code==course_code)

        elif by == 'course_student':
            course_code = query_params.get('course_code')
            student_id = query_params.get('student_id')
            if course_code and student_id:
                query = query.filter_by(course_code=course_code, student_id=student_id)
        
        elif by == 'class':
            class_id = query_params.get('class_id')
            if class_id:
                query = query.filter_by(class_id=class_id)

        return query.all()
    
    @with_app_context
    def get_student(self, id:str):
        """get student by id

        Args:
            id (str): _description_

        Returns:
            _type_: Any | None
        """
        return Student.query.get(id)
    
    @with_app_context
    def get_lecturer(self, id:str):
        """get lecturer by id

        Args:
            id (str): _description_

        Returns:
            _type_: Any | None
        """
        return Lecturer.query.get(id)
    
    @with_app_context
    def get_device(self, by: str=None, all=False, **query_params):
        """get device information

        Args:
            by (str): ip, location

        Returns:
            _type_: List | Query
        """
        query = Device.query
        
        if all:
            return query.all()

        # by ip
        if by == 'ip':
            ip = query_params.get('ip')
            if ip:
                query = query.filter_by(ip=ip)
        
        # by location
        elif by == 'location':
            location = query_params.get('location')
            if location:
                query = query.filter_by(location=location)
        
        return query.all()