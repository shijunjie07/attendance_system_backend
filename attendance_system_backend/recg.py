# ---------------------------------------------------
# facial recognition
# @author: Shi Junjie A178915
# Tue 11 June 2024
# ---------------------------------------------------

import io
import cv2
import json
import time
import warnings
import numpy as np
from PIL import Image
from datetime import datetime
from facial_fas_recognition.face_recg import FaceRecg

from embd import embeddings

# ignore warnings
warnings.filterwarnings('ignore')

# init facial recognition
face_recg = FaceRecg(embeddings)
attendance_recorded = []

def _binary_to_np_image(binary_data) -> Image:
    return np.array(Image.open(io.BytesIO(binary_data)))

async def process_image(image):
    start_time = time.time()
    
    image = _binary_to_np_image(image)
    image = cv2.rotate(image, cv2.ROTATE_180)
    print("image shape: ", image.shape)
    is_not_empty, recg_data = face_recg.recg(image)
    processed_data =  json.dumps( 
        {
            'id': ['invalid'],
            'live': ['False'],
            'recorded': ['False'],
        }
    )
    
    if is_not_empty:
        face_ids = recg_data['face_ids']
        
        is_recorded_array = np.isin(face_ids, attendance_recorded)
        
        # recorded attendance
        for i, is_recorded in enumerate(is_recorded_array):
            if not is_recorded and face_ids[i] != 'Undetected':
                attendance_recorded.append(face_ids[i])

        # update processed_data
        processed_data = json.dumps(
            {
                'id': recg_data["face_ids"],
                'live': [str(live[0, 0].item()) for live in recg_data['livenesses']],
                'recorded': list(map(str, is_recorded_array)),
            }
        )

    end_time = time.time()
    process_time = end_time - start_time
    print('[{}] Process Time: {:.2f} seconds'.format(datetime.now().strftime("%M:%S.%f"), process_time))

    return image, processed_data, recg_data
