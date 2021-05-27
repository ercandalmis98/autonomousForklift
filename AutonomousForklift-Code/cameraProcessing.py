import numpy as np
from imageProcessing import ImageProcessing
import cv2
class CameraProcessing:
    def __init__(self):
        self.minX1 = None
        self.minY1 = None
        self.maxX2 = None
        self.maxY2 = None
        self.green_in_the_middle = False
        self.search_for_green = False
        self.gathering_stuff_flag = False
        self.in_operation = False
        self.switching = False
        self.blue_in_the_middle = False
        self.blue_making_single_flag = False
        self.operation_flag = False

    def capturingFunction(self,image,searching_lane,is_gathering,is_placing,gathering_done,placing_done):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image_cpy = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image_cpy2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        middle_line = int(self.image.shape[1] / 2)
        middle_line_horizontal = int(self.image.shape[0] / 2)
        self.switching = False
        self.searching_lane = searching_lane
        
        #print(self.image[3][3])
        #print(self.image.shape[0],self.image.shape[1]) 135-224
        
        #BLUE LANE SEARCHING
        decision_image_of_bi = ImageProcessing.blueDetection(self, self.image_cpy2)
        canny_image_of_bi = ImageProcessing.canny(self, decision_image_of_bi)
        lines_of_bi = ImageProcessing.cHoughLinesP(self, canny_image_of_bi, 0, 0)
        #cv2.imshow("decision_image", canny_image_of_bi)
        
        if gathering_done is True or placing_done is True:
            self.operation_flag = True

        if self.operation_flag is True:
            count_bi = 0
            sumX_bi = 0
            sumY_bi = 0
            if lines_of_bi is not None:
                for line in lines_of_bi:
                    count_bi += 2
                    x1, y1, x2, y2 = line.reshape(4)
                    sumX_bi += (x1 + x2)
                    sumY_bi += (y1 + y2)
                #avgX = int(sumX_bi / count_bi)
                avg_of_blueLines = int(sumY_bi / count_bi)
                ImageProcessing.showingLines(self, self.image_cpy, 0, middle_line_horizontal, self.image_cpy.shape[1], middle_line_horizontal, 255, 0, 0)
                ImageProcessing.showingLines(self, self.image_cpy, 0, avg_of_blueLines, self.image_cpy.shape[1], avg_of_blueLines, 255, 255, 0)
                #ImageProcessing.showingScreen(self, "Blue Lane", self.image_cpy)
                if (middle_line_horizontal - int(self.image.shape[0] / 10)) <= avg_of_blueLines <= (middle_line_horizontal + int(self.image.shape[0] / 10)) and self.blue_making_single_flag is False:
                    self.operation_flag = False   
                    self.switching = True 

        #print(is_gathering,is_placing,self.switching ,self.searching_lane)

        #GREEN LANE SEARCHING
        if is_placing is True:
            self.search_for_green = True
        if is_gathering is False:
            if self.search_for_green == True:
                decision_image = ImageProcessing.greenDetection(self, self.image_cpy)
                canny_image_of_di = ImageProcessing.canny(self, decision_image)
                lines_of_di = ImageProcessing.cHoughLinesP(self, canny_image_of_di, 0, 0)
                #cv2.imshow("decision_image", canny_image_of_di)
                
                count_di = 0
                sumX_di = 0
                sumY_di = 0
                if lines_of_di is not None:
                    for line in lines_of_di:
                        count_di += 2
                        x1, y1, x2, y2 = line.reshape(4)
                        sumX_di += (x1 + x2)
                        sumY_di += (y1 + y2)
                    #avgX = int(sumX_di / count_di)
                    avg_of_greenLines = int(sumY_di / count_di)
                    ImageProcessing.showingLines(self, self.image_cpy, 0, middle_line_horizontal, self.image_cpy.shape[1], middle_line_horizontal, 255, 0, 0)
                    ImageProcessing.showingLines(self, self.image_cpy, 0, avg_of_greenLines, self.image_cpy.shape[1], avg_of_greenLines, 255, 255, 0)
                    ImageProcessing.showingScreen(self, "Green Lane", self.image_cpy)
                    if (middle_line_horizontal - int(self.image.shape[0] / 15)) <= avg_of_greenLines <= (middle_line_horizontal + int(self.image.shape[0] / 15)):
                        self.green_in_the_middle = True     
    
        if self.searching_lane == "blue" or self.searching_lane == "none":
            searching_image = ImageProcessing.blueDetection(self, self.image)
        elif self.searching_lane == "red":
            searching_image = ImageProcessing.redDetection(self, self.image)
        elif self.searching_lane == "yellow":
            searching_image = ImageProcessing.yellowDetection(self, self.image)
        elif self.searching_lane == "white":
            searching_image = ImageProcessing.whiteDetection(self, self.image)
        
        if self.green_in_the_middle is False:
            canny_image = ImageProcessing.canny(self, searching_image)
            lines = ImageProcessing.cHoughLinesP(self, canny_image, 0, 0)
            cv2.imshow("canny_image", canny_image)
            count = 0
            sumX = 0
            sumY = 0
            if lines is not None:
                #print("lines exist")
                for line in lines:
                    count += 2
                    x1, y1, x2, y2 = line.reshape(4)
                    sumX += (x1 + x2)
                    sumY += (y1 + y2)
                #avgX = int(sumX / count)
                avg_of_leftCamLines = int(sumX / count)
                ImageProcessing.showingLines(self, self.image, middle_line, 0, middle_line, self.image.shape[0], 255, 0, 0)
                ImageProcessing.showingLines(self, self.image, avg_of_leftCamLines, 0, avg_of_leftCamLines, self.image.shape[0], 255, 255, 0)
                ImageProcessing.showingScreen(self, "Lane", self.image)
                if (middle_line - int(middle_line / 10)) <= avg_of_leftCamLines <= (middle_line + int(middle_line / 10)):
                    return True, False, False, False, avg_of_leftCamLines,self.switching #F L R E lane_position 
                elif (middle_line - int(middle_line/10)) > avg_of_leftCamLines:
                    return False, True, False, False, avg_of_leftCamLines,self.switching #F L R E lane_position 
                elif avg_of_leftCamLines > (middle_line + int(middle_line/10)):
                    return False, False, True, False, avg_of_leftCamLines,self.switching #F L R E lane_position 
            else:
                #print("Searching lines does not exist")
                return  False, False, False, True, -1,self.switching #F L R E lane_position 
        else:
            #yeşilin ortalanmasının dönmesi, aracı durdurmak için
            self.search_for_green = False
            self.green_in_the_middle = False
            return  False, False, False, True, -1000,self.switching #F L R E lane_position
    