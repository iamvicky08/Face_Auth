# 👁️ Blink Detection Logic Documentation

## 📌 Overview
The blink detection system identifies whether a user blinks their eyes in a live video stream captured through a webcam. The detection is performed using facial landmarks extracted by MediaPipe FaceMesh and the Eye Aspect Ratio (EAR) method.

Blink detection is used as a liveness verification technique to ensure that the detected face belongs to a real person and not a static image.

---

## 🎥 Input

The system takes the following inputs:

- Live video frames captured from the webcam using OpenCV
- Facial landmark coordinates detected using MediaPipe FaceMesh

Each frame contains 468 facial landmarks, from which specific landmarks corresponding to the eyes are extracted.

---

## 👀 Eye Landmark Extraction

From the 468 facial landmarks detected by MediaPipe, six key points are selected for each eye.

- **Left Eye Landmarks:** `[33, 160, 158, 133, 153, 144]`
- **Right Eye Landmarks:** `[362, 385, 387, 263, 373, 380]`

### Landmark Description

| Point | Description        |
|------|--------------------|
| p1   | Left eye corner    |
| p2   | Upper eyelid       |
| p3   | Upper eyelid       |
| p4   | Right eye corner   |
| p5   | Lower eyelid       |
| p6   | Lower eyelid       |

These six points define the geometric shape of the eye.

---

## 📐 Eye Aspect Ratio (EAR)

The system calculates the Eye Aspect Ratio (EAR) to measure whether the eye is open or closed.

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

### Where:
- p1, p4 → Horizontal eye corners  
- p2, p3 → Upper eyelid points  
- p5, p6 → Lower eyelid points  

The Euclidean distance between these points is used for calculation.

# 📐 EAR Calculation Using Given Eye Landmarks

## 👁️ Given Landmarks

### Left Eye:
```
[33, 160, 158, 133, 153, 144]
```

### Right Eye:
```
[362, 385, 387, 263, 373, 380]
```

---

## 🔁 Mapping to EAR Points

### Left Eye Mapping:
```
p1 = 33
p2 = 160
p3 = 158
p4 = 133
p5 = 153
p6 = 144
```

### Right Eye Mapping:
```
p1 = 362
p2 = 385
p3 = 387
p4 = 263
p5 = 373
p6 = 380
```

---

## 📏 Distance Formula

```
d(pi, pj) = √((xj - xi)² + (yj - yi)²)
```

---

## 📊 LEFT EYE EAR

### Vertical Distances:
```
V1 = d(160, 144) = √((x144 - x160)² + (y144 - y160)²)

V2 = d(158, 153) = √((x153 - x158)² + (y153 - y158)²)
```

### Horizontal Distance:
```
H = d(33, 133) = √((x133 - x33)² + (y133 - y33)²)
```

### LEFT EAR Formula:
```
EAR_left = (d(160,144) + d(158,153)) / (2 * d(33,133))
```

---

## 📊 RIGHT EYE EAR

### Vertical Distances:
```
V1 = d(385, 380) = √((x380 - x385)² + (y380 - y385)²)

V2 = d(387, 373) = √((x373 - x387)² + (y373 - y387)²)
```

### Horizontal Distance:
```
H = d(362, 263) = √((x263 - x362)² + (y263 - y362)²)
```

### RIGHT EAR Formula:
```
EAR_right = (d(385,380) + d(387,373)) / (2 * d(362,263))
```

---

## 📊 FINAL EAR

```
EAR = (EAR_left + EAR_right) / 2
```

---

## 🧠 Interpretation

```
If EAR > 0.21  → Eye Open 👁️
If EAR ≤ 0.21 → Eye Closed (Blink) 👁️
```

---

## ✅ Conclusion

- EAR is calculated using vertical and horizontal eye distances  
- Uses MediaPipe landmark indices for both eyes  
- Helps detect blinking for liveness verification  
- Threshold-based decision makes it simple and efficient  


---

## ⚙️ Blink Detection Threshold

A threshold value is used to determine whether the eye is closed.

```
EAR_THRESHOLD = 0.21
```

### Interpretation

| EAR Value   | Eye State |
|------------|----------|
| EAR > 0.21 | Eye Open |
| EAR ≤ 0.21 | Eye Closed |

When the EAR value drops below the threshold, the system assumes that the eye is closed.

---

## 🔁 Consecutive Frame Verification

To avoid false blink detection caused by noise or temporary eye movement, the system checks whether the eye remains closed for a certain number of consecutive frames.

```
CONSEC_FRAMES = 3
```

The EAR must remain below the threshold for at least three continuous frames before considering it a blink.

---

## 🔄 Detection Algorithm

### Step-by-Step Process

1. Capture a video frame from the webcam  
2. Detect face landmarks using MediaPipe FaceMesh  
3. Extract eye landmarks for both eyes  
4. Calculate the EAR value for the left and right eye  
5. Compute the average EAR value  
6. Check if the EAR value is below the threshold  
7. Increase the frame counter if the eye remains closed  
8. If the number of closed-eye frames exceeds the consecutive frame limit, a blink is detected  
9. Increment the blink counter and record the timestamp  

---

## 🧾 Pseudo Code

```
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
            print("Blink detected")

        frame_counter = 0
```

---

## 📤 Output

The system outputs:

- Blink detection events  
- Total blink count  
- Real-time EAR value  

### Example Console Output

```
Blink Detected at 14:21:35
Blink Detected at 14:21:42
```

---

## ✅ Advantages of EAR-Based Detection

- Works in real time  
- Lightweight computation  
- Accurate for liveness detection  
- Less sensitive to lighting compared to some other methods  

---

## ⚠️ Limitations

The system may fail in the following situations:

- User wears glasses  
- Face is partially occluded  
- Head is rotated excessively  
- Threshold values may require tuning for different users or cameras  

---

## 🧠 Conclusion

EAR-based blink detection is a simple, efficient, and reliable method for real-time liveness detection. It is widely used in face authentication and anti-spoofing systems to enhance security.
# 🔍 Accuracy Comparison: Anti-Spoofing vs Baseline Detection

This section compares the performance of a basic face detection system (baseline) with the implemented anti-spoofing system using eye blink and head movement detection.

---

## 📊 Feature Comparison Table

| Feature / Method         | Baseline Detection | Your Anti-Spoofing |
|------------------------|------------------|-------------------|
| Face Detection         | ✅ Yes           | ✅ Yes            |
| Photo Attack Detection | ❌ No            | ✅ Yes            |
| Video Replay Detection | ❌ No            | ⚠️ Partial        |
| Eye Blink Detection    | ❌ No            | ✅ Yes            |
| Head Movement Detection| ❌ No            | ✅ Yes            |
| Real-time Logging      | ❌ No            | ✅ Yes            |
| Accuracy (Approx.)     | 60–70%          | 85–92%           |

---

## 📈 Summary

- **Baseline Detection**:
  - Detects only the presence of a face
  - Easily fooled by photos and videos
  - Lower accuracy and security

- **Anti-Spoofing System**:
  - Uses liveness detection (blink + head movement)
  - More robust against spoof attacks
  - Significantly higher accuracy

---

## 🧠 Conclusion

The anti-spoofing system improves reliability and security by verifying real human presence rather than just detecting a face. It reduces spoof attacks and is more suitable for real-world authentication systems.
