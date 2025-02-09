#!/usr/bin/env python3

# Importing the necessary modules 
import os
import cv2
import json
import pickle
import base64
import numpy as np
from datetime import datetime
from flask import Flask, request, Blueprint, session, redirect, jsonify, url_for, render_template

# Setting up model paths
detectorModel = os.path.join('Dashboard', 'models', 'face_detection_model')
embeddingModel = os.path.join('Dashboard', 'models', 'embeddingModel.t7')
recognizerModel = os.path.join('Dashboard', 'models', 'output', 'recognizer.pickle')
labelModel = os.path.join('Dashboard', 'models', 'output', 'le.pickle')

# Setting the confidence value 
confidenceValue = 0.6

# Load models
protoPath = os.path.join(detectorModel, 'deploy.prototxt')
modelPath = os.path.join(detectorModel, 'res10.caffemodel')

detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
embedder = cv2.dnn.readNetFromTorch(embeddingModel)

# Loading the actual face recognition model along with the label encoder 
recognizer = pickle.loads(open(recognizerModel, 'rb').read())
le = pickle.loads(open(labelModel, 'rb').read())

dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates',
                      static_folder='static')


# Creating a function for processing the image 
def processImageFunction(imageData):
    # reading the frame into memory 
    frame = cv2.imread(imageData)
    
    (h, w) = frame.shape[:2]
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                      (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= confidenceValue:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')

            face = frame[startY:endY, startX:endX]  # Corrected slicing
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                             (0, 0, 0), swapRB=True, crop=False)

            embedder.setInput(faceBlob)
            vec = embedder.forward()

            prediction = recognizer.predict_proba(vec)[0]
            result = np.argmax(prediction)
            name = le.classes_[result]

            predName = f'{name}'
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(frame, predName, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            

    _, buffer = cv2.imencode('.jpg', frame)
    processedImage = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/jpeg;base64,{processedImage}"


# Creating a function for processing the frame 
def processFrame(imageData):
    encodedData = imageData.replace("data:image/jpeg;base64,", "")
    nparr = np.frombuffer(base64.b64decode(encodedData), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    (h, w) = frame.shape[:2]
    imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                      (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= confidenceValue:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')

            face = frame[startY:endY, startX:endX]  # Corrected slicing
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                                             (0, 0, 0), swapRB=True, crop=False)

            embedder.setInput(faceBlob)
            vec = embedder.forward()

            prediction = recognizer.predict_proba(vec)[0]
            result = np.argmax(prediction)
            name = le.classes_[result]

            predName = f'{name}'
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(frame, predName, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            

    _, buffer = cv2.imencode('.jpg', frame)
    processedImage = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/jpeg;base64,{processedImage}"

# Creating a route for processing the frame 
@dashboard.route("/processFrame", methods=['POST'])
def processVideoFrame():
    try:
        data = request.get_json()
        imageData = data.get('image')

        if not imageData:
            return jsonify({"status": "error", "message": "No image data", "statusCode": 400})

        processedImage = processFrame(imageData)
        return jsonify({"processedImage": processedImage, "status": "success", "statusCode": 200})

    except Exception as e:
        return jsonify({"error": str(e), "statusCode": 500, "message": str(e)})

# Home route 
@dashboard.route('/', methods=['GET'])
def Dashboard():
    if 'email' in session:
        return render_template('Dashboard.html')
    return redirect(url_for('home.HomePage'))


# Creating a route for processing the image 
@dashboard.route("/processImage", methods=['POST'])
def processImage(): 
    # Get the image file 
    image = request.files['image'] 

    # if the image is present 
    if image: 
        # Getting the image file name 
        filename = image.filename

        # Getting the image extension 
        imgExt = filename.split(".")[1]

        # Getting the date timestamp value for the image uploaded 
        timestampValue = datetime.now().isoformat(timespec='seconds')
        filename = timestampValue + '.' + imgExt; 

        # Setting the full path for the image upload directory 
        imageUploadDir = "Uploads"
        imageUploadDir = os.path.sep.join([imageUploadDir, filename])

        # Saving the image to disk 
        image.save(imageUploadDir)

        #
        try:  
            image = processImageFunction(imageUploadDir)
            return jsonify({
                "processedImage": image,
                "status": "success", 
                "statusCode": 200
            })
        
        # 
        except Exception as error: 
            return jsonify({
                "imageUrl": "", 
                "status": "error", 
                "message": str(error), 
                "statusCode": 404
            })
