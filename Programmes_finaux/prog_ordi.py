import socket
import time
#import cv2
import numpy as np
import threading
import keyboard
import subprocess


def lecture(con_v,play):


	while True:
		try:
			flux=con_v.read(1024)
		#im=np.array(conn_vid.read(65535))
		#frame = conn_vid.read(4096)
		#cv2.imshow("im",frame)
			play.stdin.write(flux)
		except:
			player.terminate()
			break





host = '192.168.1.24'
port = 9322

soc_vid = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_vid.bind((host,port))
soc_vid.listen(1)
conn_vid = soc_vid.accept()[0].makefile('rb')

soc_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_cmd.bind((host,9323))
soc_cmd.listen(1)
conn_cmd = soc_cmd.accept()[0]


cmdline=['mpv','--fps=25','--cache=yes','-']
player=subprocess.Popen(cmdline,stdin=subprocess.PIPE)

x=threading.Thread(target=lecture, args=(conn_vid,player))
x.start()


while True:
	event='0'
	#récupération de la touche:
	event=keyboard.read_key()

	#traitement de la touche:
	if (event=="a"):
		conn_cmd.send(b'a')
		print("c'est a \n")
	elif (event=="z"):
		conn_cmd.send(b'z')
		print("c'est z \n")
	elif (event=="q"):
		conn_cmd.send(b'q')
		print("c'est q \n")
	elif (event=="e"):
		conn_cmd.send(b'e')
		print("c'est e \n")
	elif (event=="p"):
		conn_cmd.send(b'p')
		player.terminate()
		break
	time.sleep(1)

conn_vid.close()
conn_cmd.close()

soc_vid.close()
