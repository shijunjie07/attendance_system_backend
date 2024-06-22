import requests
import threading
import time

def start_stream(esp_ip, port):
    url = f'http://{esp_ip}:{port}/start_stream'
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

def stop_stream(esp_ip, port):
    url = f'http://{esp_ip}:{port}/stop_stream'
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
    
def check_device_status(device_status, ESP_DEVICES, CHECK_INTERVAL):
    while True:
        for device in ESP_DEVICES:
            esp_ip = device.ip
            port = device.port
            url = f'http://{esp_ip}:{port}/status'
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

def start_status_check_thread(sql_handler, CHECK_INTERVAL=10):
    ESP_DEVICES = sql_handler.get_device(all=True)
    device_status = {
        device.ip: {"status": "Unknown", "location": device.location, 'port': device.port}
        for device in ESP_DEVICES}

    status_check_thread = threading.Thread(
        target=check_device_status, args=(device_status, ESP_DEVICES, CHECK_INTERVAL), daemon=True)
    status_check_thread.start()
