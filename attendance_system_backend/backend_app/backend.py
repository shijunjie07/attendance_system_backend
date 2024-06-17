# ---------------------------------
# app routes
# @author: Shi Junjie A178915
# Sat 9 June 2024
# ---------------------------------

import time
import requests
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
from models import Course, Class, Attendance, Lecturer, Student, course_student, course_lecturer


# Initial list of ESP devices with their IPs and locations
ESP_DEVICES = [
    {"ip": "192.168.0.105", "location": "FKAB DK1"},
    {"ip": "192.168.0.106", "location": "FKAB ASTMK1"},
    {"ip": "192.168.0.107", "location": "FKAB BS6"}
]
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


mock_classes = {}

device_status = {device["ip"]: {"status": "Unknown", "location": device["location"]} for device in ESP_DEVICES}

def check_device_status():
    while True:
        for device in ESP_DEVICES:
            esp_ip = device["ip"]
            url = f'http://{esp_ip}:{ESP_PORT}/status'
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    device_status[esp_ip]["status"] = "Connected"
                else:
                    device_status[esp_ip]["status"] = "Disconnected"
            except requests.RequestException as e:
                print(f"Error checking status on {esp_ip}: {e}")
                device_status[esp_ip]["status"] = "Disconnected"
        time.sleep(CHECK_INTERVAL)

def start_stream(esp_ip):
    url = f'http://{esp_ip}:{ESP_PORT}/start_stream'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"Error starting stream on {esp_ip}: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error starting stream on {esp_ip}: {e}")
        return False

def stop_stream(esp_ip):
    url = f'http://{esp_ip}:{ESP_PORT}/stop_stream'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"Error stopping stream on {esp_ip}: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error stopping stream on {esp_ip}: {e}")
        return False

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


if __name__ == '__main__':
    status_check_thread = threading.Thread(target=check_device_status, daemon=True)
    status_check_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)
