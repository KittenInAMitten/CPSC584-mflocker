# from vilib import Vilib
from picrawler import Picrawler
from time import sleep
import readchar
import socket

# Variables
crawler = Picrawler() 
speed = 60
tilt_value = 0
in_action = False

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
    print("Moved forward")
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
    print("Moved backward")
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
    print("Turned left")
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
    print("Turned right")
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
 
def stand():
    global tilt_value
    global in_action
    if in_action:
        return
    in_action = True
    crawler.do_action("stand", speed=60)
    # coords = [
    #     # stand
    #     [[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
    #     [[45, 45, -75], [45, 45, -75], [45, 45, -35], [45, 45, -35]],
    # ]
    # for coord in coords:
    #     crawler.do_step(coord, 60)
    in_action = False
    return
    

def main(): 

    # Vilib.camera_start()
    # Vilib.display(local=False,web=True)
    # Vilib.color_detect("red") 
    
    global MANUAL_MODE
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    print('Mother Flocker activated. Awaiting commands.')
    
    try:
        connection, address = serversocket.accept()
        while True:
            buf = connection.recv(64)
            command = buf.decode('utf-8')
            if len(buf) > 0:
                print(command)
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
                        print("tilting up")
                        tilt_up()
                    elif command == "tilt_down":
                        print("tilting dow")
                        tilt_down()
                    elif command == "setAutomatic":
                        MANUAL_MODE = False
                        print("Automatic Set")
                    elif command == "setManual":
                        print("Manual Set")
                    elif command == "stand":
                        print("standing")
                        stand()
                else:
                    if command == "setManual":
                        MANUAL_MODE = True
                        print("Manual Set")
                    else:
                        print("check")
                        # INSERT BULL FIGHT CODE HERE
                connection.send(bytes('ok', 'UTF-8'))
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