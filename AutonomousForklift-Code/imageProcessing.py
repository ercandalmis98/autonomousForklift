import cv2
import numpy as np

class ImageProcessing:
    def __init__(self, imageName = None):
        self.imageName = imageName
        self.image = None
        self.slope = None

    def canny(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (1,1), 0)
        canny = cv2.Canny(blur, 50, 150)
        return canny

    def whiteDetection(self, image):
        #iki deneme mavi renk aralıgı
        #188-146-93
        #208-166-113
        #236-195-144
        #172-130-78
        lowerColor = np.array([150, 120, 70])
        upperColor = np.array([255, 220, 170])
        mask = cv2.inRange(image, lowerColor, upperColor)
        whiteDetectedImage = cv2.bitwise_and(image, image, mask = mask)
        #cv2.imshow("whiteDetection", whiteDetectedImage)
        return whiteDetectedImage
    
    def blueDetection(self, image):
        #iki deneme mavi renk aralıgı
        #15-89-231
        #6-78-221
        #255-112-19
        #7-87-243
        #170-54-2
        #228-78-3
        lowerColor = np.array([140, 40, 0])
        upperColor = np.array([235, 80, 30])
        mask = cv2.inRange(image, lowerColor, upperColor)
        blueDetectedImage = cv2.bitwise_and(image, image, mask = mask)
        #cv2.imshow("blueDetection", blueDetectedImage)
        return blueDetectedImage

    def greenDetection(self, image):
        #iki deneme mavi renk aralıgı
        #32-179-23
        #33-155-20
        #39-204-28
        #48-255-36
        lowerColor = np.array([15, 112, 10])
        upperColor = np.array([55, 210, 30])
        mask = cv2.inRange(image, lowerColor, upperColor)
        greenDetectedImage = cv2.bitwise_and(image, image, mask = mask)
        #cv2.imshow("greenDetection", greenDetectedImage)
        return greenDetectedImage
    
    def yellowDetection(self, image):
        #iki deneme mavi renk aralıgı
        #33-164-113
        #31-27-91
        #33-142-109
        #41-219-168
        #31-143-92

        lowerColor = np.array([20, 120, 65])
        upperColor = np.array([50, 240, 170])
        mask = cv2.inRange(image, lowerColor, upperColor)
        yellowDetectedImage = cv2.bitwise_and(image, image, mask = mask)
        #cv2.imshow("yellowDetection", yellowDetectedImage)
        return yellowDetectedImage

    def redDetection(self, image):
        #iki deneme mavi renk aralıgı
        #29-22-95
        #39-32-162
        #38-33-139
        #41-35-158
        #48-35-168
        lowerColor = np.array([24, 15, 70])
        upperColor = np.array([60, 50, 180])
        mask = cv2.inRange(image, lowerColor, upperColor)
        redDetectedImage = cv2.bitwise_and(image, image, mask = mask)
        #cv2.imshow("redDetection", redDetectedImage)
        return redDetectedImage

    def displayingScreen(self, text, image):
        cv2.imshow(text, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def showingScreen(self, text, image):
        cv2.imshow(text, image)
    
    def showingLines(self, image, x1, y1, x2, y2, colorParameter1, colorParameter2, colorParameter3):
        cv2.line(image, (x1, y1), (x2, y2), (colorParameter1, colorParameter2, colorParameter3), 2)

    def cHoughLinesP(self, image, minLineLength, maxLineGap):
        return cv2.HoughLinesP(image, 1, np.pi/180, 20, np.array([]), minLineLength, maxLineGap)

