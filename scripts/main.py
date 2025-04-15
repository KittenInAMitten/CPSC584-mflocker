from vilib import Vilib
from picrawler import Picrawler
from time import sleep
import socket
import os
import time

import cv2
import numpy as np

# Variables
crawler = Picrawler() 
speed = 60
tilt_value = 0
in_action = False

student_colors = ["green", "yellow", "blue"]

detected = [0,0,0]

last_time = 0

ALERT_MODE = False
MANUAL_MODE = True

# Debug variables
KEYBOARD_MODE = False
    

manual = '''
Press keys on keyboard to control PiCrawler!
    W: Forward
    A: Turn left
    S: Backward
    D: Turn right
    R: Tilt up
    F: Tilt down

    Ctrl^C: Quit
'''

def show_info():
    # print("\033[H\033[J",end='')  # clear terminal windows 
    # print(manual)
    return


def move_forward():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    tilt_value = 0
    crawler.do_action('forward',1,speed)
    # crawler.do_action('stand', speed)
    show_info()
    in_action = False
    return
    
def move_backward():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    tilt_value = 0
    crawler.do_action('backward',1,speed)
    # crawler.do_action('stand', speed)
    show_info()
    in_action = False
    return
    
def turn_left():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    tilt_value = 0
    crawler.do_action('turn left',1,speed)
    # crawler.do_action('stand', speed)
    show_info()
    in_action = False
    return
    
def turn_right():
    global tilt_value
    global in_action
    if in_action:
        return
    
    in_action = True
    tilt_value = 0
    crawler.do_action('turn right',1,speed)
    # crawler.do_action('stand', speed)
    show_info()
    in_action = False
    return

def tilt_up():
    global tilt_value
    global in_action
    if in_action:
        return
    
    in_action = True
    if tilt_value < 25:
        tilt_value += 5
        
    coords = [
        # stand
        [[45, 45, (-50 - tilt_value)], [45, 45, (-50 - tilt_value)], [45, 45, (-50 + tilt_value)], [45, 45, (-50 + tilt_value)]]
    ]
    for coord in coords:
        crawler.do_step(coord, 60)
    show_info()
    in_action = False
    return
    # crawler.do_action('look up',1,speed)
    # print("Tilted up")
    # show_info()
    # return

def tilt_down():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    
    if tilt_value > -25:
        tilt_value -= 5
    coords = [
        # stand
        [[45, 45, (-50 - tilt_value)], [45, 45, (-50 - tilt_value)], [45, 45, (-50 + tilt_value)], [45, 45, (-50 + tilt_value)]]
    ]
    for coord in coords:
        crawler.do_step(coord, 60)
    in_action = False
    return

    # crawler.do_action('look down',1,speed)
    # print("Tilted down")
    # return
 
def doNothing():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    coords = [
        # stand
        [[45, 45, (-50 - tilt_value)], [45, 45, (-50 - tilt_value)], [45, 45, (-50 + tilt_value)], [45, 45, (-50 + tilt_value)]]
    ]
    for coord in coords:
        crawler.do_step(coord, 60)
    sleep(0.05)
    in_action = False
    # else: 
    #     crawler.do_action("stand", speed=60)
    #     sleep(0.05)    
    #     in_action = False
    # coords = [
    #     # stand
    #     [[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
    #     [[45, 45, -75], [45, 45, -75], [45, 45, -35], [45, 45, -35]],
    # ]
    # for coord in coords:
    #     crawler.do_step(coord, 60)
    return

def followRed():
    global in_action
    Vilib.color_detect("red")
    if Vilib.detect_obj_parameter['color_n']!=0 and not in_action:
        coordinate_x = Vilib.detect_obj_parameter['color_x']
        in_action = True
        leftBounds = Vilib.camera_width * 0.25
        rightBounds = Vilib.camera_width * 0.75
        # if coordinate_x < 100:
        if coordinate_x < leftBounds:
            crawler.do_action('turn left',1,speed)
            sleep(0.05) 
        # elif coordinate_x > 220:
        elif coordinate_x > rightBounds:
            crawler.do_action('turn right',1,speed)
            sleep(0.05) 
        else :
            crawler.do_action('forward',2,speed)
            sleep(0.05)    
        in_action = False
    elif not in_action:
        in_action = True
        crawler.do_action('stand',speed)
        sleep(0.05)
        in_action = False
        
def takePicture():# ----- check path -----
    global last_time
    global in_action
    
    #check if time elapsed is 10 seconds, return if not
    if time.time() - last_time < 20 or in_action:
        return
    
    in_action = True
    #re-update time
    last_time = time.time()
    
    user_name = os.getlogin()
    path = f"/home/motherflocker/picrawler/custom/scripts/static/images"
    if not os.path.exists(path):
        # print('Path does not exist. Creating path now ... ')
        os.makedirs(name=path, mode=0o751, exist_ok=True)
        time.sleep(0.01) 

    # if status:
    #     print('The photo is saved as '+path+'/'+photo_name+'.jpg')
    # else:
    #     print('Photo save failed .. ')

    current_img = Vilib.img
    analyzePicture(current_img)
    
    count = 0
    for x in range(3): 
        if detected[x] == 1:
            # ----- save photo -----
            status = False
            for _ in range(5):
                if  current_img is not None:
                    status = cv2.imwrite(path + '/' + student_colors[x] +'.jpg', current_img)
                    break
                else:
                    time.sleep(0.01)
            else:
                status = False
            if status:
                print(path + '/' + student_colors[x] + '.jpg updated.')
            else:
                print(path + '/' + student_colors[x] + '.jpg not updated.')
        count = count + 1
    
    sleep(0.05)
    in_action = False
    return 

def analyzePicture(img):
    global detected
    color_dict = {
        'red':[[0, 8], [80, 255], [0, 255]],
        'orange':[[12, 18], [80, 255], [80, 255]],
        'yellow':[[20, 60], [60, 255], [120, 255]],
        'green':[[45, 85], [120, 255], [80, 255]],
        'blue':[[92,120], [120, 255], [80, 255]],
        'purple':[[115,155], [30, 255], [60, 255]],
        'magenta':[[160,180], [30, 255], [60, 255]],
    }
    
    for x in range(3):
        '''Define parameters for color detection object'''
        
        color_name = student_colors[x]
        
        # color_obj_parameter['color'] = color_name   
        
        # Reduce image for faster recognition 
        zoom = 4 # reduction ratio
        width_zoom = int(Vilib.camera_width / zoom)
        height_zoom = int(Vilib.camera_height / zoom)
        resize_img = cv2.resize(img, (width_zoom, height_zoom), interpolation=cv2.INTER_LINEAR)
        
        # Convert the image in BGR to HSV
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV) 
    
        # Set range for red color and define mask
        # color_lower = np.array([min(color_dict[color_name]), 60, 60])
        # color_upper = np.array([max(color_dict[color_name]), 255, 255])
        color_lower = np.array([min(color_dict[color_name][0]), min(color_dict[color_name][1]), min(color_dict[color_name][2])])
        color_upper = np.array([max(color_dict[color_name][0]), max(color_dict[color_name][1]), max(color_dict[color_name][2])])
        
        mask = cv2.inRange(hsv, color_lower, color_upper)

        if color_name == 'red':
            mask_2 = cv2.inRange(hsv, (167, 0, 0), (180, 255, 255))
            mask = cv2.bitwise_or(mask, mask_2)

        # define a 5*5 kernel
        kernel_5 = np.ones((5,5), np.uint8)

        # opening the image (erosion followed by dilation), to remove the image noise
        open_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_5, iterations=1)      

        # Find contours in binary image
        _tuple = cv2.findContours(open_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        # compatible with opencv3.x and openc4.x
        if len(_tuple) == 3:
            _, contours, hierarchy = _tuple
        else:
            contours, hierarchy = _tuple
        
        if(len(contours) > 0):
            detected[x] = 1
        else:
            detected[x] = 0
        

    
    return
        
# def checkForColors():
#     detection = [0, 0, 0]
#     for colorIndex in range(3):
#         Vilib.color_detect(student_colors[colorIndex])
#         Vilib.color_detect_work(Vilib.img, Vilib.camera_width, Vilib.camera_height, Vilib.color_detect_color)
#         print("Checking for Color: " + student_colors[colorIndex])
#         if Vilib.detect_obj_parameter['color_n']!=0:
#             print(' - found')
#             detection[colorIndex] = 1
#         else:
#             print(' - notfound')
#             detection[colorIndex] = 0
#     return detection
        
    

def main(): 

    Vilib.camera_start()
    Vilib.display(local=False,web=True)
    Vilib.color_detect("red") 
    
    global MANUAL_MODE
    global in_action
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(1) # become a server socket, maximum 5 connections

    print('Mother Flocker activated. Awaiting commands.')
    
    try:
        connection, address = serversocket.accept()
        while True:
            buf = connection.recv(64)
            command = buf.decode('utf-8')
            if len(buf) > 0:
                print('Received command:' + command)
                takePicture()
                if MANUAL_MODE:
                    if command == "forward":
                        move_forward()	
                    elif command == "backward":
                        move_backward()		 
                    elif command == "left":
                        turn_left()		  
                    elif command == "right":
                        turn_right()
                    elif command == "tilt_up":
                        tilt_up()
                    elif command == "tilt_down":
                        tilt_down()
                    elif command == "setAutomatic":
                        MANUAL_MODE = False
                    elif command == "blank":
                        doNothing()
                    # elif command == "take_picture":
                    #     takePicture()
                else:
                    if command == "setManual":
                        MANUAL_MODE = True
                        print("Manual Set")
                    elif command == "blank":
                        print("update")
                        followRed()
                connection.send(bytes('ok', 'UTF-8'))
                print(*detected, end="\t")
                sleep(0.05)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Error:\n {e}')
    finally:
        crawler.do_action("stand", speed=60)
        sleep(.1)		
'''    
    # try:
    #     show_info()	
    #     if(KEYBOARD_MODE):
    #         while True:
    #             key = readchar.readkey()
    #             key = key.lower()
    #             if key in('wsadrfg'):
    #                 if 'w' == key:
    #                     move_forward()	
    #                 elif 's' == key:
    #                     move_backward()		 
    #                 elif 'a' == key:
    #                     turn_left()		  
    #                 elif 'd' == key:
    #                     turn_right()
    #                 elif 'r' == key:
    #                     print("tilting up")
    #                     tilt_up()
    #                 elif 'f' == key:
    #                     print("tilting dow")
    #                     tilt_down()
    #                 elif 'g' == key:
    #                     print("standing")
    #                     stand()
    #                 sleep(0.05)
    #                 show_info()  

    #             elif key == readchar.key.CTRL_C:
    #                 print("\n Quit") 
    #                 break	
                
    #             sleep(0.02)  
    #     else:
    #         coords = crawler.move_list['stand']
    #         # print("Input [0-4] to select leg. Current coords:")
    #         last_key = None
    #         while True:
    #             print("Input [0-4] to select leg.")
    #             print(coords)
    #             key = input()

    #             if key == '':
    #                 # print(actions[last_key])
    #                 # actions_dict[actions[last_key]](my_spider)
                    
    #                 print("Input [0-4] to select leg.")
    #             else:
    #                 # key = String(key)
    #                 if key not in ["0", "1", "2", "3"]:
    #                     print("Invalid leg")
    #                 else:
    #                     last_key = int(key)
    #                     print("Input [X Y Z] to change orientation.")
    #                     s = input()
    #                     nums = list(map(int, s.split()))
    #                     coords = crawler.move_list['stand']
    #                     coords[0][last_key] = nums
    #                     print(coords)
    #                     for coord in coords:
    #                         crawler.do_step(coord, 60)

    #             # sleep(2)
    #             # wave_hand(my_spider)
    #             # shake_hand(my_spider)
    #             # fighting(my_spider)
    #             # excited(my_spider)
    #             # play_dead(my_spider)
    #             # relax_legs(my_spider)
    #             # nod(my_spider)
    #             # shake_head(my_spider)
    #             # look_left(my_spider)
    #             # look_right(my_spider)
    #             # look_up(my_spider)
    #             # look_down(my_spider)
    #             # warm_up(my_spider)
    #             # push_up(my_spider)

    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     print(f'Error:\n {e}')
    # finally:
    #     crawler.do_action("stand", speed=60)
    #     sleep(.1)		
    '''
 
if __name__ == "__main__":
    main()