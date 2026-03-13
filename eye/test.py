import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance
from datetime import datetime

print("Eye Blink Detection Started")

# ---------------- CONFIG ----------------
EAR_THRESHOLD = 0.21
CONSEC_FRAMES = 3
LOG_FILE = "blink_log.txt"
# ----------------------------------------

blink_counter = 0
frame_counter = 0

# ---------------- LOG FUNCTION ----------------
def write_log(message):
    time_now = datetime.now().strftime("%H:%M:%S")
    log_text = f"[LOG] {time_now} : {message}"
    print(log_text)

    with open(LOG_FILE, "a") as f:
        f.write(log_text + "\n")


# ---------------- EAR FUNCTION ----------------
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear


# ---------------- MEDIAPIPE SETUP ----------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indexes (MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera access failed")
    exit()

# ---------------- MAIN LOOP ----------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        mesh_points = np.array(
            [(int(p.x * w), int(p.y * h))
             for p in results.multi_face_landmarks[0].landmark]
        )

        left_eye = mesh_points[LEFT_EYE]
        right_eye = mesh_points[RIGHT_EYE]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        ear = (left_ear + right_ear) / 2.0

        # Draw eye landmarks
        for point in left_eye:
            cv2.circle(frame, point, 2, (0,255,0), -1)

        for point in right_eye:
            cv2.circle(frame, point, 2, (0,255,0), -1)

        # Blink detection
        if ear < EAR_THRESHOLD:
            frame_counter += 1
        else:
            if frame_counter >= CONSEC_FRAMES:
                blink_counter += 1
                write_log("Blink Detected")

            frame_counter = 0

        # Display
        cv2.putText(frame, f"EAR: {ear:.2f}", (30,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"Blinks: {blink_counter}", (30,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Blink Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()