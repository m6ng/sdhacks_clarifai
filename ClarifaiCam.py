import cv2 as cv
import os
import time
from clarifai.rest import ClarifaiApp

cap = cv.VideoCapture(0)
app = ClarifaiApp(api_key="6159ef1a7d5d43dcb85ed1cfd7670e4e")
model = app.public_models.general_model

def captureImageToFile(filename):
    ret, frame = cap.read()
    cv.imwrite(filename, frame)
    return frame 

def scale(img):
    return cv.resize(img, None, fx=1, fy=1, interpolation = cv.INTER_CUBIC)

def predictImage(filename):
    return model.predict_by_filename(filename)

def printConcepts(frame, response):
    concepts = response["outputs"][0]["data"]["concepts"]
    text = ""
    for i in range(5):
        text += concepts[i]['name'] + " "
        print(concepts[i])
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, text, (0, 100), font, 1, (200, 0, 0), 2)
    print("")

current_milli_time = lambda: int(round(time.time() * 1000))

def update():
    frame = captureImageToFile("frame.jpg")
    res = scale(frame)
    response = predictImage("frame.jpg")
    printConcepts(res, response)

    cv.imshow("webcam", res)
    os.remove("frame.jpg")

lastTime = current_milli_time()
while (True):
    if (lastTime + 5000 > current_milli_time()):
        update()
        lastTime = current_milli_time()

    if (cv.waitKey(1) == ord("q")):
        break
    

cv.destroyAllWindows()