import cv2

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BAYER_GB2GRAY)
    cv2.imshow('frame', gray)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.relase()
cv2.destroyAllWindows()