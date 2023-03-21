import socket
import picamera
import time
import sys
import pigpio
import threading
import queue

######    Configuration de la socket de communication VIDEO  #####
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('192.168.1.24',9322))
conn = client_socket.makefile('wb') #creation socket file-like pour envoyer directement le flux video

con_cmd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
con_cmd.connect(('192.168.1.24',9323))

##################################################################


#####  Pour la communication entre le thread moteur et le thread gyroscope  #####
q=queue.Queue()
mutex=threading.Lock()

##################################################################


#####   Configuration de la camera #####
camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.framerate = 25

########################################

#Corps du projet (capture de la video, envoie par socket, création thread pour controle moteurs)



##### Creation d'un thread pour récupéré les commandes + controle des moteurs #####
moteurs=[0,0,0,0]
def controle_moteurs():
	#Configuration de la socket de communication COMMANDES


	pi1=pigpio.pi()
	pi1.set_mode(18,pigpio.OUTPUT)
	pi1.set_mode(12,pigpio.OUTPUT)
	pi1.set_mode(13,pigpio.OUTPUT)
	pi1.set_mode(19,pigpio.OUTPUT)

	pi1.hardware_PWM(18,800,0)
	pi1.hardware_PWM(12,800,0)
	pi1.hardware_PWM(13,800,0)
	pi1.hardware_PWM(19,800,0)

	while True:
		cmd=con_cmd.recv(1)
		mutex.acquire()
		if cmd==b'a':
			print("\n c'est a \n\n")
			if moteurs[2]<=1000000 :
				moteurs[0]=moteurs[0]+100000
				moteurs[1]=moteurs[1]+100000
				moteurs[2]=moteurs[2]+100000
				moteurs[3]=moteurs[3]+100000
		elif cmd==b'z':
			print("premier")
			moteurs[0]=moteurs[0]-50000
			moteurs[1]=moteurs[1]-50000

			con_cmd.recv(1)
			print("deuxieme")
			moteurs[0]=moteurs[0]+50000
			moteurs[1]=moteurs[1]+50000

		elif cmd==b'q':
			moteurs[0]=moteurs[0]-50000

			con_cmd.recv(1)
			moteurs[0]=moteurs[0]+50000

		elif cmd==b'd':
			moteurs[1]=moteurs[1]-50000

			con_cmd.recv(1)
			moteurs[1]=moteurs[1]+50000

		elif cmd==b'e':
			if moteurs[2]>=100000 :
				moteurs[0]=moteurs[0]-100000
				moteurs[1]=moteurs[1]-100000
				moteurs[2]=moteurs[2]-100000
				moteurs[3]=moteurs[3]-100000
		elif cmd==b'p':
			pi1.stop()
			con_cmd.close()
			break

		q.put(moteurs)
		pi1.hardware_PWM(18,800,moteurs[0])
		pi1.hardware_PWM(12,800,moteurs[1])
		pi1.hardware_PWM(13,800,moteurs[2])
		pi1.hardware_PWM(19,800,moteurs[3])
		mutex.release()
		time.sleep(0.5)

######################################################



##### Creation du thread pour utiliser le gyroscope #####


def gyroscope():

	pi=pigpio.pi()
	gy=pi.i2c_open(1,0x68,0)
	pi.i2c_write_byte_data(gy,0x19,0x00) # de combien diviser la fréquence d'ech ? 0
	pi.i2c_write_byte_data(gy,0x6B,0x00) # Oscillateur interne 8Mhz utilisé
	pi.i2c_write_byte_data(gy,0x1A,0x00) # registre CONFIG : input désactivé (pas de signal externe)
	pi.i2c_write_byte_data(gy,0x1B,0x18) # registre gyroscope : range de +-2000 deg/s
	pi.i2c_write_byte_data(gy,0x38,0x00) # interruption désactivée


	while True:
		mutex.acquire()
		(a,data)=pi.i2c_read_i2c_block_data(gy,0x43,2)
		dataX=np.short((data[0]<<8)|data[1])
		(a,data)=pi.i2c_read_i2c_block_data(gy,0x45,2)
		dataY=np.short((data[0]<<8)|data[1])
		(a,data)=pi.i2c_read_i2c_block_data(gy,0x47,2)
		dataZ=np.short((data[0]<<8)|data[1])

		m=q.get()

		mutex.release()
		time.sleep(0.5)


############################################################

t_moteurs=threading.Thread(target=controle_moteurs, args=())
t_moteurs.start()
t_gyro=threading.Thread(target=gyroscope, args=())
t_gyro.start()


#####	Envoi du flux video #####
time.sleep(15)
camera.start_recording(conn, format='h264')
camera.wait_recording(15)
time.sleep(15)
#################################


#####    Arret de l'ensemble des elements créés  #####
camera.stop_recording()
conn.close()
client_socket.close()
######################################################


