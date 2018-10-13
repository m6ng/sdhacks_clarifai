import cv2 as cv
import os
from threading import Thread
import clarifai
from clarifai.rest import ClarifaiApp

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
        self.concepts = None
    
    def start(self):
        Thread(target=self.predict, args=()).start()
        return self
    
    def predict(self):
        while not self.stopped:
            try:
                prediction = self.model.predict_by_filename(self.filename)
                self.concepts = prediction["outputs"][0]["data"]["concepts"]
                for i in range(5):
                    print(self.concepts[i])
                print("")
            except (clarifai.errors.ApiError):
                continue

    def stop(self):
        self.stopped = True

class FrameDrawer():
    def __init__(self, frame, concepts):
        self.frame = frame 
        self.stopped = False
    
    def start(self):
        Thread(target=self.draw, args=()).start()
        return self

    def draw(self):
        while not self.stopped:
            self.img = cv.resize(self.frame, None, fx=2, fy=2)

            if (self.concepts != None):
                text = ""
                for i in range(5):
                    text += self.concepts[i]['name'] + " "
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(self.img, text, (50, 50), font, 2, (255, 100, 50), 2)

            cv.imshow("Display", self.img)
            if (cv.waitKey(1) == ord("q")):
                self.stopped = True
    
    def stop(self):
        self.stopped = True

def main(source=0, filename="frame.jpg"):
    frameGetter = FrameGetter(source, filename).start()
    clarifaiPredict = ClarifaiPredict(filename).start()
    frameDrawer = FrameDrawer(frameGetter.frame, clarifaiPredict.concepts).start()

    while (True):
        if (frameGetter.stopped or clarifaiPredict.stopped or frameDrawer.stopped):
            frameGetter.stop()
            clarifaiPredict.stop()
            frameDrawer.stop()
            break
        
        frameDrawer.frame = frameGetter.frame
        frameDrawer.concepts = clarifaiPredict.concepts

main()

os.remove("frame.jpg")
cv.destroyAllWindows()