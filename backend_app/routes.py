from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from datetime import datetime, timedelta
from .app import app
from .sql_handler import SQLHandler
from .device_manager import start_stream, stop_stream
sql_handler = SQLHandler()


ESP_DEVICES = sql_handler.get_device(all=True)
CLASSES = sql_handler.get_classes(by='date', date='2024-06-15')

ESP_PORT = 80
CHECK_INTERVAL = 600  # Interval in seconds to check device status (10 minutes)

device_status = {device.ip: {"status": "Unknown", "location": device.location} for device in ESP_DEVICES}

def get_class_schedules(class_date):
    classes_of_the_date = sql_handler.get_classes(by='date', date=class_date)
    location_classes = {class_.location: [] for class_ in classes_of_the_date}
    for class_ in classes_of_the_date:
        course = sql_handler.get_courses(by='code', code=class_.course_code)[0]
        location_classes[class_.location].append({
            'course_code': class_.course_code,
            'course_name': course.name,
            'start_time': class_.start_time.strftime("%Y-%m-%d %H:%M"),
            'end_time': class_.end_time.strftime("%Y-%m-%d %H:%M")
        })
    return location_classes

@app.route('/')
def index():
    class_date = '2024-06-15'
    location_classes = get_class_schedules(class_date)
    locations = list(location_classes.keys())
    course_codes = [cls['course_code'] for classes in location_classes.values() for cls in classes]
    return render_template(
        'index.html', locations=locations, course_codes=course_codes,
        location_classes=location_classes, device_status=device_status
    )

@app.route('/status')
def status():
    class_date = '2024-06-15'
    location_classes = get_class_schedules(class_date)
        
    status_with_classes = {}
    for device in ESP_DEVICES:
        ip = device.ip
        location = device.location
        status_with_classes[ip] = {
            'status': device_status[ip]['status'],
            'location': location,
            'classes': location_classes.get(location, [])
        }

    return jsonify(status_with_classes)

@app.route('/start/<ip>')
def start(ip):
    print('start ip: {}'.format(ip))
    success = start_stream(ip, port=80)
    if success:
        device_status[ip]["status"] = "Stream Started"
    else:
        device_status[ip]["status"] = "Failed to Start Stream"
    return redirect(url_for('index'))

@app.route('/stop/<ip>')
def stop(ip):
    success = stop_stream(ip, port=80)
    if success:
        device_status[ip]["status"] = "Stream Stopped"
    else:
        device_status[ip]["status"] = "Failed to Stop Stream"
    return redirect(url_for('index'))

@app.route('/start_all')
def start_all():
    for device in ESP_DEVICES:
        start_stream(device.ip, port=80)
    return redirect(url_for('index'))

@app.route('/stop_all')
def stop_all():
    for device in ESP_DEVICES:
        stop_stream(device.ip, port=80)
    return redirect(url_for('index'))