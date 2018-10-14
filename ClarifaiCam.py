import cv2 as cv
import numpy as np
import os
from threading import Thread
import clarifai
from clarifai.rest import ClarifaiApp

mainWindow = cv.namedWindow("MAIN", flags=cv.WINDOW_KEEPRATIO | cv.WINDOW_GUI_EXPANDED)
cv.moveWindow("MAIN", 0, 0)
cv.resizeWindow("MAIN", 500, 500)
conceptsWindow = cv.namedWindow("CONCEPTS", flags=cv.WINDOW_KEEPRATIO | cv.WINDOW_GUI_EXPANDED)
cv.moveWindow("CONCEPTS", 0, 500)
cv.resizeWindow("CONCEPTS", 500, 500)

class FrameGetter():
    def __init__(self, src=0, filename="frame.jpg"):
        self.filename = filename
        self.cap = cv.VideoCapture(src)
        (grabbed, self.frame) = self.cap.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            (grabbed, self.frame) = self.cap.read()
            cv.imwrite(self.filename, self.frame)

    def stop(self):
        self.stopped = True

class ClarifaiPredict:
    def __init__(self, filename):
        self.app = ClarifaiApp(api_key="6159ef1a7d5d43dcb85ed1cfd7670e4e")
        self.model = self.app.public_models.general_model
        self.filename = filename
        self.stopped = False
        self.prediction = None

    def start(self):
        Thread(target=self.predict, args=()).start()
        return self

    def predict(self):
        while not self.stopped:
            try:
                self.prediction = self.model.predict_by_filename(self.filename)
                concepts = self.prediction['outputs'][0]['data']['concepts']
                for i in range(5):
                    concept = concepts[i]
                    print(concept["name"], concept["value"])
                print("")
            except (clarifai.errors.ApiError):
                continue

    def stop(self):
        self.stopped = True

class FrameDrawer():
    def __init__(self, frame, prediction):
        self.frame = frame
        self.prediction = prediction
        self.stopped = False

    def start(self):
        Thread(target=self.draw, args=()).start()
        return self

    def draw(self):
        while not self.stopped:
            self.img = cv.resize(self.frame, None, fx=1, fy=1)
            height = 500
            width = 1000
            textDisplay = np.zeros((height,width,3), np.uint8)

            if (self.prediction != None):
                concepts = self.prediction['outputs'][0]['data']['concepts']
                for i in range(5):
                    concept = concepts[i]
                    text = concept["name"] + " " + concept["value"]
                    print(text)
                    font = cv.FONT_HERSHEY_SIMPLEX
                    cv.putText(textDisplay, text, (50, 100 + i * 50), font, 1, (255, 255, 255), 2)

            cv.imshow("MAIN", self.img)
            cv.imshow("CONCEPTS", textDisplay)
            if (cv.waitKey(1) == ord("q")):
                self.stopped = True

    def stop(self):
        self.stopped = True

def main(source=0, filename="frame.jpg"):
    frameGetter = FrameGetter(source, filename).start()
    clarifaiPredict = ClarifaiPredict(filename).start()
    frameDrawer = FrameDrawer(frameGetter.frame, clarifaiPredict.prediction).start()

    while (True):
        if (frameGetter.stopped or clarifaiPredict.stopped or frameDrawer.stopped):
            frameGetter.stop()
            clarifaiPredict.stop()
            frameDrawer.stop()
            break

        frameDrawer.frame = frameGetter.frame
        frameDrawer.perdiction = clarifaiPredict.prediction

main()

os.remove("frame.jpg")
cv.destroyAllWindows()
