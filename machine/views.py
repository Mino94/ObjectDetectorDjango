from django.shortcuts import render , render_to_response
# from .serializers import VersionSerializer
# from .models import Version
from rest_framework import viewsets
import cv2
import numpy as np
from django.http import StreamingHttpResponse
import os
import serial
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
from .form import PostForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import base64

@csrf_exempt
def new(request):
        global new_frame
        global tfnet
        global newImage, confidence
        
        if confidence >= 0.9:
                converted = cv2.imencode('.jpg', newImage)[1].tostring()
                encoded = base64.b64encode(converted) # encoding  # json형태로 바꿔라
                return HttpResponse(encoded)
        else:
                return HttpResponse("Not minho!!!")

#----------------------------Camera Web으로 불러오기 --------------------

def index(request):
        return render(request, 'index.html')
#-----------------------------------------------------------------------------------------------------
options = {"model": "/home/keti/Desktop/MachineWeb/machine_api/darkflow/cfg/yolo-obj.cfg", "load":"/home/keti/Desktop/MachineWeb/machine_api/darkflow/backup_mh/yolo-obj_final.weights", "labels":"/home/keti/Desktop/MachineWeb/machine_api/darkflow/labels.txt", "threshold": 0.1, "gpu":0.7}


tfnet = TFNet(options)

cap = cv2.VideoCapture(0)
def gen():
        global cap
        global options  
        global tfnet
        global frame, results
        global new_frame
        print('Starting camera thread')
        while True:
                ret, frame = cap.read()
                if ret == True:
                        frame = np.asarray(frame)
                        
                        results = tfnet.return_predict(frame)
                        new_frame = boxing(frame, results)
                ret, jpeg = cv2.imencode('.jpg', new_frame) 
                
                get_frame = jpeg.tobytes() # jpg 를  Byte 로 변환

                yield (b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' + get_frame + b'\r\n')
                        
def video_feed(request):
        return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')

def boxing(original_img, predictions):
    global minholabel 
    global newImage, confidence
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']

        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 3))

        minholabel=result['label']

        if confidence > 0.9:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
    return newImage

