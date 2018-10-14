from PIL import Image
import re
import requests
import cv2 as cv
import numpy as np
import os, glob
from threading import Thread
import clarifai
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

files = glob.glob('./img/*')
for f in files:
    os.remove(f)

app = ClarifaiApp(api_key="105fbb4fbd4046208e8c76191b470eb4")

USER_AGENT = USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
headers = { 'User-Agent': USER_AGENT }

isConfirmed = False
isPredicted = False
imageDisplayNum = 0
isWebcamMode = True

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
        global app
        self.model = app.public_models.general_model
        self.filename = filename
        self.stopped = False
        self.concepts = None

    def start(self):
        Thread(target=self.predict, args=()).start()
        return self

    def predict(self):
        while not self.stopped:
            global isPredicted
            if (isConfirmed and not isPredicted):
                try:
                    prediction = self.model.predict_by_filename(self.filename)
                    self.concepts = prediction["outputs"][0]["data"]["concepts"]
                    for concept in self.concepts:
                        print(concept)
                    print("")
                except (clarifai.errors.ApiError):
                    continue
                isPredicted = True
                global isPictureSwitched
                isPictureSwitched = True

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
            global isConfirmed
            global isWebcamMode
            if (not isConfirmed and isWebcamMode):
                self.displayWebcam()
            if (not isWebcamMode):
                self.displayMain()
            self.displayConcepts()
            self.displayGallery("img")
            self.handleInput()
            
    def displayWebcam(self):
        self.img = cv.resize(self.frame, None, fx=1, fy=1)
        cv.imshow("MAIN", self.img)
        cv.moveWindow("MAIN", 0, 0)
        cv.resizeWindow("MAIN", 1000, 500)

    def displayMain(self):
        cv.imshow("MAIN", self.img)
        cv.moveWindow("MAIN", 0, 0)
        cv.resizeWindow("MAIN", 1000, 500)

    def displayConcepts(self):
        height = 500
        width = 1000
        textDisplay = np.zeros((height,width,3), np.uint8)
        if (self.concepts != None):
            for i in range(len(self.concepts)):
                concept = self.concepts[i]
                text = concept['name'] + " ( " + str(round(concept['value'], 4)) + " )"
                font = cv.FONT_HERSHEY_COMPLEX_SMALL

                if (i < 10):
                    cv.putText(textDisplay, text, (30, 30 + 50 * i), font, 1, (255, 255, 255), 2)
                else:
                    cv.putText(textDisplay, text, (500, 30 + 50 * (i - 10)), font, 1, (255, 255, 255), 2)

        cv.imshow("CONCEPTS", textDisplay)
        cv.moveWindow("CONCEPTS", 0, 500)
        cv.resizeWindow("CONCEPTS", 1000, 500)
    
    def displayGallery(self, directory):
        for i in range(len(os.listdir(directory))):
            img = np.zeros((2000,1000,3), np.uint8)
            global imageDisplayNum
            if (i == imageDisplayNum):
                filename = os.listdir(directory)[i]
                path = directory + "/" + filename
                image = Image.open(path)
                img = cv.cvtColor(np.asarray(image), cv.COLOR_RGB2BGR)
                cv.putText(img, str(i), (20, 20), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                cv.imshow("BROWSER", img)

    def handleInput(self):
        global isWebcamMode
        global imageDisplayNum
        key = cv.waitKey(1)
        if (key == ord("j")):
            if (imageDisplayNum + 1 < len(os.listdir("img"))):
                imageDisplayNum += 1
        if (key == ord("k")):
            if (imageDisplayNum - 1 >= 0):
                imageDisplayNum -= 1
        if (key == ord("n")):
            global imageDisplayNum
            filename = os.listdir("img")[imageDisplayNum]
            path = "img" + "/" + filename
            image = Image.open(path)
            image_data = cv.cvtColor(np.asarray(image), cv.COLOR_RGB2BGR) 
            self.img = image_data 
            isWebcamMode = False
        if (key == ord("c") and isWebcamMode):
            global isConfirmed
            isConfirmed = True
        if (key == ord("r")):
            isConfirmed = False
            global isPredicted
            isPredicted = False
        if (key == ord("q")):
            self.stop()

    def stop(self):
        self.stopped = True

class ImageDiscovery:
    def __init__(self):
        self.concepts = None
        self.stopped = False

    def start(self):
        Thread(target=self.performImageDiscovery, args=()).start()
        return self

    def performImageDiscovery(self):
        while (not self.stopped):
            global isConfirmed
            if (isConfirmed == True and self.concepts != None):
                files = glob.glob('./img/*')
                for f in files:
                    os.remove(f)
                self.concepts = self.concepts[0:2]
                self.downloadImgs(self.urlLookup(self.concepts), "img")
                isConfirmed = False
                global isPredicted
                isPredicted = False

    def get_image_urls_fr_gs(self, query_key):
        query_key.replace(' ','+')
        tgt_url = 'https://www.google.com.sg/search?q={}&tbm=isch&tbs=sbd:0'.format(query_key)
        try:
            r = requests.get(tgt_url, headers = headers)
        except (requests.exceptions.ConnectionError):
            return None
        urllist = [n for n in re.findall('"ou":"([a-zA-Z0-9_./:-]+.(?:jpg|jpeg|png))",', r.text)]
        return urllist

    def urlLookup(self, concepts):
        urlList = []
        for concept in concepts:
            conceptName = concept["name"]
            rawUrlList = self.get_image_urls_fr_gs(conceptName)
            if (rawUrlList != None):
                for i in range(min(len(rawUrlList), 1)):
                    print(rawUrlList[i])
                    urlList.append(rawUrlList[i])
        return urlList

    def downloadImgs(self, urls, directory):
        for i in range(min(len(urls), 4)):
            url = urls[i]
            filename = url.split("/")[-1]
            r = requests.get(url)
            with open(directory + "/" + filename,'wb') as f:
                f.write(r.content)

        print("EVERYTHING IS FINISHED!!!")

    def stop(self):
        self.stopped = True

def main(source=0, filename="frame.jpg"):
    frameGetter = FrameGetter(source, filename).start()
    clarifaiPredict = ClarifaiPredict(filename).start()
    frameDrawer = FrameDrawer(frameGetter.frame, clarifaiPredict.concepts).start()
    imageDiscovery = ImageDiscovery().start()

    while (True):
        if (frameGetter.stopped or clarifaiPredict.stopped or frameDrawer.stopped or imageDiscovery.stopped):
            frameGetter.stop()
            clarifaiPredict.stop()
            frameDrawer.stop()
            imageDiscovery.stop()
            break

        frameDrawer.frame = frameGetter.frame
        frameDrawer.concepts = clarifaiPredict.concepts
        imageDiscovery.concepts = clarifaiPredict.concepts

main()

if (os.path.isfile("frame.jpg")):
    os.remove("frame.jpg")
cv.destroyAllWindows()

files = glob.glob('./img/*')
for f in files:
    os.remove(f)