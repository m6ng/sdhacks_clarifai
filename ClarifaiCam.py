import cv2
from clarifai.rest import ClarifaiApp

cap = cv2.VideoCapture(0)
app = ClarifaiApp(api_key="6159ef1a7d5d43dcb85ed1cfd7670e4e")
model = app.public_models.general_model

def captureImageToFile(filename):
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)
    return frame

def evalImage(filename):
    return model.predict_by_filename(filename)

def printConcepts(frame, response):
    concepts = response["outputs"][0]["data"]["concepts"]
    for concept in concepts:
        print(concept['name'], concept['value'])

while (True):
    frame = captureImageToFile("frame.jpg")
    response = evalImage("frame.jpg")
    printConcepts(frame, response)

    cv2.imshow("webcam", frame)
    if (cv2.waitKey(1) == 27):
        break

cv2.destroyAllWindows()