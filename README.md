# 🎓 Face Recognition Attendance System for RTU Liepaja 

This is a Python-based Face Recognition Attendance System built for a university project by **Akash Veeranmalayil Anil**. It uses computer vision and deep learning techniques to detect and recognize faces in real-time, automatically marking attendance when a registered face is detected.

---

## 🚀 Features

- Real-time face detection and recognition
- Face encoding using deep learning (`dlib`)
- Simple and clean UI with `CVZone`
- Easily extendable for new users/faces
- Attendance data stored in firebase database

---

## 🛠️ Tech Stack

- Python
- OpenCV
- Dlib
- face_recognition
- CVZone
- NumPy
- CMake (for Dlib installation)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/akashvanil/FACIAL_ATTENDANCE.git

### 2. Install a C++ Compiler

Dlib requires a C++ compiler to build properly. Make sure you have a working compiler installed before proceeding.

#### 🪟 Windows
Install **Visual Studio Build Tools**:
- Go to [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- During installation, select:
  - "C++ build tools"
  - "Windows 10 SDK" or later

#### 🐧 Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install build-essential
