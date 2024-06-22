from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from datetime import datetime, timedelta
from .app import app
from .sql_handler import SQLHandler
from .device_manager import start_stream, stop_stream
sql_handler = SQLHandler()

SOCKET_SERVER_PORT = 3000
APP_SERVER_PORT = 5001

# Initial list of ESP devices with their IPs and locations
# ESP_DEVICES = [
#     {"ip": "192.168.0.105", "location": "FKAB DK1"},
#     {"ip": "192.168.0.106", "location": "FKAB ASTMK1"},
#     {"ip": "192.168.0.107", "location": "FKAB BS6"}
# ]
ESP_DEVICES = sql_handler.get_device(all=True)

ESP_PORT = 80
CHECK_INTERVAL = 600  # Interval in seconds to check device status (10 minutes)

# Mock data for classes
mock_classes = {
    "FKAB DK1": [
        {"course_code": "KKKL3233", "course_name": "System Design", "start_time": datetime(2024, 6, 15, 15, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 15, 15, 0, 0) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")},
        {"course_code": "KKKL3183", "course_name": "Digital Signal Processing", "start_time": datetime(2024, 6, 15, 17, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 15, 17, 0, 0) + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")}
    ],
    "FKAB ASTMK1": [
        {"course_code": "KKEE3133", "course_name": "Power System Analysis", "start_time": datetime(2024, 6, 15, 9, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 15, 9, 0, 0) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")},
        {"course_code": "KKKQ3123", "course_name": "Statistics and Numerical Method", "start_time": datetime(2024, 6, 15, 10, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 15, 10, 0, 0) + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")}
    ],
    "FKAB BS6": [
        {"course_code": "KKKL3293", "course_name": "Microprocessor and Microcomputer", "start_time": datetime(2024, 6, 10, 10, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 10, 10, 0, 0) + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")},
        {"course_code": "KKEC3103", "course_name": "Object Oriented Programming", "start_time": datetime(2024, 6, 15, 13, 0, 0).strftime("%Y-%m-%d %H:%M"), "end_time": (datetime(2024, 6, 15, 13, 0, 0) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")}
    ],
}

# mock_classes = {}

# mock_classes = {}

device_status = {device.ip: {"status": "Unknown", "location": device.location} for device in ESP_DEVICES}

@app.route('/')
def index():
    class_date = '2024-06-15'
    classes_of_the_date = sql_handler.get_classes(by='date', date=class_date)
    locations = [class_.location for class_ in classes_of_the_date]
    course_codes = [class_.course_code for class_ in classes_of_the_date]
    return render_template('index.html', locations=locations, course_codes=course_codes)

@app.route('/status')
def status():
    status_with_classes = {}
    for device in ESP_DEVICES:
        ip = device.ip
        location = device.location
        status_with_classes[ip] = device_status[ip]
        # status_with_classes[ip]["classes"] = mock_classes.get(location, [])
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

@app.route('/add_device', methods=['POST'])
def add_device():
    ip = request.form.get('ip')
    location = request.form.get('location')
    if ip and location:
        sql_handler.insert_device(ip, port=80, location=location)
        device_status[ip] = {'status': 'Unknown', 'location': location}
    #     ESP_DEVICES.append({"ip": ip, "location": location})
    #     device_status[ip] = {"status": "Unknown", "location": location}
    return redirect(url_for('index'))

@app.route('/remove_device/<ip>', methods=['POST'])
def remove_device(ip):
    # global ESP_DEVICES
    # ESP_DEVICES = [device for device in ESP_DEVICES if device["ip"] != ip]
    device_status.pop(ip, None)
    return redirect(url_for('index'))

@app.route('/update_class', methods=['POST'])
def update_class():
    # location = request.form.get('location')
    # course_code = request.form.get('course_code')
    # start_time_str = request.form.get('start_time')
    # end_hour = request.form.get('end_hour')
    # end_minute = request.form.get('end_minute')
    
    # if location and course_code and start_time_str and end_hour and end_minute:
    #     start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    #     end_time = start_time + timedelta(hours=int(end_hour), minutes=int(end_minute))
    #     new_end_time = end_time.strftime("%Y-%m-%d %H:%M")
        
    #     # Update the mock class data
    #     for cls in mock_classes.get(location, []):
    #         if cls['course_code'] == course_code:
    #             cls['start_time'] = start_time_str
    #             cls['end_time'] = new_end_time
    #             break
    
    return redirect(url_for('index'))

@app.route('/move_class', methods=['POST'])
def move_class():
    # old_location = request.form.get('old_location')
    # new_location = request.form.get('new_location')
    # course_code = request.form.get('course_code')
    
    # if old_location and new_location and course_code:
    #     # Find the class in the old location and move it to the new location
    #     for cls in mock_classes.get(old_location, []):
    #         if cls['course_code'] == course_code:
    #             moved_class = cls
    #             mock_classes[old_location].remove(cls)
    #             if new_location not in mock_classes:
    #                 mock_classes[new_location] = []
    #             mock_classes[new_location].append(moved_class)
    #             break

    return redirect(url_for('index'))
