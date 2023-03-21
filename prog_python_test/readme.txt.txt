Le programme python contenue dans ce dossier sera executé sur la raspberry.

Il permet de :

	Configuration de la socket :
		Mettre en place une socket UDP afin qu'il se connecte sur l'ordinateur distant et envoie le flux video 

	Configurer la camera : 
		format de l'image de sortie (320x240), framerate (24)
	
	Envoie du flux :
		Capturer une image (en la compressant en jpeg) en continue dans un buffer (stream)
		avec camera.capture(stream, 'jpeg')
		Envoyer les images les unes après les autres via la socket UDP


Le programme permet donc la communication avec un autre terminal distant afin d'envoyer le flux video capturé par la camera de la raspberry.


http://abyz.me.uk/rpi/pigpio/python.htm
https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi