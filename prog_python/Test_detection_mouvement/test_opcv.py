import cv2
import numpy as np
import time

#import de la video
vid = cv2.VideoCapture("test.h264")


i=0
while vid.isOpened() and i<48:
	vid.read()
	# Capture de snapshot (frame de la video)
	if i==47:
		ret,frme2=vid.read()
	elif i==10:
		ret,frme=vid.read()
	i=i+1



#Transformation de l'image en GRIS
im_chang = cv2.cvtColor(frme,cv2.COLOR_BGR2GRAY)
im_chang2 = cv2.cvtColor(frme2,cv2.COLOR_BGR2GRAY)

a,b = im_chang.shape

#Création de l'image final (matrice de zeros au départ)
im_chang3=np.zeros((a,b),np.int8)



for i in range(0,a):
	for j in range(0,b):
		im_chang3[i,j]=255-abs(im_chang[i,j]-im_chang2[i,j])



#im_chang3 = cv2.bitwise_and(frme,frme2)


cv2.imshow("image",im_chang3)
cv2.waitKey(0)

vid.release()
cv2.destroyAllWindows()

