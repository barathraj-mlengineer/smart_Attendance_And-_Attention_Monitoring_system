import cv2

def is_attentive(frame, face_loc):
    top, right, bottom, left = face_loc
    face_img = frame[top:bottom, left:right]
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    eyes = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    detected_eyes = eyes.detectMultiScale(gray)
    return "Yes" if len(detected_eyes) >= 1 else "No"