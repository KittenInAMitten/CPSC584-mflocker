from flask import Flask, render_template, jsonify, request
# from picrawler import Picrawler
import time
from time import sleep
import readchar
import threading
import socket


# Variables
# crawler = Picrawler() 
speed = 60
tilt_value = 0
in_action = False
waiting = False
start_time = 0
last_time = 0
current_detection = [0, 0, 0]

# Debug variables
KEYBOARD_MODE = True
    

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

'''
# def show_info():
#     # print("\033[H\033[J",end='')  # clear terminal windows 
#     print(manual)


# def move_forward():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
#     in_action = True
#     tilt_value = 0
#     crawler.do_action('forward',1,speed)
#     crawler.do_action('stand', speed)
#     print("Moved forward")
#     show_info()
#     in_action = False
#     return
    
# def move_backward():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
#     in_action = True
#     tilt_value = 0
#     crawler.do_action('backward',1,speed)
#     crawler.do_action('stand', speed)
#     print("Moved backward")
#     show_info()
#     in_action = False
#     return
    
# def turn_left():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
#     in_action = True
#     tilt_value = 0
#     crawler.do_action('turn left',1,speed)
#     crawler.do_action('stand', speed)
#     print("Turned left")
#     show_info()
#     in_action = False
#     return
    
# def turn_right():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
    
#     in_action = True
#     tilt_value = 0
#     crawler.do_action('turn right',1,speed)
#     crawler.do_action('stand', speed)
#     print("Turned right")
#     show_info()
#     in_action = False
#     return

# def tilt_up():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
    
#     in_action = True
#     if tilt_value < 25:
#         tilt_value += 5
        
#     coords = [
#         # stand
#         [[45, 45, (-50 - tilt_value)], [45, 45, (-50 - tilt_value)], [45, 45, (-50 + tilt_value)], [45, 45, (-50 + tilt_value)]]
#     ]
#     for coord in coords:
#         crawler.do_step(coord, 60)
#     show_info()
#     in_action = False
#     return
#     # crawler.do_action('look up',1,speed)
#     # print("Tilted up")
#     # show_info()
#     # return

# def tilt_down():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
#     in_action = True
    
#     if tilt_value > -25:
#         tilt_value -= 5
#     coords = [
#         # stand
#         [[45, 45, (-50 - tilt_value)], [45, 45, (-50 - tilt_value)], [45, 45, (-50 + tilt_value)], [45, 45, (-50 + tilt_value)]]
#     ]
#     for coord in coords:
#         crawler.do_step(coord, 60)
#     in_action = False
#     return

#     # crawler.do_action('look down',1,speed)
#     # print("Tilted down")
#     # return
 
# def stand():
#     global tilt_value
#     global in_action
#     if in_action:
#         return
#     in_action = True
#     crawler.do_action("stand", speed=60)
#     # coords = [
#     #     # stand
#     #     [[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
#     #     [[45, 45, -75], [45, 45, -75], [45, 45, -35], [45, 45, -35]],
#     # ]
#     # for coord in coords:
#     #     crawler.do_step(coord, 60)
#     in_action = False
#     return

def lock_pos():
    # global in_action
    # if in_action:
    #     return
    # print('test')
    # # coords = crawler.current_step_all_leg_value()
    # # print(coords)
    # for coord in [coords]:
    #     # crawler.do_step(coord, 60)
    #     # print(coord)
    return

def main_loop(): 

    # Vilib.camera_start()
    # Vilib.display()
    # Vilib.color_detect("red")
    print("is happening")
    show_info()   
    if(KEYBOARD_MODE):
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsad'):
                if 'w' == key:
                    move_forward()   
                elif 's' == key:
                    move_backward()         
                elif 'a' == key:
                    turn_left()          
                elif 'd' == key:
                    turn_right()
                elif 'r' == key:
                    tilt_up()
                elif 'f' == key:
                    tilt_down()
                sleep(0.05)
                show_info()  

            elif key == readchar.key.CTRL_C:
                print("\n Quit") 
                break    
            
            sleep(0.02)          

'''

app = Flask(__name__)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    global waiting
    global start_time
    global last_time
    data = request.json
    # show_info()
    # if data['action'] != "lock": 
    if waiting == False:
        start_time = time.time()
        print(f"Received command: {data['action']}")
        waiting = True
        if data['action'] == "forward":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # move_forward()
        elif data['action'] == "backward":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # move_backward()
        elif data['action'] == "left":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # turn_left()
        elif data['action'] == "right":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # turn_right()
        elif data['action'] == "tilt_up":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # tilt_up()
        elif data['action'] == "tilt_down":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
        elif data['action'] == "setAutomatic":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
        elif data['action'] == "setManual":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
        elif data['action'] == "blank":
            clientsocket.send(bytes(data['action'], 'UTF-8'))
            # tilt_down()
        # elif data['action'] == "lock":
        #     lock_pos()
        # show_info()  
        sleep(0.5)
        while waiting:
            buf = clientsocket.recv(64)
            reply = buf.decode('utf-8')
            if len(buf) > 0:
                if reply == 'ok':
                    waiting = False
                    break
        print(current_detection)
        
    else:
        last_time = time.time()
        if last_time - start_time > 1.5:
            waiting = False
    
    return jsonify({"status": "success", "action": data['action']})

@app.route('/video_feed')
def video_feed():
    print("video started")
    # return Vilib.display()
    return "http://172.17.10.168:9000/mjpg"

if __name__ == '__main__':
    # control_thread = threading.Thread(target=main_loop, daemon=True)
    # control_thread.start()
    
    # Vilib.camera_start()
    # Vilib.display(local=False, web=False)
    # Vilib.color_detect("red") 
    # print("Camera started")
    
    
    # crawler.do_action("stand", speed=60)
    app.run(debug=True, host='0.0.0.0')
    
    