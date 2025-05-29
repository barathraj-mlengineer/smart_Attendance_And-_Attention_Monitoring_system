import cv2
import face_recognition
from datetime import datetime
from utils.face_utils import load_known_faces
from utils.attention import is_attentive
from utils.db import insert_attendance, insert_attention

print("Loading known faces...")
known_encodings, known_names = load_known_faces()
cap = cv2.VideoCapture(0)

print("Starting live camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, face_locs)

    for enc, loc in zip(encodings, face_locs):
        matches = face_recognition.compare_faces(known_encodings, enc)
        name = "Unknown"
        if True in matches:
            match_idx = matches.index(True)
            name = known_names[match_idx]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_attendance(name, timestamp)
            attentive = is_attentive(frame, loc)
            insert_attention(name, timestamp, attentive)
            cv2.putText(frame, f"{name} ({attentive})", (loc[3], loc[2]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        else:
            cv2.putText(frame, "Unknown", (loc[3], loc[2]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.rectangle(frame, (loc[3], loc[0]), (loc[1], loc[2]), (255, 0, 0), 2)

    cv2.imshow("Smart Classroom", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()