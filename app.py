from flask import Flask, render_template, jsonify
import threading
import cv2
import dlib
from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils

app = Flask(__name__)

# Initialize mixer for sound alert
mixer.init()
mixer.music.load("music.wav")

# Global variables
is_running = False
detection_thread = None

# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Drowsiness detection parameters
thresh = 0.25
frame_check = 20
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\\techexpo\\shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# Detection function
def run_detection():
    global is_running
    cap = cv2.VideoCapture(0)
    flag = 0

    while is_running:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detector(gray, 0)  # Use the correct 'detector' from dlib

        for subject in subjects:
            shape = predictor(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            if ear < thresh:
                flag += 1
                if flag >= frame_check:
                    if not mixer.music.get_busy():
                        mixer.music.play()
            else:
                flag = 0
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Flask route to start detection
@app.route('/start_detection', methods=['GET'])
def start_detection():
    global is_running, detection_thread
    if not is_running:
        is_running = True
        detection_thread = threading.Thread(target=run_detection)
        detection_thread.start()
    return jsonify({'status': 'Drowsiness detection started'})

# Flask route to stop detection
@app.route('/stop_detection', methods=['GET'])
def stop_detection():
    global is_running, detection_thread
    is_running = False
    if detection_thread is not None:
        detection_thread.join()
    return jsonify({'status': 'Drowsiness detection stopped'})

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
