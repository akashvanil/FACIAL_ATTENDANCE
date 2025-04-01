import os
import pickle
from datetime import datetime
import cv2
import face_recognition
import numpy as np
import cvzone
from cv2 import imdecode

from encode import encodeListKnown, encodeListKnownIDs, studentID
import firebase_admin
from firebase_admin import credentials, db, storage

# Check if Firebase has already been initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://rtu-attendance-31d29-default-rtdb.firebaseio.com/',
        'storageBucket': 'rtu-attendance-31d29.firebasestorage.app'
    })

bucket = storage.bucket()

# Open the webcam with error handling
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

if not cap.isOpened():
    print("Error: Could not open webcam. Check camera connection.")
    exit()

# Load the background image
imgBackground = cv2.imread('files/bg.png')
if imgBackground is None:
    print("Error: Background image not found. Check the file path!")
    exit()

# Load icons
folderModePath = 'files/icons'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList if cv2.imread(os.path.join(folderModePath, path)) is not None]

if not imgModeList:
    print("Error: No icons loaded. Check the 'files/icons' folder.")

# Define webcam feed position
rect_x, rect_y, rect_w, rect_h = 55, 260, 633, 400
offset_x, offset_y = -50, -30  # Move feed left and up

# Load encoded file
print("Loading encoded file...")
with open('EncodedFile.p', 'rb') as file:
    encodeListKnownIDs = pickle.load(file)
encodeListKnown, studentID = encodeListKnownIDs
print("Encoded file loaded.")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Error: Could not read frame from webcam.")
        continue  # Skip this loop iteration

    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Reduce size for faster processing
    imgRGB = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Detect faces
    faceCurrentFrame = face_recognition.face_locations(imgRGB)

    encodeCurrentFrame = face_recognition.face_encodings(imgRGB, faceCurrentFrame)

    img_resized = cv2.resize(img, (rect_w, rect_h))
    h_bg, w_bg, _ = imgBackground.shape
    h_res, w_res, _ = img_resized.shape

    # Ensure it does not exceed background image size
    if (rect_y + offset_y + h_res) <= h_bg and (rect_x + offset_x + w_res) <= w_bg:
        imgBackground[rect_y + offset_y:rect_y + offset_y + h_res,
        rect_x + offset_x:rect_x + offset_x + w_res] = img_resized
    else:
        print("Error: Webcam feed does not fit in background image")

    # Display mode icon if available
    if len(imgModeList) > 3:
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        print("Error: Not enough icon images.")
    if faceCurrentFrame:
        # Face Recognition Processing
        for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

            #print("Matches:", matches)
            #print("Face Distance:", faceDistance)

            matchIndex = np.argmin(faceDistance)
            print("match index", matchIndex)

            if matches[matchIndex]:
                # print("face identified")
                # print(studentID[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale up the coordinates

                # Define bounding box
                top_left = (x1 - 50, y1 + 163)
                bottom_right = (x2 + 50, y2 + 163)

                # Draw rectangle using OpenCV
                color = (0, 255, 0)  # Green color
                thickness = 2  # Line thickness
                cv2.rectangle(imgBackground, top_left, bottom_right, color, thickness)
                id = studentID[matchIndex]
                #print(id)
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading...",(275,400))
                    cv2.imshow("RTU ATTENDANCE", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter!= 0: 

            if counter == 1:
                studentInfo = db.reference(f'students/{id}').get()   #getting the images
                print(studentInfo)
                blob = bucket.get_blob(f'images/{id}.png')          #getting the images
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent =cv2.imdecode(array,cv2.COLOR_BGRA2RGB)
                #updating the data
                datetimeObject = datetime.strptime(studentInfo['recent_attendance_time'],
                                                  "%Y-%m-%d %H:%M:%S")

                secondsElapsed= (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed >20:
                    ref = db.reference(f'students/{id}')
                    studentInfo['total attendance'] = int(studentInfo['total attendance']) + 1
                    ref.child('total attendance').set(studentInfo['total attendance'])
                    ref.child('recent_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType =3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType !=3:
                if 10<counter<15:
                    modeType =2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <=10:

                    total_attendance = studentInfo['total attendance']
                    # Set the position slightly lower and adjust font size
                    position = (900, 200)  # Adjust position if needed5
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.2  # Smaller font size
                    color = (81, 85, 0)  # Black text
                    thickness = 1  # Thinner line for smaller text
                    cv2.putText(imgBackground, f"Total.Attd: {total_attendance}", (800,110),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(studentInfo['name']), (910,360),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(studentInfo['Group']), (920, 475),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(id), (950, 420),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(studentInfo['level']), (905, 525),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(studentInfo['study cycle']), (880, 573),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (81, 85, 0), 2)

                    cv2.putText(imgBackground, str(studentInfo['recent_attendance_time']), (970, 620),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (81, 85, 0), 2)

                    imgBackground[156:156+160,918:918+160] = imgStudent






           #resetting
                counter += 1

                if counter >=15:
                    counter = 0
                    modeType = 0
                    studentInfo =[]
                    imgStudent =[]
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0


    # Display output
    cv2.imshow("RTU ATTENDANCE", imgBackground)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
