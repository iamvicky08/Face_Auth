import cv2
import mediapipe as mp
import numpy as np
import time

print("Anti-Spoofing Baseline Test Started")

EAR_THRESHOLD = 0.21
CONSEC_FRAMES = 3
HEAD_MOVE_THRESHOLD = 15
TEST_DURATION = 10

blink_detected = False
head_moved = False

blink_counter = 0
frame_counter = 0
prev_nose_x = None

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]
NOSE_TIP = 1


def euclidean(p1,p2):
    return np.linalg.norm(np.array(p1)-np.array(p2))


def calculate_EAR(eye):

    p1,p2,p3,p4,p5,p6 = eye

    vertical1 = euclidean(p2,p6)
    vertical2 = euclidean(p3,p5)
    horizontal = euclidean(p1,p4)

    return (vertical1+vertical2)/(2*horizontal)


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

print("Camera started")

start_time = time.time()

log_file = open("spoof_test_log.txt","a")

while True:

    ret,frame = cap.read()

    if not ret:
        print("Frame not captured")
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        mesh_points = results.multi_face_landmarks[0].landmark
        h,w = frame.shape[:2]

        left_eye=[]
        right_eye=[]

        for idx in LEFT_EYE:
            x=int(mesh_points[idx].x*w)
            y=int(mesh_points[idx].y*h)
            left_eye.append((x,y))

        for idx in RIGHT_EYE:
            x=int(mesh_points[idx].x*w)
            y=int(mesh_points[idx].y*h)
            right_eye.append((x,y))


        leftEAR=calculate_EAR(left_eye)
        rightEAR=calculate_EAR(right_eye)

        EAR=(leftEAR+rightEAR)/2


        if EAR < EAR_THRESHOLD:

            frame_counter+=1

        else:

            if frame_counter>=CONSEC_FRAMES:

                blink_counter+=1
                blink_detected=True

                timestamp=time.strftime("%H:%M:%S")

                log=f"[LOG] {timestamp} : Blink Detected"
                print(log)
                log_file.write(log+"\n")

            frame_counter=0


        nose=mesh_points[NOSE_TIP]

        nose_x=int(nose.x*w)

        if prev_nose_x is not None:

            movement=nose_x-prev_nose_x

            if abs(movement)>HEAD_MOVE_THRESHOLD:

                head_moved=True
                timestamp=time.strftime("%H:%M:%S")

                direction="RIGHT" if movement>0 else "LEFT"

                log=f"[LOG] {timestamp} : Head Moved {direction}"

                print(log)
                log_file.write(log+"\n")

        prev_nose_x=nose_x


        cv2.putText(frame,f"EAR:{EAR:.2f}",(30,40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


    cv2.imshow("Anti-Spoof Test",frame)


    # timer check AFTER window display
    if time.time()-start_time > TEST_DURATION:
        print("Test duration finished")
        break


    if cv2.waitKey(1)==27:
        break


cap.release()
cv2.destroyAllWindows()


timestamp=time.strftime("%H:%M:%S")

if blink_detected and head_moved:
    result="REAL USER (LIVENESS PASSED)"
else:
    result="SPOOF DETECTED"


print("\n=== TEST RESULT ===")
print(result)

log_file.write(f"[RESULT] {timestamp} : {result}\n\n")

log_file.close()