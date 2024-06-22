# ---------------------------------------------------
# websockets to receive image and send message
# @author: Shi Junjie A178915
# Mon 10 June 2024
# ---------------------------------------------------

import os
import json
import asyncio
import websockets
import cv2
import warnings
import time

from .recg import process_image
from backend_app.app import db

warnings.filterwarnings('ignore')


async def receive_message(websocket, message_queue):
    async for message in websocket:
        # print('received message')
        await message_queue.put(message)

async def send_message(websocket, message_queue, image_queue):
    receive_last_frame_time = 0.0
    process_last_frame_time = 0.0
    
    while True:
        message = await message_queue.get()
        
        # calculate receive time interval
        receive_time = time.time()
        receive_diff_time = receive_time - receive_last_frame_time
        receive_last_frame_time = receive_time
        if receive_diff_time == 0:
            receive_fps = '-1'
        else:
            receive_fps = round(1 / (receive_diff_time), 2)
        print('_______________')
        print('receive fps: {}'.format(receive_fps))
        
        image, processed_message, data = await process_image(message)
        processed_message_dict = json.loads(processed_message)
        image_info = [image, processed_message, data]
        await image_queue.put(image_info)
        print(processed_message)
        print("----")
        print()
        await websocket.send(processed_message)
        message_queue.task_done()

        # calculate receive time interval
        process_time = time.time()
        process_diff_time = process_time - process_last_frame_time
        process_last_frame_time = process_time
        if process_diff_time == 0:
            process_fps = '-1'
        else:
            process_fps = round(1 / (process_diff_time), 2)
        print('total process fps: {}'.format(process_fps))

async def show_stream(image_queue):
    stream_image_dir = "/home/junja/attendance_system_backend/stream"       # change to the dir where u want to place the processed image
    stream_idx = 0
    while True:
        img, msg, data = await image_queue.get()
        msg_dict = json.loads(msg)
        # cv2 visualise ---------------------------------------------------------
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # print(data)
        try:
            if msg_dict['id'][0] != "invalid":
                box_color = (0, 0, 225)
                if msg_dict['live'][0] == 'True':
                    box_color = (0, 255, 0)

                cv2.rectangle(
                    img, (data["bboxes"][0][0], data["bboxes"][0][1]),
                    (data["bboxes"][0][2], data["bboxes"][0][3]), box_color, 2,
                )
            
                cv2.putText(img, msg_dict['id'][0], (20, 20), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(
                    img, 'live: {} {:.3f}'.format(msg_dict['live'][0], data['liveness_scores'][0]), (20, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                
        except:
            cv2.putText(img, 'Exception', (20, 100), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

        img_file_name = 'stream_{}.jpg'.format(stream_idx)
        cv2.imwrite(os.path.join(
            stream_image_dir, img_file_name
            ), img)
        stream_idx += 1
        image_queue.task_done()
    
async def websocket_handler(websocket, path):
    
    message_queue = asyncio.Queue()
    image_queue = asyncio.Queue()

    receive_task = asyncio.create_task(receive_message(websocket, message_queue))
    send_task = asyncio.create_task(send_message(websocket, message_queue, image_queue))
    show_stream_task = asyncio.create_task(show_stream(image_queue))
    
    await asyncio.gather(
        receive_task,
        send_task,
        show_stream_task,
    )

async def start_socket_server(port):
    print('running websocket server on port: {}'.format(port))
    server = await websockets.serve(websocket_handler, '0.0.0.0', port)
    await server.wait_closed()
    
def run_socket_server(port):
    asyncio.run(start_socket_server(port))
    
# run_socket_server(3000)