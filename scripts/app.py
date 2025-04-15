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

# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
    global lastBlank
    global current_detection
    data = request.json
    
    
    # show_info()
    # if data['action'] != "lock": 
    if waiting == False:
        start_time = time.time()
        if data['action'] != 'blank':
            print(f"Received command: {data['action']}")
        waiting = True
        lastBlank = False
        clientsocket.send(bytes(data['action'], 'UTF-8'))
        
        sleep(0.5)
        while waiting:
            buf = clientsocket.recv(64)
            reply = buf.decode('utf-8')
            if len(buf) > 0:
                print(reply)
                parts = reply.split(" ")
                if len(parts) == 4:
                    for x in range(3):
                        if parts[x + 1].isnumeric():
                            current_detection[x] = int(parts[x + 1])
                if parts[0] == 'ok':
                    waiting = False
                    break
        
    else:
        last_time = time.time()
        if last_time - start_time > 1.5:
            waiting = False
    
    return jsonify({"status": "success", "action": data['action'], "students": ' '.join(str(x) for x in current_detection)})

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
    
    