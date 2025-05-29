import face_recognition
import os

def load_known_faces(base_path='data/faces'):
    encodings = []
    names = []
    for name in os.listdir(base_path):
        for img_file in os.listdir(f"{base_path}/{name}"):
            path = os.path.join(base_path, name, img_file)
            img = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                encodings.append(encoding[0])
                names.append(name)
    return encodings, names