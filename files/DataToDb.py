from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rtu-attendance-31d29-default-rtdb.firebaseio.com/',
    'storageBucket': 'rtu-attendance-31d29.firebasestorage.app'
})

ref = db.reference('students')
bucket = storage.bucket()

with open('EncodedFile.p', 'rb') as file:
    encodeListKnown, studentIDs = pickle.load(file)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

modeType = 0
counter = 0
student_info_cache = {}
imgStudent = []

# Load your 4 mode icons
mode_icons = [f"static/files/icons/{i}.png" for i in range(1, 5)]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mode_data')
def mode_data():
    global student_info_cache, modeType
    return jsonify({
        'mode': modeType,
        'student': student_info_cache,
        'icon': mode_icons[modeType]
    })


def generate_frames():
    global counter, modeType, student_info_cache, imgStudent

    while True:
        success, img = cap.read()
        if not success:
            continue

        imgSmall = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgRGB = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(imgRGB)
        encode_current_frame = face_recognition.face_encodings(imgRGB, face_locations)

        if face_locations:
            for encodeFace, faceLoc in zip(encode_current_frame, face_locations):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                face_distance = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(face_distance)

                if matches[matchIndex]:
                    id = studentIDs[matchIndex]
                    if counter == 0:
                        modeType = 1
                        studentInfo = db.reference(f'students/{id}').get()
                        blob = bucket.get_blob(f'images/{id}.png')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                        datetimeObject = datetime.strptime(studentInfo['recent_attendance_time'], "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                        if secondsElapsed > 20:
                            studentInfo['total attendance'] = int(studentInfo['total attendance']) + 1
                            ref.child('total attendance').set(studentInfo['total attendance'])
                            ref.child('recent_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            modeType = 2
                        else:
                            modeType = 3

                        student_info_cache = studentInfo
                        counter = 1

        if counter != 0:
            counter += 1
            if counter >= 15:
                counter = 0
                modeType = 0
                student_info_cache = {}

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    app.run(debug=True)
