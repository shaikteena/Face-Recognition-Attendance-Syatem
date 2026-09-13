import os
from datetime import datetime

import cv2
import face_recognition
import numpy as np
import pandas as pd

KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "Attendance.csv"
CAMERA_INDEX = 0
TOLERANCE = 0.5


def load_known_faces():
    encodings, names = [], []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

    for filename in sorted(os.listdir(KNOWN_FACES_DIR)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) == 1:
            encodings.append(face_encodings[0])
            names.append(os.path.splitext(filename)[0])
            print(f"Loaded: {names[-1]}")
        elif len(face_encodings) == 0:
            print(f"Skipped {filename}: no face found.")
        else:
            print(f"Skipped {filename}: multiple faces found.")

    return encodings, names


def ensure_attendance_file():
    if not os.path.exists(ATTENDANCE_FILE):
        pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(
            ATTENDANCE_FILE, index=False
        )


def mark_attendance(name):
    ensure_attendance_file()
    df = pd.read_csv(ATTENDANCE_FILE)
    today = datetime.now().strftime("%Y-%m-%d")

    if ((df["Name"] == name) & (df["Date"] == today)).any():
        return False

    now = datetime.now()
    record = pd.DataFrame([{
        "Name": name,
        "Date": today,
        "Time": now.strftime("%H:%M:%S")
    }])
    pd.concat([df, record], ignore_index=True).to_csv(
        ATTENDANCE_FILE, index=False
    )
    print(f"Attendance marked: {name}")
    return True


def main():
    known_encodings, known_names = load_known_faces()

    if not known_encodings:
        print("\nNo valid student photos found in known_faces/.")
        print("Add one clear photo per student and run again.")
        return

    ensure_attendance_file()

    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("Could not open webcam.")
        return

    print("\nCamera started. Press Q to quit.")

    while True:
        success, frame = camera.read()
        if not success:
            print("Could not read from webcam.")
            break

        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding, location in zip(encodings, locations):
            name = "Unknown"

            distances = face_recognition.face_distance(
                known_encodings, encoding
            )
            best_index = int(np.argmin(distances))

            if distances[best_index] <= TOLERANCE:
                name = known_names[best_index]
                mark_attendance(name)

            top, right, bottom, left = [v * 4 for v in location]

            cv2.rectangle(
                frame, (left, top), (right, bottom), (0, 255, 0), 2
            )
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom),
                (0, 255, 0), cv2.FILLED
            )
            cv2.putText(
                frame, name, (left + 6, bottom - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2
            )

        cv2.imshow("Face Recognition Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
