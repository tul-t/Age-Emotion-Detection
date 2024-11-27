from keras.models import load_model
import numpy as np
import cv2
from keras.utils import img_to_array
from keras.preprocessing import image
from PIL import ImageGrab
import sys
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="tul#21MySQL", database="emotions")
cursor = conn.cursor()

print("Connection Established: " + str(conn.is_connected()))

def emotion_instances(emotions_):
    emotions = {"angry":0, "happy":0, "sad":0, "neutral":0, "disgust":0, "surprise":0, "fear":0}

    for k in emotions_:
        if k.lower() == "angry":
            emotions["angry"] += 1
        elif k.lower() == "happy":
            emotions["angry"] += 1
        elif k.lower() == "sad":
            emotions["sad"] += 1
        elif k.lower == "neutral":
            emotions["neutral"] += 1
        elif k.lower() == "disgust":
            emotions["disgust"] += 1
        elif k.lower() == "surprise":
            emotions["surprise"] += 1
        elif k.lower() == "fear":
            emotions["fear"] += 1
    
    min, max = emotions["angry"], emotions["angry"]
    least_emotion, common_emotion = "Angry", "Angry" 
        
    for k in emotions:
        if emotions[k] < min:
            min, least_emotion = emotions[k], k
        if emotions[k] > max:
            max, common_emotion = emotions[k], k
    return least_emotion, common_emotion

#arg = sys.argv[1] 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
prediction_model = load_model('model')
age_model = load_model('age')

#if (arg == '-c'):
capture = cv2.VideoCapture(0)

emotion_labels = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}
colors = {0:(0, 128, 255), 1:(246, 61, 252), 2:(246, 61, 252), 3:(0,255,90), 4:(204, 204, 204), 5:(237, 28, 63), 6:(252,238,33)}

while True:
    camera = True
    user_id = 1
    #if (arg == '-c'):
    _, frame = capture.read()

    #else:    
    #    camera = False
    #    frame = np.array(ImageGrab.grab(bbox=(40,300,1200,1000)))
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi = gray[y : y + h, x : x + w]
        roi = cv2.resize(roi, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi]) != 0:
            roi_ = roi.astype('float')/255.0
            roi_ = img_to_array(roi_)
            print(roi_.ndim, roi_.shape)
            roi_ = np.expand_dims(roi_, axis=0)
            print(roi_.shape)

            prediction = prediction_model.predict(roi_)[0]
            emotion = emotion_labels[prediction.argmax()]
            age = str(int(age_model.predict(roi_)))
            label_pos = (x, y - 10)

            cv2.putText(frame, f'{emotion}, {age}', label_pos, cv2.FONT_HERSHEY_PLAIN, 2, colors[prediction.argmax()], 2)
            cursor.execute(f'insert into EmotionTracker values("{user_id}","{emotion}", "{age}")')
            print("added to database")
        else:
            pass
    
    if not camera:
        cv2.imshow('Detector', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    else:
        cv2.imshow('Detector', frame)

    

    if cv2.waitKey(1) == ord('Q'):
        break

cv2.destroyAllWindows()

opt = int(input("1 - Retrieve user emotions, 2 - Quit :"))

if (opt ==1 ):
    cursor.execute(f'select * from EmotionTracker where user_id=1')
    for k in cursor.fetchall():
        print(k)
    #max_emotion
    #min_emotion
    #max_age
    #min_age