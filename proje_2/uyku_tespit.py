import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture("C:/Users/feyza/Documents/proje_2/uyku_tespit/video1.mp4")
detector = FaceMeshDetector()
plotY = LivePlot(540, 360, [10, 60])

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
color = (0, 0, 255)
counter = 0
blinkCounter = 0
imgStack = None

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

        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftRight, leftLeft)

        cv2.line(img, leftUp, leftDown, (0, 255, 0), 3)
        cv2.line(img, leftRight, leftLeft, (0, 255, 255), 3)

        ratio = int(lenghtVer / lenghtHor * 100)
        ratioList = []
        ratioList.append(ratio)

        if len(ratioList) > 3:
            ratioList.pop(0)

        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 255, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0, 0, 255)
        
        if blinkCounter >= 5:
            cvzone.putTextRect(img, 'Uykunuz gelmis olabilir!', (30, 100), colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

    cv2.imshow("img", imgStack)
    if cv2.waitKey(150) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


