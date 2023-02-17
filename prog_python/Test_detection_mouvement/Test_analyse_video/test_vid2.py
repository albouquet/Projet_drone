import cv2
import numpy as np
import time
import matplotlib.pyplot as mp
import math
import threading
import queue
q=queue.Queue()

#Fonction thread contenant retournant les indexs des contours des mouvements
def thread_analyse(a,b,im_chang,im_chang2):
	#L'image im_chang3 est l'image binaire du mouvement (matrice de zeros au départ)
	im_chang3=np.zeros((a,b),np.ubyte)
	#Pour la segmentation avec noyau de Sobel :
	imS1=0
	imS2=0

	#Ce tableau contiendra les indexs des régions en mouvement
	tab_region_mvm=[(np.ubyte(0),np.ubyte(0))]
	list_ctr=[(np.ubyte(0),np.ubyte(0))]




	### Etape 1 : binarisation de l'image (mouvement en blanc, autre en noir)
	for i in range(2,a-2):
		for j in range(2,b-2):
			#Seuille utilisé : 100 (si c'est supérieur -> il y a eu un mouvement)
			#abs pour faire disparaitre les valeurs négatives
			if abs(np.int16(im_chang[i,j])-np.int16(im_chang2[i,j])) > np.int16(100):
				im_chang3[i,j]=0 #du changement (donc mouvement) -> noir
				#index des regions en mouvement, placées dans tab_region_mvm
				#tab_region_mvm.append((i,j))
				#tab_region_mvm.append((i-1,j-1))
				tab_region_mvm.append((i,j-1))
				#tab_region_mvm.append((i+1,j-1))
				tab_region_mvm.append((i-1,j))
				tab_region_mvm.append((i+1,j))
				#tab_region_mvm.append((i-1,j+1))
				tab_region_mvm.append((i,j+1))
				#tab_region_mvm.append((i+1,j+1))

			else:
				im_chang3[i,j]=255 # peu de changement -> blanc


	### Etape2 :  Segmentation en contour

		#Application du filtre de sobel (noyau 3x3):

	for index in tab_region_mvm:
		i=index[0]
		j=index[1]
		imS1 = im_chang3[i-1,j-1]*(-1) + im_chang3[i,j-1]*(-2) + im_chang3[i+1,j-1]*(-1)
		+ im_chang3[i-1,j+1] + (im_chang3[i,j+1]*2) + im_chang3[i+1,j+1]

		imS2 = im_chang3[i-1,j-1]*(-1) + im_chang3[i-1,j]*(-2) + im_chang3[i-1,j+1]*(-1)
		+ im_chang3[i+1,j-1] + (im_chang3[i+1,j]*2) + im_chang3[i+1,j+1]

		if np.ubyte(math.sqrt(imS1**2 + imS2**2)) > 230 :
			list_ctr.append(index)

	#Fin traitement
	q.put(list_ctr)
	print("c'est put à : ", time.time())
	print("tab : ",len(tab_region_mvm),"et :",len(list_ctr))






#import de la video
vid = cv2.VideoCapture("test.h264")
#vid.set(cv2.CAP_PROP_MODE, cv2.CAP_MODE_GRAY)


nb_im=0
ret,frme1=vid.read()
im1 = cv2.cvtColor(frme1,cv2.COLOR_BGR2GRAY)

#Taille de l'image en abcisse et en ordonnée
a,b = im1.shape
#tableau contenant les précedents contours
#list_ctr=[]

x=threading.Thread(target=thread_analyse, args=(a,b,im1,im1))
x.start()


#Debut (Lecture de la video, Analyse, Affichage)



while vid.isOpened():
	vid.read()
	# Capture de snapshot (frame de la video)
	ret,frme2=vid.read()
	im2 = cv2.cvtColor(frme2,cv2.COLOR_BGR2GRAY)

	if nb_im == 6:
		if not x.is_alive():
			print("C'est lance a : ",time.time())
			x=threading.Thread(target=thread_analyse, args=(a,b,im1,im2))
			x.start()
			im1=im2
			nb_im=0
		else:
			nb_im=nb_im-1
	else:
		if not q.empty():
			list_c=q.get()
			print("c'est recup")
			for index in list_c:
				frme2[index[0],index[1]]=[0,255,0]

	cv2.imshow("image",frme2)
	cv2.waitKey(200)
	nb_im=nb_im+1









vid.release()
cv2.destroyAllWindows()

