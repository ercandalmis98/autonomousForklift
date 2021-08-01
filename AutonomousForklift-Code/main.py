import numpy as np
import cv2
import time
from cameraProcessing import CameraProcessing
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import pyautogui
import win32api

class SimulationProcessing:
    def __init__(self):
        #Carrying company_1 - company_2 - company_3 none
        self.carrying = "none"
        #searching lane
        self.searching_lane = "red"
        #Leaving stuff - True-False
        self.dropping_stuff = False
        #Finding stuff - True-False
        self.gathering_stuff = False
        #Finding stuff flag - True-False
        self.gathering_stuff_flag = False
        #Gathering stuff searching lane - True-False
        self.gathering_stuff_searching_lane = "yellow"
        #forklift level Default - bottom-1 - buttom-0 - mid-1 - mid-0 - top-1 - top-0
        self.forklift_level = "Default"
        #stock first(0. index) is bottom, last(2. index) is top
        self.stock = [[0,0,0],[0,0,0],[0,0,0]]
        #the placing operation flag
        self.placing_done = False
        #the gathering operation flag
        self.switch_operation = False
        #the placing operation
        self.is_gathering = True
        #the gathering operation
        self.is_placing = False

    def click_coordinates(self):
        """
        If the key state changes, get the positions
        """
        for pos in range(2):
            state_prev = win32api.GetKeyState(0x01)
            while True:
                state_current = win32api.GetKeyState(0x01)
                if state_current != state_prev:
                    pos = pyautogui.position()
                    print("**Positions set: ", pos)
                    return pos

    def set_pos(self):
        print('\n*Select first corner of the cam')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the cam')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.x = int(mouse_posX1)
        self.y = int(mouse_posY1)
        self.w = int(mouse_posX2)
        self.h = int(mouse_posY2)
        print("First area has been set!")
        """print('\n*Select first corner of the area of DL image')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the area of DL image')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.DL_x = int(mouse_posX1)
        self.DL_y = int(mouse_posY1)
        self.DL_w = int(mouse_posX2)
        self.DL_h = int(mouse_posY2)
        print("Second area has been set!(DL)")"""
 
    def lift_level_default_arranging(self,keyboard):
        keyboard.press("c")
        if self.forklift_level == "buttom-1" or self.forklift_level == "buttom-0":
            time.sleep(4)
        if self.forklift_level == "mid-1" or self.forklift_level == "mid-0":
            time.sleep(1.5)
        if self.forklift_level == "top-1" or self.forklift_level == "top-0":
            time.sleep(5)
        keyboard.release("c")
        self.forklift_level = "Default"
        print("Level arrangement done! (Default)")
        time.sleep(1)
    
    def lift_level_buttom_arranging(self,keyboard):
        keyboard.press("f")
        time.sleep(5)
        keyboard.release("f")
        self.forklift_level = "buttom-0"
        print("Level arrangement done! (Buttom)")
        time.sleep(1)

    def turn_back(self,keyboard):
        keyboard.press("x")
        time.sleep(0.1)
        keyboard.release("x")
        """if self.gathering_stuff is True:
            self.gathering_stuff = False
            self.gathering_stuff_flag = False"""

    def brake(self,keyboard):
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        keyboard.release(Key.up)
        keyboard.press(Key.space)

    def lane_tracing_activating(self,keyboard):
        self.turn_back(keyboard)
        time.sleep(0.2)

    def putting_stuff_buttom_1(self,keyboard):
        keyboard.press("g")
        if self.forklift_level == "Default":
            time.sleep(3.5)
        if self.forklift_level == "mid-1" or self.forklift_level == "mid-0":
            time.sleep(4.5)
        if self.forklift_level == "top-1" or self.forklift_level == "top-0":
            time.sleep(7.5)
        keyboard.release("g")
        self.forklift_level = "bottom-1"
        print("Level arrangement done! (buttom-1)")
        time.sleep(1)

    def dropping_stuff_buttom_0(self,keyboard):
        keyboard.press("f")
        time.sleep(1)
        keyboard.release("f")
        self.forklift_level = "bottom-0"
        print("Level arrangement done! (buttom-0)")
        time.sleep(1)

    def putting_stuff_mid_1(self,keyboard):
        keyboard.press("j")
        if self.forklift_level == "Default":
            time.sleep(1.5)
        if self.forklift_level == "buttom-1" or self.forklift_level == "buttom-0":
            time.sleep(4.5)
        if self.forklift_level == "top-1" or self.forklift_level == "top-0":
            time.sleep(4)
        keyboard.release("j")
        self.forklift_level = "mid-1"
        print("Level arrangement done! (mid-1)")
        time.sleep(1)

    def dropping_stuff_mid_0(self,keyboard):
        keyboard.press("h")
        time.sleep(1)
        keyboard.release("h")
        self.forklift_level = "mid-0"
        print("Level arrangement done! (mid-0)")
        time.sleep(1)

    def putting_stuff_top_1(self,keyboard):
        keyboard.press("l")
        if self.forklift_level == "Default":
            time.sleep(5)
        if self.forklift_level == "buttom-1" or self.forklift_level == "buttom-0":
            time.sleep(7.5)
        if self.forklift_level == "mid-1" or self.forklift_level == "mid-0":
            time.sleep(4)
        keyboard.release("l")
        self.forklift_level = "top-1"
        print("Level arrangement done! (top-1)")
        time.sleep(1)

    def dropping_stuff_top_0(self,keyboard):
        keyboard.press("k")
        time.sleep(1)
        keyboard.release("k")
        self.forklift_level = "top-0"
        print("Level arrangement done! (mid-0)")
        time.sleep(1)

    def going_forward_to_shelf(self,keyboard):
        time.sleep(0.1)
        keyboard.release(Key.space)
        saniye = float(6)
        t_end = time.time() + saniye
        while time.time() < t_end:
            keyboard.press(Key.up)
            time.sleep(0.1)
            keyboard.release(Key.up)
        keyboard.press(Key.space)
        time.sleep(1)
        
    def going_backward_to_road(self,keyboard):
        time.sleep(0.1)
        keyboard.release(Key.space)
        saniye = float(5)
        t_end = time.time() + saniye
        while time.time() < t_end:
            keyboard.press(Key.down)
            time.sleep(0.1)
            keyboard.release(Key.down)
        keyboard.press(Key.space)
        time.sleep(1)
    
    def stock_arrangement_buttom_shelf(self):
        if self.carrying is "company_1":
            self.stock[0][0] = 1
        elif self.carrying is "company_2":
            self.stock[1][0] = 1
        elif self.carrying is "company_3":
            self.stock[2][0] = 1
        print("Stock has been arranged!")
        print(self.stock)

    def stock_arrangement_mid_shelf(self):
        if self.carrying is "company_1":
            self.stock[0][1] = 1
        elif self.carrying is "company_2":
            self.stock[1][1] = 1
        elif self.carrying is "company_3":
            self.stock[2][1] = 1
        print("Stock has been arranged!")
        print(self.stock)
    
    def stock_arrangement_top_shelf(self):
        if self.carrying is "company_1":
            self.stock[0][2] = 1
        elif self.carrying is "company_2":
            self.stock[1][2] = 1
        elif self.carrying is "company_3":
            self.stock[2][2] = 1
        print("Stock has been arranged!")
        print(self.stock)
    
    def placing_stuff_to_buttom_shelf(self,keyboard):
        #alta yerleştirme
        self.putting_stuff_buttom_1(keyboard)
        self.going_forward_to_shelf(keyboard)
        self.dropping_stuff_buttom_0(keyboard)
        self.going_backward_to_road(keyboard)
        self.lane_tracing_activating(keyboard)
        self.lift_level_default_arranging(keyboard)
        self.stock_arrangement_buttom_shelf()
        self.carrying = "none"
        keyboard.release(Key.space)
    
    def placing_stuff_to_mid_shelf(self,keyboard):
        #ortaya yerleştirme
        self.putting_stuff_mid_1(keyboard)
        self.going_forward_to_shelf(keyboard)
        self.dropping_stuff_mid_0(keyboard)
        self.going_backward_to_road(keyboard)
        self.lane_tracing_activating(keyboard)
        self.lift_level_default_arranging(keyboard)
        self.stock_arrangement_mid_shelf()
        self.carrying = "none"
        keyboard.release(Key.space)

    def placing_stuff_to_top_shelf(self,keyboard):
        #üste yerleştirme
        self.putting_stuff_top_1(keyboard)
        self.going_forward_to_shelf(keyboard)
        self.dropping_stuff_top_0(keyboard)
        self.going_backward_to_road(keyboard)
        self.lane_tracing_activating(keyboard)
        self.lift_level_default_arranging(keyboard)
        self.stock_arrangement_top_shelf
        self.carrying = "none"
        keyboard.release(Key.space)

    def placing_function(self,keyboard):
        if self.carrying is "company_1" and self.stock[0][0] == 0:
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying is "company_1" and self.stock[0][1] == 0:
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying is "company_1" and self.stock[0][2] == 0:
            self.placing_stuff_to_top_shelf(keyboard)

        if self.carrying is "company_2" and self.stock[1][0] == 0:
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying is "company_2" and self.stock[1][1] == 0:
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying is "company_2" and self.stock[1][2] == 0:
            self.placing_stuff_to_top_shelf(keyboard)

        if self.carrying is "company_3" and self.stock[2][0] == 0:
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying is "company_3" and self.stock[2][1] == 0:
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying is "company_3" and self.stock[2][2] == 0:
            self.placing_stuff_to_top_shelf(keyboard)
        self.placing_done = True
    
    def going_forward_to_stuff(self,keyboard):
        time.sleep(0.1)
        keyboard.release(Key.space)
        saniye = float(6)
        t_end = time.time() + saniye
        while time.time() < t_end:
            keyboard.press(Key.up)
            time.sleep(0.1)
            keyboard.release(Key.up)
        keyboard.press(Key.space)
        time.sleep(1)
    
    def picking_stuff_from_the_ground(self,keyboard):
        self.lift_level_buttom_arranging(keyboard)
        self.going_forward_to_stuff(keyboard)
        self.lift_level_default_arranging(keyboard)
        self.going_backward_to_road(keyboard)
        self.turn_back(keyboard)

    def simulationFunction(self):
        keyboard = Controller()
        self.set_pos()
        self.middle_line = int((self.h - self.y)/2)
        time.sleep(2)
        camera_processing = CameraProcessing()
        count=0
        while(True):
            frame_of_cam = ImageGrab.grab((self.x, self.y, self.w, self.h))
            count += 1
            """if count == 1:
                self.going_backward_to_road(keyboard)"""
            if count % 25 == 0:
                print(self.carrying," - ",self.searching_lane)
                print(self.carrying," - ",self.searching_lane,"is_placing: ",self.is_placing," is_gathering: ",self.is_gathering)
            #PLACING 
            if self.is_placing is True and self.is_gathering is False:
                if self.carrying is not "none":
                    if self.carrying == "company_1":
                        self.searching_lane = "yellow"
                    elif self.carrying == "company_2":
                        self.searching_lane = "red"
                    elif self.carrying == "company_3":
                        self.searching_lane = "white"
                self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,False,True)
            #GATHERING
            elif self.is_placing is False and self.is_gathering is True:
                if self.gathering_stuff_searching_lane == "yellow":
                    self.searching_lane = "yellow"
                elif self.gathering_stuff_searching_lane == "red":
                    self.searching_lane = "red"
                elif self.gathering_stuff_searching_lane == "white":
                    self.searching_lane = "white"
                
                if self.searching_lane == "yellow":
                    self.carrying = "company_1"
                elif self.searching_lane == "red":
                    self.carrying = "company_2"
                elif self.searching_lane == "white":
                    self.carrying = "company_3"
                self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation  = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,True,False)
            #PLACING OPERATION
            elif self.dropping_stuff is True:
                self.placing_function(keyboard)
            #GATHERING OPERATION
            elif self.gathering_stuff is True:
                print("gathering_stuff")
                self.placing_done = False

            if self.switch_operation is True:
                if self.is_gathering is True:
                    self.is_placing = True
                    self.is_gathering = False
                else:
                    self.is_placing = False
                    self.is_gathering = True
                    self.gathering_stuff_searching_lane = "white"
            
            """#önce sarı sonra ordan diger sarıya geçti döndü beyaza gitti döndü yine beyaza gitti ama gather ve place tutuyor!
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER BAŞLANGICI
            if self.lane_position == -1000:
                print("Green lane detected!!")
                self.brake(keyboard)
                if self.is_placing is True:
                    self.placing_function(keyboard)
                    time.sleep(0.2)
                    keyboard.release(Key.space)
            else:
                #print ("Forward:{} Left:{} Right:{} Lane Position:{}".format(self.forward, self.left, self.right,self.lane_position))
                keyboard.press(Key.up)
                if self.error is True:
                    if count % 20 == 0:
                        print("Searching lane couldnt be detected!!")
                    keyboard.release(Key.right)
                    keyboard.release(Key.left)
                    keyboard.release(Key.up)
                elif self.forward is True:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)
                    #print("Go forward!")
                elif self.left is True:
                    keyboard.release(Key.right)
                    #print("Go left!")
                    keyboard.press(Key.left)
                elif self.right is True:
                    keyboard.release(Key.left)
                    #print("Go right!")
                    keyboard.press(Key.right)
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER SONU"""
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        keyboard.release('w')
mySim = SimulationProcessing()
mySim.simulationFunction()