# ---------------------------------------------------
# facial recognition
# @author: Shi Junjie A178915
# Tue 11 June 2024
# ---------------------------------------------------

import os
import cv2
import warnings

from facial_fas_recognition.face_recg import FaceRecg
from facial_fas_recognition.detector import FaceDetector
from facial_fas_recognition.recognizer import Recognizer
from PIL import Image
# ignore warnings
warnings.filterwarnings('ignore')

# init facial recg
face_detector = FaceDetector()
encode = Recognizer().encode

# generate embeddings for testing
def _gen_embeddings():
    print("generating embeddings", end='')
    saved_pictures = "known_faces/"     # face image folder
    all_people_faces = {}

    files = os.listdir(saved_pictures)
    for file in files:
        print(".", end='')
        face_id, _ = file.split(".")
        # print(face_id)
        img = cv2.imread('{}{}'.format(saved_pictures, file))
        _, cropped = face_detector.detect_faces(img)
        if cropped is not None:
            cropped = Image.fromarray(cropped[0])
            # cropped = cropped[0].transpose(2, 0, 1)
            
            all_people_faces[face_id] = encode(cropped)[0, :]
    print()
    return all_people_faces

embeddings = _gen_embeddings()