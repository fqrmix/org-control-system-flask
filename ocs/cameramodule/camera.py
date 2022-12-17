import face_recognition
import cv2
import numpy as np

class Camera:
    """
    Класс который позволяет подключится к определенной камере и
    распознать лица на видеопотоке. Видеопоток рендерится в .JPG картинках.
    """
    def __init__(self):
        self.current_id = 0

    def connect(self, known_face_encodings, known_face_ids, camera_id):
        """
        Метод подключения к камере.

            *args:
                :known_face_encodings:   Энкодинги известных программе лиц.
                :known_face_ids:         ID известных программе людей.
                :camera_id:              ID камеры, к которой будет происходить подключение.

            *return:            :yield (b'--frame\r\n'
                                    b'Content-Type: video/jpeg\r\n\r\n' + frame + b'\r\n')       
                                    frame - JPG изображения, в byte-формате. 
        """

        while True:
            video_capture = cv2.VideoCapture(camera_id)
            _, frame = video_capture.read()
            if frame is not None:
                break
            else:
                print('Frame is empty! Trying to connect...')

        # Инициализация изначальных параметров
        face_locations = []
        face_encodings = []
        face_ids = []
        whoIs = ''
        object_id = ''
        process_this_frame = True

        while True:
            # Захват одного кадра
            _, frame = video_capture.read()
            if frame is not None:
                if face_locations == []:
                    isOnCam = False
                    whoIs = ''
                else:
                    if face_ids == []:
                        pass
                    else:
                        whoIs = face_ids[0]
                        isOnCam = True
                
                # Обрабатываем только 1 кадр, для увеличения производительности.
                if process_this_frame:
                    # Для более быстрого распознования лиц поделим размер кадра на 4
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    cv2.putText(frame, str(isOnCam) + ' ' + whoIs, (100, 100), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                    rgb_small_frame = small_frame[:, :, ::-1]
                    
                    # Находим все лица на текущем кадре
                    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_ids = []
                    for face_encoding in face_encodings:
                        # Сравниваем найденные лица с известными
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        object_id = "Unknown"

                        # Считаем расстояние между найденным лицом и известным
                        face_distances = face_recognition.face_distance(
                                known_face_encodings, face_encoding
                        )
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            object_id = known_face_ids[best_match_index]
                        # Обрабатываем не только известные лица, для отображения в dashboard
                        face_ids.append(object_id)

                process_this_frame = not process_this_frame


                # Отображение результатов
                for (top, right, bottom, left), object_id in zip(face_locations, face_ids):
                    # Возврат исходного размера изображения
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Отрисовка квадратов вокруг лиц
                    cv2.rectangle(frame, 
                            (left, top), (right, bottom), 
                            (0, 0, 255), 2
                    )

                    # Отрисовка ID около квадрата
                    cv2.rectangle(frame, (left, bottom - 35), 
                                (right, bottom), (0, 0, 255), 
                                cv2.FILLED
                    )
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, object_id, 
                            (left + 6, bottom - 6), font, 1.0, 
                            (255, 255, 255), 1
                    )

                # Возвращаем полученное изображение
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: video/jpeg\r\n\r\n' + frame + b'\r\n')
            
                # Если на камере никого - присваиваем id 6
                if not isOnCam:
                    self.current_id = 6
                
                # Если на камере Unknown - присваиваем id 0
                elif isOnCam and object_id == 'Unknown' and len(face_ids) < 2:
                    self.current_id = 0

                # Если на камере не Unknown - присваиваем ID известного лица
                elif object_id != 'Unknown':
                    self.current_id = int(object_id)
