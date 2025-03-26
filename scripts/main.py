# from vilib import Vilib
from picrawler import Picrawler
from time import sleep
import readchar

# Variables
crawler = Picrawler() 
speed = 70

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
	# crawler.do_action('look_up', speed)
	coords = [
		# stand
		[[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
		[[45, 45, -76], [45, 45, -76], [45, 45, -38], [45, 45, -30]],
	]

	for coord in coords:
		crawler.do_step(coord, 60)
	show_info()
	return

def tilt_down():
	# crawler.do_action('look_down', speed)
	coords = [
		# stand
		[[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
		[[45, 45, -28], [45, 45, -40], [45, 45, -68], [45, 45, -76]],
	]
	for coord in coords:
		crawler.do_step(coord, 60)
	return

def stand():
	coords = [
		# stand
		[[45, 45, -50], [45, 45, -50], [45, 45, -50], [45, 45, -50]],
		[[45, 45, -75], [45, 45, -75], [45, 45, -35], [45, 45, -35]],
	]
	for coord in coords:
		crawler.do_step(coord, 60)
	return
	

def main(): 

	# Vilib.camera_start()
	# Vilib.display()
	# Vilib.color_detect("red") 

	try:
		show_info()	
		if(KEYBOARD_MODE):
			while True:
				key = readchar.readkey()
				key = key.lower()
				if key in('wsadrfg'):
					if 'w' == key:
						move_forward()	
					elif 's' == key:
						move_backward()		 
					elif 'a' == key:
						turn_left()		  
					elif 'd' == key:
						turn_right()
					elif 'r' == key:
						print("tilting up")
						tilt_up()
					elif 'f' == key:
						print("tilting dow")
						tilt_down()
					elif 'g' == key:
						print("standing")
						stand()
					sleep(0.05)
					show_info()  

				elif key == readchar.key.CTRL_C:
					print("\n Quit") 
					break	
				
				sleep(0.02)  
		else:
			coords = crawler.move_list['stand']
			# print("Input [0-4] to select leg. Current coords:")
			last_key = None
			while True:
				print("Input [0-4] to select leg.")
				print(coords)
				key = input()

				if key == '':
					# print(actions[last_key])
					# actions_dict[actions[last_key]](my_spider)
					
					print("Input [0-4] to select leg.")
				else:
					# key = String(key)
					if key not in ["0", "1", "2", "3"]:
						print("Invalid leg")
					else:
						last_key = int(key)
						print("Input [X Y Z] to change orientation.")
						s = input()
						nums = list(map(int, s.split()))
						coords = crawler.move_list['stand']
						coords[0][last_key] = nums
						print(coords)
						for coord in coords:
							crawler.do_step(coord, 60)

				# sleep(2)
				# wave_hand(my_spider)
				# shake_hand(my_spider)
				# fighting(my_spider)
				# excited(my_spider)
				# play_dead(my_spider)
				# relax_legs(my_spider)
				# nod(my_spider)
				# shake_head(my_spider)
				# look_left(my_spider)
				# look_right(my_spider)
				# look_up(my_spider)
				# look_down(my_spider)
				# warm_up(my_spider)
				# push_up(my_spider)

	except KeyboardInterrupt:
		pass
	except Exception as e:
		print(f'Error:\n {e}')
	finally:
		crawler.do_action("stand", speed=60)
		sleep(.1)		
	 
 
if __name__ == "__main__":
	main()