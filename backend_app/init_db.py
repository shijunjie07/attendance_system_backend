# --------------------------
# initialise database
# @author: Shi Junjie
# Sat 8 June 2024
# --------------------------

from .backend import app, db
from .models import Course, Class, Attendance, Lecturer, Student, Device, \
    course_student, course_lecturer
from datetime import datetime, timedelta
from .utils import Utils
import torch

devices = {
    'demo_1': {
        'ip': '0.0.0.1',
        'port': 80,
    },
    'demo_2': {
        'ip': '0.0.0.2',
        'port': 80,
    },
    'FKAB DK1': {
        'ip': '0.0.0.0',
        'port': 80,
    },
    'FKAB DK6': {
        'ip': '0.0.0.3',
        'port': 80,
    },
    'FKAB DK2': {
        'ip': '0.0.0.4',
        'port': 80,
    },
    'FKAB BS5': {
        'ip': '0.0.0.5',
        'port': 80,
    },
    'FKAB BS1': {
        'ip': '0.0.0.6',
        'port': 80,
    },
    'FKAB ASTMK1': {
        'ip': '0.0.0.7',
        'port': 80,
    },
}

mock_courses = {
        'KKEE3153': 'System Design',
        'KKEE3163': 'Digital Signal Processing',
        'KKEC3113': 'Embedded Systems',
        'KKEE3133': 'Power System Analysis',
        'KKKQ3123': 'Statistics and Numerical Method',
        'KKEE3123': 'Control Engineering',
        'KKEE3143': 'Microprocessor and Microcomputer',
        'KKEC3103': 'Object Oriented Programming',
        'KKKF3103': 'Project Management',
        'KKET3103': 'Data Communication and Computer Networks',
        'KKKL3183': 'Digital Signal Processing',
        'KKKF3283': 'Engineering Ethics and Technological Advancement',
        'KKEE3113': 'Measurements and Instrumentation',
        'KKEE4103': 'Electrical Machine, Drives and Application',
        'KKET4113': 'Network and Security',
}

# Mock data for classes
mock_classes = {
    "FKAB DK1": [
        {"course_code": "KKEE3153", "course_name": "System Design", "start_time": datetime(2024, 6, 15, 15, 0, 0), "end_time": (datetime(2024, 6, 15, 15, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKEE3163", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 15, 17, 0, 0), "end_time": (datetime(2024, 6, 15, 17, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEC3113", "course_name": "Embedded Systems", "start_time": datetime(2024, 6, 16, 11, 0, 0), "end_time": (datetime(2024, 6, 16, 11, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB DK6": [
        {"course_code": "KKEE3133", "course_name": "Power System Analysis", "start_time": datetime(2024, 6, 15, 9, 0, 0), "end_time": (datetime(2024, 6, 15, 9, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKKQ3123", "course_name": "Statistics and Numerical Method", "start_time": datetime(2024, 6, 15, 10, 0, 0), "end_time": (datetime(2024, 6, 15, 10, 0, 0) + timedelta(hours=2))},
        {"course_code": "KKEE3123", "course_name": "Control Engineering", "start_time": datetime(2024, 6, 16, 14, 0, 0), "end_time": (datetime(2024, 6, 16, 14, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB DK2": [
        {"course_code": "KKEE3143", "course_name": "Microprocessor and Microcomputer", "start_time": datetime(2024, 6, 10, 10, 0, 0), "end_time": (datetime(2024, 6, 10, 10, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEC3103", "course_name": "Object Oriented Programming", "start_time": datetime(2024, 6, 15, 13, 0, 0), "end_time": (datetime(2024, 6, 15, 13, 0, 0) + timedelta(hours=1))},
        {"course_code": "KKKF3103", "course_name": "Project Management", "start_time": datetime(2024, 6, 17, 9, 0, 0), "end_time": (datetime(2024, 6, 17, 9, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB BS5": [
        {"course_code": "KKET3103", "course_name": "Data Communication and Computer Networks", "start_time": datetime(2024, 6, 12, 10, 0, 0), "end_time": (datetime(2024, 6, 12, 10, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKKL3183", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 13, 11, 0, 0), "end_time": (datetime(2024, 6, 13, 11, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB BS1": [
        {"course_code": "KKKF3283", "course_name": "Engineering Ethics and Technological Advancement", "start_time": datetime(2024, 6, 14, 14, 0, 0), "end_time": (datetime(2024, 6, 14, 14, 0, 0) + timedelta(hours=3))},
        {"course_code": "KKEE3113", "course_name": "Measurements and Instrumentation", "start_time": datetime(2024, 6, 18, 8, 0, 0), "end_time": (datetime(2024, 6, 18, 8, 0, 0) + timedelta(hours=2))}
    ],
    "FKAB ASTMK1": [
        {"course_code": "KKEE4103", "course_name": "Electrical Machine, Drives and Application", "start_time": datetime(2024, 6, 20, 12, 0, 0), "end_time": (datetime(2024, 6, 20, 12, 0, 0) + timedelta(hours=2))},
        {"course_code": "KKET4113", "course_name": "Network and Security", "start_time": datetime(2024, 6, 21, 14, 0, 0), "end_time": (datetime(2024, 6, 21, 14, 0, 0) + timedelta(hours=2))}
    ]
}

# Mock data for lecturers
mock_lecturers = {
    'L000001': {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': list(mock_courses.keys()),
    },
    'L000002': {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3133', 'KKEC3113']
    },
    'L000003': {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice.johnson@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3123', 'KKEC3113', 'KKEE4103']
    },
    'L000004': {
        'first_name': 'Bob',
        'last_name': 'Williams',
        'email': 'bob.williams@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKEE3143', 'KKEC3103', 'KKKF3103']
    },
    'L000005': {
        'first_name': 'Charlie',
        'last_name': 'Brown',
        'email': 'charlie.brown@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKET3103', 'KKEC3103', 'KKEC3113', 'KKET4113']
    },
    'L000006': {
        'first_name': 'Emily',
        'last_name': 'Davis',
        'email': 'emily.davis@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKL3183', 'KKKF3283', 'KKEE3113']
    },
}

# Mock data for students
mock_students = {
    'A000001': {
        'first_name': 'Michael',
        'last_name': 'Clark',
        'email': 'michael.clark@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKEE3153', 'KKEE3163', 'KKEC3113', 'KKET3103', 'KKEE3143']
    },
    'A000002': {
        'first_name': 'Sophia',
        'last_name': 'Martinez',
        'email': 'sophia.martinez@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3133', 'KKEC3113', 'KKEE3143']
    },
    'A000003': {
        'first_name': 'Ethan',
        'last_name': 'Taylor',
        'email': 'ethan.taylor@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKQ3123', 'KKEE3123', 'KKEC3113', 'KKEE4103', 'KKEE3133'],
    },
    'A000004': {
        'first_name': 'Isabella',
        'last_name': 'Anderson',
        'email': 'isabella.anderson@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKEE3143', 'KKEC3103', 'KKKF3103']
    },
    'A000005': {
        'first_name': 'Daniel',
        'last_name': 'Thomas',
        'email': 'daniel.thomas@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKET3103', 'KKEC3103', 'KKEC3113', 'KKET4113', 'KKEE4103']
    },
    'A000006': {
        'first_name': 'Mia',
        'last_name': 'Moore',
        'email': 'mia.moore@example.com',
        'embedding': Utils.convert_tensor_to_binary(torch.randn(1, 512)),
        'courses': ['KKKL3183', 'KKKF3283', 'KKEE3113', 'KKEE4103']
    },
}

def add_mock_data():
    # Add courses
    for code, name in mock_courses.items():
        course = Course(code=code, name=name)
        db.session.add(course)

    # Add lecturers and link to courses
    for lecturer_id, lecturer_data in mock_lecturers.items():
        lecturer = Lecturer(
            lecturer_id=lecturer_id,
            first_name=lecturer_data['first_name'],
            last_name=lecturer_data['last_name'],
            email=lecturer_data['email'],
            embedding=lecturer_data['embedding']
        )
        db.session.add(lecturer)
        for course_code in lecturer_data['courses']:
            course = Course.query.filter_by(code=course_code).first()
            lecturer.courses.append(course)

    # Add students and link to courses
    for student_id, student_data in mock_students.items():
        student = Student(
            student_id=student_id,
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            email=student_data['email'],
            embedding=student_data['embedding']
        )
        db.session.add(student)
        for course_code in student_data['courses']:
            course = Course.query.filter_by(code=course_code).first()
            student.courses.append(course)

    # Add classes and attendance
    for location, classes in mock_classes.items():
        for class_data in classes:
            class_session = Class(
                course_code=class_data['course_code'],
                start_time=class_data['start_time'],
                end_time=class_data['end_time'],
                location=location,
                lecturer_id='L000001'  # Assuming the lecturer is L000001 for simplicity
            )
            db.session.add(class_session)
            db.session.flush()

            # Add attendance for each student in the course
            students_in_course = Student.query.join(course_student).filter(course_student.c.course_code == class_data['course_code']).all()
            for student in students_in_course:
                attendance = Attendance(
                    course_code=class_data['course_code'],
                    class_id=class_session.class_id,
                    student_id=student.student_id,
                    record_time=class_data['start_time'],
                    status='present'
                )
                db.session.add(attendance)

    # Add attendance device
    for location, network in devices.items():
        device = Device(
            ip=network['ip'],
            port=network['port'],
            location=location,
        )
        db.session.add(device)

    db.session.commit()

def init_db():
    with app.app_context():
        # init db for the first time
        db.create_all()
        print("database initialised and tables created")
        
        add_mock_data()
        print("Sample data added")

if __name__ == "__main__":
    init_db()