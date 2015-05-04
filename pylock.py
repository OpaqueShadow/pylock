import subprocess
import RPi.GPIO as GPIO
import time


def main():
	unlock_bolt()
	locked = unlock_bolt()

	while 1 == 1:
		if check_usb():
			locked = unlock_bolt() if locked else lock_bolt()
		time.sleep(2)


def unlock_bolt():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(33, GPIO.OUT)
	p = GPIO.PWM(33, 50)
	p.start(12.5)
	time.sleep(1.5)
	p.stop()
	return False

def lock_bolt():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(33, GPIO.OUT)
	p = GPIO.PWM(33, 50)
	p.start(7.1)
	time.sleep(1)
	p.stop()
	return True

def check_usb():
	#get's the listing of all usb devices attached to the system
	device_list = subprocess.check_output('lsusb', shell=True)
	device_ids = []

	auth_id = "03f0";

	#parse for the devicedev's
	for line in filter(lambda s: s.startswith('Bus'), device_list.split('\n')):
		businfo,dev, _ = line.split(':')
		dev =dev.split()[1]
		device_ids.append(dev)


	if auth_id in device_ids:
		return True
	else:
		return False

if __name__ == "__main__":
	main()