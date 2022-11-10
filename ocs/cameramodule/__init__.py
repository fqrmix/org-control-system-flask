import os
import cv2
import pickle
import face_recognition
from imutils import paths
from .camera import Camera


main_camera = Camera()

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
        # используем библиотеку Face_recognition для обнаружения лиц
        boxes = face_recognition.face_locations(rgb, model='hog')
        # вычисляем эмбеддинги для каждого лица
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownIds.append(id)
    # сохраним эмбеддинги вместе с их ID в формате словаря
    data = {
        "encodings": knownEncodings, 
        "ids": knownIds
    }
    if existedData is not None:
        unitedData = {**data, **existedData}
        data = unitedData
    # для сохранения данных в файл используем метод pickle
    with open(path, "wb") as f:
        f.write(pickle.dumps(data))

def read_encodings(path: str):
    return pickle.loads(open(path, "rb").read())

path = ROOT_DIR + '/face_enc'
create_encodings(path=path, start=1)
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
