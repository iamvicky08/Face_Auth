import cv2
import mediapipe as mp
import numpy as np
import time

print("Blink Liveness Detection Started")

# -------- CONFIG --------
EAR_THRESHOLD = 0.21
CONSEC_FRAMES = 3
# ------------------------

blink_counter = 0
frame_counter = 0

# MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indexes
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def calculate_EAR(eye):

    p1, p2, p3, p4, p5, p6 = eye

    vertical1 = euclidean(p2, p6)
    vertical2 = euclidean(p3, p5)
    horizontal = euclidean(p1, p4)

    ear = (vertical1 + vertical2) / (2.0 * horizontal)

    return ear


# Start Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

print("Camera Started")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        mesh_points = results.multi_face_landmarks[0].landmark
        h, w = frame.shape[:2]

        left_eye = []
        right_eye = []

        for idx in LEFT_EYE:
            x = int(mesh_points[idx].x * w)
            y = int(mesh_points[idx].y * h)
            left_eye.append((x, y))
            cv2.circle(frame, (x, y), 2, (0,255,0), -1)

        for idx in RIGHT_EYE:
            x = int(mesh_points[idx].x * w)
            y = int(mesh_points[idx].y * h)
            right_eye.append((x, y))
            cv2.circle(frame, (x, y), 2, (0,255,0), -1)

        leftEAR = calculate_EAR(left_eye)
        rightEAR = calculate_EAR(right_eye)

        EAR = (leftEAR + rightEAR) / 2.0


        # Blink detection logic
        if EAR < EAR_THRESHOLD:

            frame_counter += 1

        else:

            if frame_counter >= CONSEC_FRAMES:

                blink_counter += 1
                timestamp = time.strftime("%H:%M:%S")

                print(f"Blink Detected at {timestamp}")

            frame_counter = 0


        # Display information
        cv2.putText(frame, f"EAR: {EAR:.2f}", (30,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(frame, f"Blinks: {blink_counter}", (30,80),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


    cv2.imshow("Blink Liveness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()