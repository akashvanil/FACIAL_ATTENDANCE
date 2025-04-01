import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")

# Replace with  database URL from Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rtu-attendance-31d29-default-rtdb.firebaseio.com/',
    'storageBucket': 'rtu-attendance-31d29.firebasestorage.app'
})
#importing students images
folderPath = 'images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentID = []

for path in PathList:
    icon_path = os.path.join(folderPath, path)  # Get the full path for each icon
    icon_image = cv2.imread(icon_path)
    if icon_image is not None:
        imgList.append(icon_image)
        #print(f"Loaded imgList: {path}")
        #print(os.path.splitext(path)[0])
        studentID.append(os.path.splitext(path)[0])
    else:
        print(f"Error loading imgList: {path}")
#print(studentID)

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncode(imagesList):
    encodeList =[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("encoding is started....")
encodeListKnown = findEncode(imgList)
encodeListKnownIDs = [encodeListKnown, studentID]
print("encoding is completed")

file = open("EncodedFile.p", 'wb')
pickle.dump(encodeListKnownIDs, file)
file.close()
print("file is saved")