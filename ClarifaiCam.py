import cv2 as cv
from clarifai.rest import ClarifaiApp

cap = cv.VideoCapture(0)
app = ClarifaiApp(api_key="6159ef1a7d5d43dcb85ed1cfd7670e4e")
model = app.public_models.general_model

def captureImageToFile(filename):
    ret, frame = cap.read()
    cv.imwrite(filename, frame)
    return frame 

def scale(img):
    return cv.resize(img, None, fx=2, fy=2, interpolation = cv.INTER_CUBIC)

def evalImage(filename):
    return model.predict_by_filename(filename)

def printConcepts(frame, response):
    concepts = response["outputs"][0]["data"]["concepts"]
    for concept in concepts:
        print(concept['name'], concept['value'])

while (True):
    frame = captureImageToFile("frame.jpg")
    res = scale(frame)
    response = evalImage("frame.jpg")
    printConcepts(res, response)

    cv.imshow("webcam", res)
    if (cv.waitKey(1) == 27):
        break

cv.destroyAllWindows()