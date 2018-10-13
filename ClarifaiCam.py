import cv2

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    cv2.imshow("webcam", frame)
    if (cv2.waitKey(1) == 27):
        break

cv2.destroyAllWindows()