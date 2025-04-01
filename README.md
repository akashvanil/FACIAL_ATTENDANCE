# 🎓 Face Recognition Attendance System for RTU Liepaja 

This is a Python-based Face Recognition Attendance System built for a university project by **Akash Veeranmalayil Anil**. 

This is a real-time **Face Recognition Attendance System** built with **OpenCV**, **face_recognition**, **Firebase**, and **Flask**. It detects and recognizes faces from a webcam feed, logs attendance, displays student info, and uses **Firebase Storage** and **Realtime Database** for cloud-based storage and synchronization.

---

## 🚀 Features

- Real-time face detection and recognition
- Attendance tracking with time logging
- Student info displayed on custom UI background
- Firebase Realtime Database for attendance records
- Firebase Storage for student image retrieval
- Flask web server with live video streaming


---

## 🛠️ Tech Stack

- Python
- OpenCV
- Dlib
- face_recognition
- NumPy
- CVZone
- Flask
- Firebase Admin SDK (for Firebase Storage)
- CMake (for Dlib installation)
- html

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/akashvanil/FACIAL_ATTENDANCE.git
```

## 🧰 Install a C++ Compiler

Dlib requires a C++ compiler to be installed before it can build properly.

### 🪟 For Windows
- Download and install **Visual Studio Build Tools**:  
  [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
``` bash
```

## 👍install dependencies
```
pip install opencv-python face_recognition numpy cvzone Flask firebase-admin cvzone
```

## 🧪 Firebase Configuration
Go to https://console.firebase.google.com
Create a new project.
Go to Project Settings > Service Accounts, and generate a private key.
Download the JSON file and place it in your project directory.
Update this line in main.py with your project info:

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project.firebaseio.com/',
    'storageBucket': 'your-project.appspot.com'
})
finish setting your database 
```
```
## 🧪 How the System Works
```
Loads known face encodings from EncodedFile.p

Starts webcam and reads frames in real-time

Uses face_recognition to compare with known encodings

If match is found:

Displays student info

Updates total attendance in Firebase

Uploads and retrieves student image from Firebase Storage

Displays everything on a custom background with UI elements

Serves a live video stream via Flask

```bas
```
## 🙌 Author
Akash Veernmalayil Anil

```bash
```

## sample screenshot




