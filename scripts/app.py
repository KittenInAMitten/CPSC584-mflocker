from flask import Flask, render_template, jsonify, request
# from picrawler import Picrawler
from time import sleep
import readchar
import threading

# Variables
# crawler = Picrawler() 
speed = 70

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

def show_info():
	# print("\033[H\033[J",end='')  # clear terminal windows 
	print(manual)


def move_forward():
	# crawler.do_action('forward',1,speed)
	print("Moved forward")
	show_info()
	return
    
def move_backward():
	# crawler.do_action('backward',1,speed)
	print("Moved backward")
	show_info()
	return
    
def turn_left():
	# crawler.do_action('turn left',1,speed)
	print("Turned left")
	show_info()
	return
    
def turn_right():
	# crawler.do_action('turn right',1,speed)
	print("Turned right")
	show_info()
	return

def tilt_up():
	# crawler.do_action('look up',1,speed)
	print("Tilted up")
	show_info()
	return

def tilt_down():
	# crawler.do_action('look down',1,speed)
	print("Tilted down")
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    # show_info()
    print(f"Received command: {data['action']}")
    if data['action'] == "forward":
        move_forward()
    elif data['action'] == "backward":
        move_backward()
    elif data['action'] == "left":
        turn_left()
    elif data['action'] == "right":
        turn_right()
    elif data['action'] == "tilt_up":
        tilt_up()
    elif data['action'] == "tilt_down":
        tilt_down()
    # show_info()  
    return jsonify({"status": "success", "action": data['action']})

@app.route('/video_feed')
def video_feed():
    print("video started")
    # return Vilib.display()

if __name__ == '__main__':
    # control_thread = threading.Thread(target=main_loop, daemon=True)
    # control_thread.start()
    
    # Vilib.camera_start()
    # Vilib.display()
    # Vilib.color_detect("red") 
    print("Camera started")

    app.run(debug=True, host='0.0.0.0')
    
