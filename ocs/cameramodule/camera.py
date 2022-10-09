import pickle
from threading import Thread
import face_recognition
import cv2
import numpy as np
import os
from imutils import paths
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_encodings(path, start, existedData = None):
    # в директории Images хранятся папки со всеми изображениями
    imagePaths = list(paths.list_images(ROOT_DIR + '/photos'))
    print(imagePaths)
    knownEncodings = []
    knownIds = []
    # перебираем все папки с изображениями
    for (i, imagePath) in enumerate(imagePaths, start=start):
        # извлекаем ID человека из названия папки
        id = imagePath.split(os.path.sep)[-2]
        # загружаем изображение и конвертируем его из BGR (OpenCV ordering)
        # в dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #используем библиотеку Face_recognition для обнаружения лиц
        boxes = face_recognition.face_locations(rgb,model='hog')
        # вычисляем эмбеддинги для каждого лица
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownIds.append(id)
    # сохраним эмбеддинги вместе с их именами в формате словаря
    data = {"encodings": knownEncodings, "ids": knownIds}
    if existedData is not None:
        unitedData = {**data, **existedData}
        data = unitedData
    # для сохранения данных в файл используем метод pickle
    with open(path, "wb") as f:
        f.write(pickle.dumps(data))

def read_encodings(path: str):
    data = pickle.loads(open(path, "rb").read())
    return data

path = ROOT_DIR + '/face_enc'

create_encodings(
    path=path,
    start=1
)


data = read_encodings(path)
known_face_encodings_new = data['encodings']
known_face_ids = data['ids']

name_list = {
    0: "Unknown person",
    1: "Dima Golovin",
    2: "Roma Kulakov",
    3: "Semen Sergeev",
    4: "Nikita Vlasjuk",
    5: "Sasha Vorontsov",
    6: "No one"
}

class Camera:
    def __init__(self):
        self.current_id = 0

    def connect(self, known_face_encodings, known_face_ids, camera_id):
        video_capture = cv2.VideoCapture(camera_id)
        print('Started connect...')
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_ids = []
        whoIs = ''
        object_id = ''
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            if face_locations == []:
                isOnCam = False
                whoIs = ''
            else:
                if face_ids == []:
                    pass
                else:
                    whoIs = face_ids[0]
                    isOnCam = True
            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                cv2.putText(frame, str(isOnCam) + ' ' + whoIs, (100, 100), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_ids = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    object_id = "Unknown"
                    
                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     id = known_face_ids[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(
                            known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        object_id = known_face_ids[best_match_index]
                    face_ids.append(object_id) # Process not only known faces
                    # Unknown person will be processed too

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), object_id in zip(face_locations, face_ids):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), 
                        (0, 0, 255), 2
                        )

                # Draw a label with a id below the face
                cv2.rectangle(frame, (left, bottom - 35), 
                            (right, bottom), (0, 0, 255), 
                            cv2.FILLED
                            )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, object_id, 
                        (left + 6, bottom - 6), font, 1.0, 
                        (255, 255, 255), 1
                        )

            # Display the resulting image
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: video/jpeg\r\n\r\n' + frame + b'\r\n')
            if not isOnCam:
                self.current_id = 6
            elif isOnCam and object_id == 'Unknown' and len(face_ids) < 2:
                self.current_id = 0
            elif object_id != 'Unknown':
                # video_capture.release()
                # cv2.destroyAllWindows()
                self.current_id = int(object_id)
