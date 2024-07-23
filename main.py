import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs

import cv2
import numpy as np
import tensorflow as tf

class YOLOv3:
    def __init__(self, config_path, weights_path, names_path):
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.classes = open(names_path).read().strip().split("\n")

    def detect_objects(self, image):
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        return self.post_process(image, outputs)

    def post_process(self, image, outputs):
        height, width = image.shape[:2]
        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = f"{self.classes[class_ids[i]]}: {confidences[i]:.2f}"
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image

def detect_in_image(yolo, image_path):
    image = cv2.imread(image_path)
    result_image = yolo.detect_objects(image)
    cv2.imshow("Image", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_in_video(yolo, video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result_frame = yolo.detect_objects(frame)
        
        # Resize the frame to make it more manageable
        height, width = frame.shape[:2]
        new_width = int(width * 0.75)  # Decrease width by 25%
        new_height = int(height * 0.75)  # Decrease height by 25%
        resized_frame = cv2.resize(result_frame, (new_width, new_height))
        
        cv2.imshow("Video", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolo = YOLOv3("yolo/yolov3.cfg", "yolo/yolov3.weights", "yolo/coco.names")
    
    # Detect objects in an image
    detect_in_image(yolo, "images/test.png")
    
    # Detect objects in a video
    detect_in_video(yolo, "videos/vid1.mp4")
