Blink Detection Logic Documentation
1. Overview

The blink detection system identifies whether a user blinks their eyes in a live video stream captured through a webcam. The detection is performed using facial landmarks extracted by MediaPipe FaceMesh and the Eye Aspect Ratio (EAR) method.

Blink detection is used as a liveness verification technique to ensure that the detected face belongs to a real person and not a static image.

2. Input

The system takes the following inputs:

Live video frames captured from the webcam using OpenCV.

Facial landmark coordinates detected using MediaPipe FaceMesh.

Each frame contains 468 facial landmarks, from which specific landmarks corresponding to the eyes are extracted.

3. Eye Landmark Extraction

From the 468 facial landmarks detected by MediaPipe, six key points are selected for each eye.

Left Eye Landmarks
[33, 160, 158, 133, 153, 144]
Right Eye Landmarks
[362, 385, 387, 263, 373, 380]

These landmarks represent:

Landmark	Description
p1	Left eye corner
p2	Upper eyelid
p3	Upper eyelid
p4	Right eye corner
p5	Lower eyelid
p6	Lower eyelid

These six points define the geometric shape of the eye.

4. Eye Aspect Ratio (EAR)

The system calculates the Eye Aspect Ratio (EAR) to measure whether the eye is open or closed.

The EAR is calculated using the distances between vertical and horizontal eye landmarks.

EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2||p_1 - p_4||}

Where:

𝑝
1
p
1
	​

 and 
𝑝
4
p
4
	​

 represent horizontal eye corners.

𝑝
2
,
𝑝
3
p
2
	​

,p
3
	​

 represent upper eyelid points.

𝑝
5
,
𝑝
6
p
5
	​

,p
6
	​

 represent lower eyelid points.

The Euclidean distance between these points is used for calculation.

5. Blink Detection Threshold

A threshold value is used to determine whether the eye is closed.

EAR_THRESHOLD = 0.21

Interpretation:

EAR Value	Eye State
EAR > 0.21	Eye open
EAR ≤ 0.21	Eye closed

When the EAR value drops below the threshold, the system assumes that the eye is closed.

6. Consecutive Frame Verification

To avoid false blink detection caused by noise or temporary eye movement, the system checks whether the eye remains closed for a certain number of consecutive frames.

CONSEC_FRAMES = 3

This means the EAR must remain below the threshold for at least three continuous frames before considering it a blink.

7. Detection Algorithm
Step 1

Capture a video frame from the webcam.

Step 2

Detect face landmarks using MediaPipe FaceMesh.

Step 3

Extract eye landmarks for both eyes.

Step 4

Calculate the EAR value for the left and right eye.

Step 5

Compute the average EAR value.

Step 6

Check if the EAR value is below the threshold.

Step 7

Increase the frame counter if the eye remains closed.

Step 8

If the number of closed-eye frames exceeds the consecutive frame limit, a blink is detected.

Step 9

Increment the blink counter and record the timestamp.

8. Blink Detection Logic (Pseudo Code)
Start camera

Loop:
    Capture frame

    Detect face landmarks

    Extract eye landmarks

    Calculate EAR

    IF EAR < threshold:
        frame_counter += 1

    ELSE:
        IF frame_counter >= 3:
            blink_counter += 1
            print "Blink detected"

        frame_counter = 0
9. Output

The system outputs:

Blink detection events

Total blink count

Real-time EAR value

Example console output:

Blink Detected at 14:21:35
Blink Detected at 14:21:42
10. Advantages of EAR-Based Detection

Works in real time

Lightweight computation

Accurate for liveness detection

Independent of lighting conditions compared to some other methods

11. Limitations

May fail if:

The user wears glasses

The face is partially occluded

The head is rotated excessively

Threshold values may require tuning for different users or camera
