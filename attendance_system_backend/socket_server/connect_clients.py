# -------------------------------------------------------
# http to receive image and send message - mult clients
# @author: Shi Junjie A178915
# Sat 15 June 2024
# -------------------------------------------------------

import requests


ESP_IP = "192.168.0.105"        # change to your ESP ip address
ESP_PORT = 80
ESP_URL = "http://{}:{}".format(ESP_IP, ESP_PORT)

SERVER_PORT = 5000

def start_stream(camera_id=None, location=None):
    url = '{}/{}'.format(ESP_URL, 'start_stream')
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # asyncio.run(start_socket_server(SERVER_PORT))
            # print("")
            return True
        else:
            return False
    except requests.RequestException as e:
        return e

def stop_stream(camera_id=None, location=None):
    url = '{}/{}'.format(ESP_URL, 'stop_stream')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return e
        
if __name__ == "__main__":
    while True:
        input_start_str = input("type 'start' to start stream from esp32cam: ")
        if input_start_str.strip().lower() == 'start':
            start_stream()
        else:
            continue