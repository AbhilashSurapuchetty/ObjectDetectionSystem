# Object Detection System

This project is part of the internship at CodeClause, where the objective is to develop an object detection system using YOLOv3.

## Project Structure

ObjectDetectionSystem/
│
├── images/
│ └── test.png
│
├── venv/
│ ├── ... (Virtual environment files)
│ └── ... (Other files)
│
├── videos/
│ └── vid1.mp4
│
├── yolo/
│ ├── coco.names
│ ├── yolov3.cfg
│ └── yolov3.weights (not included, see below)
│
├── .gitattributes
├── main.py
└── README.md

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/AbhilashSurapuchetty/CodeClause-ObjectDetectionSystem.git
cd CodeClause-ObjectDetectionSystem 

### 2. Setup the Virtual Environment
Create and activate a virtual environment:
Windows:

python -m venv venv
venv\Scripts\activate
Linux/MacOS:

python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
Install the required packages:

pip install -r requirements.txt

### 4. Download Large Files
Due to file size constraints, the yolov3.weights and pywrap_tensorflow_internal.pyd files are not included in this repository. Download them from the links provided below and place them in the appropriate directories.
link to google Drive : https://drive.google.com/drive/folders/1lLr1VU-Gp1zZF1r1MeVme0xoUxBXfqMe
yolov3.weights - Place in yolo/ directory.
pywrap_tensorflow_internal.pyd - Place in venv/Lib/site-packages/tensorflow/python/ directory.

### 5. Run the Project
Once everything is set up, you can run the project:
python main.py
