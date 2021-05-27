import numpy as np
import cv2
import time
from cameraProcessing import CameraProcessing
from cameraProcessing_2 import CameraProcessing_2
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
        self.searching_lane = "none"
        #Leaving stuff - True-False
        self.dropping_stuff = False
        #Finding stuff - True-False
        self.gathering_stuff = False
        #Finding stuff flag - True-False
        self.gathering_stuff_flag = False
        #Gathering stuff searching lane - True-False
        self.gathering_stuff_searching_lane = "white"
        #forklift level Default - bottom-1 - buttom-0 - mid-1 - mid-0 - top-1 - top-0
        self.forklift_level = "Default"
        #stock first(0. index) is bottom, last(2. index) is top
        self.stock = [["Empty","Empty","Empty"],["Empty","Empty","Empty"],["Empty","Empty","Empty"]]
        #the placing operation flag
        self.placing_done = False
        #the gathering operation flag
        self.gathering_done = False
        #the gathering and placing switch operation flag
        self.switch_operation = False
        #the gathering  operation
        self.is_gathering = True
        #the placing operation
        self.is_placing = False
        #object detected flag
        self.object_detected_flag = False
        #execution flag
        self.DL_flag = True
        #switch_count
        self.switch_count = 0
        #stuff to pick done flag
        self.stuff_exists = True
        #stock managing done flag
        self.arrangement_done = False
        #turning on DL- flag
        self.detect_for_picking = False
        self.loop_flag = False
        self.search_for_upper_box = False
        self.found_on_first_level = False
        self.found_on_second_level = False
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
        print('\n*Select first corner of the area of DL image')
        mouse_posX1, mouse_posY1 = self.click_coordinates()
        time.sleep(0.8)
        print('\n*Select second corner of the area of DL image')
        mouse_posX2, mouse_posY2 = self.click_coordinates()
        time.sleep(0.8)
        self.DL_x = int(mouse_posX1)
        self.DL_y = int(mouse_posY1)
        self.DL_w = int(mouse_posX2)
        self.DL_h = int(mouse_posY2)
        print("Second area has been set!(DL)")
 
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
        print("Lifting level arrangement of forklift has done! (Default)")
        time.sleep(1)
    
    def lift_level_buttom_arranging(self,keyboard):
        keyboard.press("f")
        time.sleep(4)
        keyboard.release("f")
        self.forklift_level = "buttom-0"
        print("Lifting level arrangement of forklift has done! (Buttom)")
        time.sleep(1)

    def lift_level_for_second_box_arranging(self,keyboard):
        keyboard.press("v")
        time.sleep(3)
        keyboard.release("v")
        self.forklift_level = "Default"
        print("Lifting level arrangement of forklift has done! (Level 2-for picking)")
        time.sleep(1)

    def turn_back(self,keyboard):
        keyboard.press("x")
        time.sleep(0.1)
        keyboard.release("x")
        time.sleep(7)
        """if self.gathering_stuff is True:
            self.gathering_stuff = False
            self.gathering_stuff_flag = False"""

    def brake(self,keyboard):
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        keyboard.release(Key.up)
        keyboard.press(Key.space)
    
    def making_child(self,keyboard):
        keyboard.press("p")
        time.sleep(0.1)
        keyboard.release("p")
    
    def unmaking_child(self,keyboard):
        keyboard.press("u")
        time.sleep(0.1)
        keyboard.release("u")

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
        print("Lifting level arrangement of forklift has done! (buttom-1)")
        time.sleep(1)

    def dropping_stuff_buttom_0(self,keyboard):
        keyboard.press("f")
        time.sleep(1)
        keyboard.release("f")
        self.forklift_level = "bottom-0"
        print("Lifting level arrangement of forklift has done! (buttom-0)")
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
        print("Lifting level arrangement of forklift has done! (mid-1)")
        time.sleep(1)

    def dropping_stuff_mid_0(self,keyboard):
        keyboard.press("h")
        time.sleep(1)
        keyboard.release("h")
        self.forklift_level = "mid-0"
        print("Lifting level arrangement of forklift has done! (mid-0)")
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
        print("Lifting level arrangement of forklift has done! (top-1)")
        time.sleep(1)

    def dropping_stuff_top_0(self,keyboard):
        keyboard.press("k")
        time.sleep(1)
        keyboard.release("k")
        self.forklift_level = "top-0"
        print("Lifting level arrangement of forklift has done! (mid-0)")
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
        saniye = float(4.5)
        t_end = time.time() + saniye
        while time.time() < t_end:
            keyboard.press(Key.down)
            time.sleep(0.1)
            keyboard.release(Key.down)
        keyboard.press(Key.space)
        time.sleep(1)

    def stock_arrangement_buttom_shelf(self):
        if self.carrying == "company_1":
            self.stock[0][0] = "Full"
        elif self.carrying == "company_2":
            self.stock[1][0] = "Full"
        elif self.carrying == "company_3":
            self.stock[2][0] = "Full"
        print("**Stock has been arranged!")
        self.print_stock()

    def stock_arrangement_mid_shelf(self):
        if self.carrying == "company_1":
            self.stock[0][1] = "Full"
        elif self.carrying == "company_2":
            self.stock[1][1] = "Full"
        elif self.carrying == "company_3":
            self.stock[2][1] = "Full"
        print("**Stock has been arranged!")
        self.print_stock()
    
    def stock_arrangement_top_shelf(self):
        if self.carrying == "company_1":
            self.stock[0][2] = "Full"
        elif self.carrying == "company_2":
            self.stock[1][2] = "Full"
        elif self.carrying == "company_3":
            self.stock[2][2] = "Full"
        print("**Stock has been arranged!")
        self.print_stock()
    
    def print_stock(self):
        print("-Company_1 - Bottom shelf:",self.stock[0][0],", Mid shelf:",self.stock[0][1],", Top shelf:",self.stock[0][2])
        print("-Company_2 - Bottom shelf:",self.stock[1][0],", Mid shelf:",self.stock[1][1],", Top shelf: ",self.stock[1][2])
        print("-Company_3 - Bottom shelf:",self.stock[2][0],", Mid shelf:",self.stock[2][1],", Top shelf: ",self.stock[2][2])

    def check_stock(self):
        if self.searching_lane == "yellow":
            if self.stock[0][0] == "Full" and self.stock[0][1] == "Full" and self.stock[0][2] == "Full":
                self.searching_lane = "red"
        if self.searching_lane == "red":
            if self.stock[1][0] == "Full" and self.stock[1][1] == "Full" and self.stock[1][2] == "Full":
                self.searching_lane = "white"
        if self.searching_lane == "white":
            if self.stock[2][0] == "Full" and self.stock[2][1] == "Full" and self.stock[2][2] == "Full":
                self.searching_lane = "none"
                print("All shelves are full!!")
                
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
        self.stock_arrangement_top_shelf()
        self.carrying = "none"
        keyboard.release(Key.space)

    def placing_function(self,keyboard):
        self.unmaking_child(keyboard)
        if self.carrying == "company_1" and self.stock[0][0] == "Empty":
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying == "company_1" and self.stock[0][1] == "Empty":
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying == "company_1" and self.stock[0][2] == "Empty":
            self.placing_stuff_to_top_shelf(keyboard)

        if self.carrying == "company_2" and self.stock[1][0] == "Empty":
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying == "company_2" and self.stock[1][1] == "Empty":
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying == "company_2" and self.stock[1][2] == "Empty":
            self.placing_stuff_to_top_shelf(keyboard)

        if self.carrying == "company_3" and self.stock[2][0] == "Empty":
            self.placing_stuff_to_buttom_shelf(keyboard)
        elif self.carrying == "company_3" and self.stock[2][1] == "Empty":
            self.placing_stuff_to_mid_shelf(keyboard)
        elif self.carrying == "company_3" and self.stock[2][2] == "Empty":
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
        self.making_child(keyboard)
        self.turn_back(keyboard)
    
    def picking_stuff_from_the_second_level(self,keyboard):
        self.lift_level_for_second_box_arranging(keyboard)
        self.going_forward_to_stuff(keyboard)
        self.lift_level_default_arranging(keyboard)
        self.going_backward_to_road(keyboard)
        self.making_child(keyboard)
        self.turn_back(keyboard)

    def simulationFunction(self):
        keyboard = Controller()
        self.set_pos()
        self.middle_line = int((self.h - self.y)/2)
        time.sleep(2)
        camera_processing = CameraProcessing()
        count=0
        while(True):
            frame_of_DL_cam = ImageGrab.grab((self.DL_x, self.DL_y, self.DL_w, self.DL_h))
            frame_of_cam = ImageGrab.grab((self.x, self.y, self.w, self.h))
            if count % 150 == 0:
                print("Carrying -",self.carrying,", is_placing: ",self.is_placing,", is_gathering: ",self.is_gathering)
            #PLACING 
            if self.is_placing is True and self.is_gathering is False:
                self.object_detected_flag = False
                if self.carrying != "none":
                    if self.carrying == "company_1":
                        self.searching_lane = "yellow"
                    elif self.carrying == "company_2":
                        self.searching_lane = "red"
                    elif self.carrying == "company_3":
                        self.searching_lane = "white"
                self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,False,True,self.gathering_done,self.placing_done)
                self.placing_done = False
            #GATHERING
            elif self.is_placing is False and self.is_gathering is True:
                if self.DL_flag is True:
                    image_np = np.array(frame_of_DL_cam)
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)

                    # Things to try:
                    # Flip horizontally
                    # image_np = np.fliplr(image_np).copy()

                    # Convert image to grayscale
                    # image_np = np.tile(
                    #     np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

                    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
                    detections, predictions_dict, shapes = detect_fn(input_tensor)

                    label_id_offset = 1
                    image_np_with_detections = image_np.copy()
                    image_np_with_detections = cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB)
                    
                    img, obj_detected = viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections,
                        detections['detection_boxes'][0].numpy(),
                        (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
                        detections['detection_scores'][0].numpy(),
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=500,
                        min_score_thresh=.60,
                        agnostic_mode=False)
                    for n in range(len(obj_detected)):
                        #print(obj_detected[n][1],int((self.DL_h-self.DL_y)/2))
                        if self.object_detected_flag is False:
                            if (obj_detected[n][4] >= ((self.DL_h-self.DL_y) - int((self.DL_h-self.DL_y)/20)) ) and ( (obj_detected[n][1] <= int((self.DL_w-self.DL_x)/2)) and obj_detected[n][3] >= int((self.DL_w-self.DL_x)/2) ):
                                self.brake(keyboard)
                                time.sleep(1)
                                self.object_detected_flag = True
                                print(obj_detected[n][0],"is being gathered!")
                                self.picking_stuff_from_the_ground(keyboard)
                                self.gathering_done = True
                                time.sleep(0.1)
                                keyboard.release(Key.space)
                                self.carrying = obj_detected[n][0]
                                self.DL_flag = False
                    # Display output
                    cv2.imshow('object detection', image_np_with_detections)
                if self.switch_count >= 0 and self.switch_count < 3:
                    self.gathering_stuff_searching_lane = "white"
                elif  self.switch_count >= 3 and self.switch_count < 6:
                    self.gathering_stuff_searching_lane = "red"
                elif  self.switch_count >= 6 and self.switch_count < 9:
                    self.gathering_stuff_searching_lane = "yellow"
                else:
                    self.stuff_exists = False

                if self.gathering_stuff_searching_lane == "yellow":
                    self.searching_lane = "yellow"
                elif self.gathering_stuff_searching_lane == "red":
                    self.searching_lane = "red"
                elif self.gathering_stuff_searching_lane == "white":
                    self.searching_lane = "white"
                self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation  = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,True,False,self.gathering_done,self.placing_done)
                self.gathering_done = False
            
            if self.stuff_exists ==  False:
                self.brake(keyboard)
            if self.switch_operation is True:
                if self.is_gathering is True:
                    self.switch_count += 1
                    self.is_placing = True
                    self.is_gathering = False
                else:
                    self.is_placing = False
                    self.is_gathering = True
                    self.brake(keyboard)
                    time.sleep(2.5)
                    keyboard.release(Key.space)
                    self.DL_flag = True
            
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER BAŞLANGICI
            if self.lane_position == -1000:
                print("Green lane detected in the middle!!")
                self.brake(keyboard)
                if self.is_placing is True:
                    self.placing_function(keyboard)
                    time.sleep(0.2)
                    keyboard.release(Key.space)
            else:
                #print ("Forward:{} Left:{} Right:{} Lane Position:{}".format(self.forward, self.left, self.right,self.lane_position))
                keyboard.press(Key.up)
                if self.error is True:
                    #print("Searching lane couldnt be detected!!")
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
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER SONU
            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        keyboard.release(Key.right)
        keyboard.release(Key.left)
        keyboard.release(Key.up)

    def simulationFunction_2(self):
        keyboard = Controller()
        self.set_pos()
        self.middle_line = int((self.h - self.y)/2)
        time.sleep(2)
        camera_processing = CameraProcessing()
        count=0
        while(True):
            frame_of_DL_cam = ImageGrab.grab((self.DL_x, self.DL_y, self.DL_w, self.DL_h))
            frame_of_cam = ImageGrab.grab((self.x, self.y, self.w, self.h))
            self.loop_flag = False
            if count % 150 == 0:
                if self.searching_lane == "yellow":
                    print("Managing 'company_1' , is_placing: ",self.is_placing,", is_gathering: ",self.is_gathering)
                if self.searching_lane == "red":
                    print("Managing 'company_2' , is_placing: ",self.is_placing,", is_gathering: ",self.is_gathering)
                if self.searching_lane == "white":
                    print("Managing 'company_3' , is_placing: ",self.is_placing,", is_gathering: ",self.is_gathering)
            #PLACING 
            if self.is_placing is True and self.is_gathering is False:
                self.object_detected_flag = False
                if self.DL_flag is True:
                    self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,False,True,self.gathering_done,self.placing_done)
                    self.placing_done = False
            #GATHERING
            elif self.is_placing is False and self.is_gathering is True:
                self.forward, self.left, self.right,self.error, self.lane_position,self.switch_operation  = camera_processing.capturingFunction(np.array(frame_of_cam),self.searching_lane,True,False,self.gathering_done,self.placing_done)
                self.gathering_done = False
            
            if self.DL_flag is False or self.detect_for_picking is True:
                image_np = np.array(frame_of_DL_cam)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)

                # Things to try:
                # Flip horizontally
                # image_np = np.fliplr(image_np).copy()

                # Convert image to grayscale
                # image_np = np.tile(
                #     np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

                input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
                detections, predictions_dict, shapes = detect_fn(input_tensor)

                label_id_offset = 1
                image_np_with_detections = image_np.copy()
                image_np_with_detections = cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB)
                
                img, obj_detected = viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'][0].numpy(),
                    (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
                    detections['detection_scores'][0].numpy(),
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=500,
                    min_score_thresh=.60,
                    agnostic_mode=False)
                
                if self.is_placing == True:
                    for n in range(len(obj_detected)):
                        if int((self.DL_w-self.DL_x)/3) <= int((obj_detected[n][1] + obj_detected[n][3])/2) <= int(((self.DL_w-self.DL_x)/3)*2):
                            if int((self.DL_h-self.DL_y)/2) <= int((obj_detected[n][2] + obj_detected[n][4])/2) <= (self.DL_h-self.DL_y):
                                if self.searching_lane == "yellow":
                                    self.stock[0][0] = "Full"
                                elif self.searching_lane == "red":
                                    self.stock[1][0] = "Full"
                                elif self.searching_lane == "white":
                                    self.stock[2][0] = "Full"
                            elif int((self.DL_h-self.DL_y)/4) <= int((obj_detected[n][2] + obj_detected[n][4])/2) <= int((self.DL_h-self.DL_y)/2):
                                if self.searching_lane == "yellow":
                                    self.stock[0][1] = "Full"
                                elif self.searching_lane == "red":
                                    self.stock[1][1] = "Full"
                                elif self.searching_lane == "white":
                                    self.stock[2][1] = "Full"
                            elif 0 <= int((obj_detected[0][2] + obj_detected[n][4])/2) <= int((self.DL_h-self.DL_y)/4):
                                if self.searching_lane == "yellow":
                                    self.stock[0][2] = "Full"
                                elif self.searching_lane == "red":
                                    self.stock[1][2] = "Full"
                                elif self.searching_lane == "white":
                                    self.stock[2][2] = "Full"
                    self.print_stock()
                    self.placing_done = True
                    self.turn_back(keyboard)
                    keyboard.release(Key.space)
                if self.detect_for_picking == True:
                    bottom_box_area = 0
                    box_area = 0
                    y2_of_close_obj = 0
                    will_be_taken = ""
                    for n in range(len(obj_detected)):
                        if (obj_detected[n][4] >= ((self.DL_h-self.DL_y) - int((self.DL_h-self.DL_y)/20)) ) and ( (obj_detected[n][1] <= int((self.DL_w-self.DL_x)/2)) and obj_detected[n][3] >= int((self.DL_w-self.DL_x)/2) ):
                            bottom_box_area = int((obj_detected[n][4] - obj_detected[n][2]) * (obj_detected[n][3] - obj_detected[n][1]))
                            y2_of_close_obj =  obj_detected[n][4]
                            will_be_taken = obj_detected[n][0]
                            self.brake(keyboard)
                            self.search_for_upper_box = True
                            self.found_on_first_level = True
                            self.found_on_second_level = False
                            break
                    if self.search_for_upper_box == True:
                        img, obj_detected = viz_utils.visualize_boxes_and_labels_on_image_array(
                            image_np_with_detections,
                            detections['detection_boxes'][0].numpy(),
                            (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
                            detections['detection_scores'][0].numpy(),
                            category_index,
                            use_normalized_coordinates=True,
                            max_boxes_to_draw=500,
                            min_score_thresh=.60,
                            agnostic_mode=False)
                        for n in range(len(obj_detected)):
                            if ( (obj_detected[n][1] <= int((self.DL_w-self.DL_x)/2)) and (obj_detected[n][3] >= int((self.DL_w-self.DL_x)/2)) ) and (obj_detected[n][4] < y2_of_close_obj):  
                                box_area = int((obj_detected[n][4] - obj_detected[n][2]) * (obj_detected[n][3] - obj_detected[n][1]))
                                if box_area >= int((bottom_box_area)*9/10):
                                    self.found_on_second_level = True
                                    print(obj_detected[n][0],"is being gathered!")
                                    self.carrying = obj_detected[n][0].lower()
                                    self.picking_stuff_from_the_second_level(keyboard)
                                    self.search_for_upper_box = False
                                    self.detect_for_picking = False
                                    self.gathering_done = True
                                    time.sleep(0.1)
                                    keyboard.release(Key.space)
                                    break

                    if self.found_on_second_level == False and self.found_on_first_level == True:
                        self.object_detected_flag = True
                        print(will_be_taken,"is being gathered!")
                        self.carrying = will_be_taken.lower()
                        self.picking_stuff_from_the_ground(keyboard)
                        self.gathering_done = True
                        time.sleep(0.1)
                        keyboard.release(Key.space)
                        self.detect_for_picking = False
                        self.found_on_first_level = False
                        self.search_for_upper_box = False
                
                # Display output
                cv2.imshow('object detection', image_np_with_detections)
                
                self.DL_flag = True
                #self.check_stock()
                self.lane_position = 0
            
            if self.switch_operation is True:
                if self.is_gathering is True:
                    self.switch_count += 1
                    self.is_placing = True
                    self.is_gathering = False
                    self.DL_flag = True
                else:
                    self.brake(keyboard)
                    time.sleep(2.5)
                    if self.searching_lane == "yellow":
                        if self.stock[0][0] == "Full" and self.stock[0][1] == "Full" and self.stock[0][2] == "Full":
                            self.searching_lane = "red"
                            self.loop_flag = True
                            self.turn_back(keyboard)
                            keyboard.release(Key.space)
                    elif self.searching_lane == "red":
                        if self.stock[1][0] == "Full" and self.stock[1][1] == "Full" and self.stock[1][2] == "Full":
                            self.searching_lane = "white"
                            self.loop_flag = True
                            self.turn_back(keyboard)
                            keyboard.release(Key.space)
                    elif self.searching_lane == "white":
                        if self.stock[2][0] == "Full" and self.stock[2][1] == "Full" and self.stock[2][2] == "Full":
                            self.searching_lane = "none"
                            print("Shelves are FULL!")
                    
                    if self.loop_flag == False:
                        self.is_placing = False
                        self.is_gathering = True
                        self.detect_for_picking = True
                        keyboard.release(Key.space)

            
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER BAŞLANGICI
            if self.lane_position == -1000 and self.DL_flag == True:
                print("Green lane detected in the middle!!")
                if self.carrying == "none":
                    self.DL_flag = False
                    self.brake(keyboard)
                    time.sleep(0.2)
                    self.going_backward_to_road(keyboard)
                    self.brake(keyboard)
                else:
                    self.brake(keyboard)
                    time.sleep(0.2)
                    self.placing_function(keyboard)
            else:
                #print ("Forward:{} Left:{} Right:{} Lane Position:{}".format(self.forward, self.left, self.right,self.lane_position))
                keyboard.press(Key.up)
                if self.error is True:
                    #print("Searching lane couldnt be detected!!")
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
            #GELEN VERİLERE GÖRE ARACI HAREKET ETTİRDİĞİMİZ YER SONU

            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        keyboard.release(Key.up)
        keyboard.release(Key.left)
        keyboard.release(Key.right)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)

# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file("exported-models/my_model_frcnn_resnet50_v1_RVH_RFH_4Batches/pipeline.config")
model_config = configs['model']
detection_model = model_builder.build(model_config=model_config, is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join("exported-models/my_model_frcnn_resnet50_v1_RVH_RFH_4Batches/checkpoint", 'ckpt-0')).expect_partial()

@tf.function
def detect_fn(image):
    """Detect objects in image."""

    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])

category_index = label_map_util.create_category_index_from_labelmap("annotations/label_map.pbtxt",
                                                                    use_display_name=True)

print("**Running Types**\n1-Filling the shelves\n2-Detect and fill the shelves")
run_type = int(input("Which type would you like to run with(1/2) :"))
if run_type == 1:    
    mySim = SimulationProcessing()
    mySim.simulationFunction()
elif run_type == 2:
    mySim = SimulationProcessing()
    mySim.simulationFunction_2()