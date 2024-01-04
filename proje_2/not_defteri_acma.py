import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import os

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector()

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
color = (0, 0, 255)
counter = 0

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)
    
    if faces:
        face = faces[0]
        
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)
        
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftRight, leftLeft)
        
        cv2.line(img, leftUp, leftDown, (0, 255, 0), 3)
        cv2.line(img, leftRight, leftLeft, (0, 255, 255), 3)
        
        ratio = int(lengthVer / lengthHor * 100)
        
        if ratio < 35 and counter == 0:
            counter += 1
            color = (0, 255, 0)
            os.startfile("notepad.exe")
        
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0, 0, 255)
        
    cv2.imshow("img", img)
    if cv2.waitKey(150) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

