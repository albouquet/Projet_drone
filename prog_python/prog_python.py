import io
import socket
import struct
import picamera
import time

host ='192.168.1.24'
port = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect((host,port))

#connection = client_socket.makefile('wb')

camera=picamera.PiCamera()
camera.resolution =(320,240)
camera.framerate = 24
time.sleep(2)

try:
	while True:

		stream = io.BytesIO()
		#start = time.time()

		#camera.capture(stream, 'jpeg')
		#stream.seek(0)
		#stream.truncate()

		f=open("projet.py", "rb")
		#f.write(stream.read())
		client_socket.send(f.read())
		f.close()


		#for frame in camera.capture_continuous(stream,'jpeg'):
		#	f=open("im1.jpg", "xb")
		#	f.write(stream.read())
		#	f.close()

			#client_socket.send(stream.read())
			#time.sleep(5)

			#if time.time() - start > 30:
			#	break
			#stream.seek(0)
			#stream.truncate()

		#time.sleep(3)
		break


finally:
	client_socket.close()
