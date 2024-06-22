from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from datetime import datetime, timedelta
from .app import app
from .sql_handler import SQLHandler

@app.route('/')
def index():
    locations = list(mock_classes.keys())
    course_codes = {course['course_code'] for classes in mock_classes.values() for course in classes}
    return render_template('index.html', locations=locations, course_codes=course_codes)

@app.route('/status')
def status():
    status_with_classes = {}
    for device in ESP_DEVICES:
        ip = device["ip"]
        location = device["location"]
        status_with_classes[ip] = device_status[ip]
        status_with_classes[ip]["classes"] = mock_classes.get(location, [])
    return jsonify(status_with_classes)

@app.route('/start/<ip>')
def start(ip):
    success = start_stream(ip)
    if success:
        device_status[ip]["status"] = "Stream Started"
    else:
        device_status[ip]["status"] = "Failed to Start Stream"
    return redirect(url_for('index'))

@app.route('/stop/<ip>')
def stop(ip):
    success = stop_stream(ip)
    if success:
        device_status[ip]["status"] = "Stream Stopped"
    else:
        device_status[ip]["status"] = "Failed to Stop Stream"
    return redirect(url_for('index'))

@app.route('/start_all')
def start_all():
    for device in ESP_DEVICES:
        start_stream(device["ip"])
    return redirect(url_for('index'))

@app.route('/stop_all')
def stop_all():
    for device in ESP_DEVICES:
        stop_stream(device["ip"])
    return redirect(url_for('index'))

@app.route('/add_device', methods=['POST'])
def add_device():
    ip = request.form.get('ip')
    location = request.form.get('location')
    if ip and location:
        ESP_DEVICES.append({"ip": ip, "location": location})
        device_status[ip] = {"status": "Unknown", "location": location}
    return redirect(url_for('index'))

@app.route('/remove_device/<ip>', methods=['POST'])
def remove_device(ip):
    global ESP_DEVICES
    ESP_DEVICES = [device for device in ESP_DEVICES if device["ip"] != ip]
    device_status.pop(ip, None)
    return redirect(url_for('index'))

@app.route('/update_class', methods=['POST'])
def update_class():
    location = request.form.get('location')
    course_code = request.form.get('course_code')
    start_time_str = request.form.get('start_time')
    end_hour = request.form.get('end_hour')
    end_minute = request.form.get('end_minute')
    
    if location and course_code and start_time_str and end_hour and end_minute:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=int(end_hour), minutes=int(end_minute))
        new_end_time = end_time.strftime("%Y-%m-%d %H:%M")
        
        # Update the mock class data
        for cls in mock_classes.get(location, []):
            if cls['course_code'] == course_code:
                cls['start_time'] = start_time_str
                cls['end_time'] = new_end_time
                break
    
    return redirect(url_for('index'))

@app.route('/move_class', methods=['POST'])
def move_class():
    old_location = request.form.get('old_location')
    new_location = request.form.get('new_location')
    course_code = request.form.get('course_code')
    
    if old_location and new_location and course_code:
        # Find the class in the old location and move it to the new location
        for cls in mock_classes.get(old_location, []):
            if cls['course_code'] == course_code:
                moved_class = cls
                mock_classes[old_location].remove(cls)
                if new_location not in mock_classes:
                    mock_classes[new_location] = []
                mock_classes[new_location].append(moved_class)
                break

    return redirect(url_for('index'))
