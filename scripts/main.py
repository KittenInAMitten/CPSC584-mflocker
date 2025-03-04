from picrawler import Picrawler
from time import sleep
import readchar

# Variables
crawler = Picrawler() 
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
	print("\033[H\033[J",end='')  # clear terminal windows 
	print(manual)


def move_forward():
	crawler.do_action('forward',1,speed)
	show_info()
	return
    
def move_backward():
	crawler.do_action('backward',1,speed) 
	show_info()
	return
    
def turn_left():
	crawler.do_action('turn left',1,speed)
	show_info()
	return
    
def turn_right():
	crawler.do_action('turn right',1,speed)
	show_info()
	return

def tilt_up():
	crawler.do_action('look up',1,speed)
	show_info()
	return

def tilt_down():
	crawler.do_action('look down',1,speed)
	return

def main(): 

    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect("red") 

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
     
 
if __name__ == "__main__":
	main()