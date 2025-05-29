import cv2
import os
import pandas as pd

def register_student(name):
    os.makedirs(f"data/faces/{name}", exist_ok=True)
    cap = cv2.VideoCapture(0)
    count = 0

    while count < 5:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(f"Registering {name} - Press 's' to save", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(f"data/faces/{name}/{count}.jpg", frame)
            count += 1
            print(f"Saved image {count} for {name}")
        elif key == ord('q'):
            print("Registration cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Registration Complete for {name}.\n")

# Load student names from Excel file
try:
    df = pd.read_excel("students.xlsx")
    if 'name' not in df.columns:
        raise KeyError("Excel file must have a column named 'name'.")

    names = df['name'].dropna().astype(str).tolist()

    for name in names:
        input(f"Prepare {name} and press Enter to start registration...")
        register_student(name)

except Exception as e:
    print(f"Error: {e}")
