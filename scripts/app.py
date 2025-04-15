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

lastBlank = False

# Debug variables
KEYBOARD_MODE = True

app = Flask(__name__)

# clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientsocket.connect(('localhost', 8089))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    global waiting
    global start_time
    global last_time
    global lastBlank
    data = request.json
    # show_info()
    # if data['action'] != "lock": 
    if waiting == False:
        start_time = time.time()
        if data['action'] != 'blank':
            print(f"Received command: {data['action']}")
        waiting = True
        lastBlank = False
        # clientsocket.send(bytes(data['action'], 'UTF-8'))
        
        # if data['action'] == "forward":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        #     # move_forward()
        # elif data['action'] == "backward":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        #     # move_backward()
        # elif data['action'] == "left":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        #     # turn_left()
        # elif data['action'] == "right":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        #     # turn_right()
        # elif data['action'] == "tilt_up":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        #     # tilt_up()
        # elif data['action'] == "tilt_down":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        # elif data['action'] == "setAutomatic":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        # elif data['action'] == "setManual":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        # elif data['action'] == "take_picture":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
        # elif data['action'] == "blank":
        #     clientsocket.send(bytes(data['action'], 'UTF-8'))
            # lastBlank = True
            # tilt_down()
        # elif data['action'] == "lock":
        #     lock_pos()
        # show_info()  
        sleep(0.5)
        # while waiting:
        #     buf = clientsocket.recv(64)
        #     reply = buf.decode('utf-8')
        #     if len(buf) > 0:
        #         print(reply)
        #         if reply == 'ok':
        #             waiting = False
        #             break
        
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
    
    