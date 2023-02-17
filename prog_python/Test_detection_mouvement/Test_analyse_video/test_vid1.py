import cv2
import numpy as np
import time
import matplotlib.pyplot as mp
import math

#import de la video
vid = cv2.VideoCapture("test.h264")
#vid.set(cv2.CAP_PROP_MODE, cv2.CAP_MODE_GRAY)


i=0
ret,frme1=vid.read()
im_chang = cv2.cvtColor(frme1,cv2.COLOR_BGR2GRAY)

#Taille de l'image en abcisse et en ordonnée
a,b = im_chang.shape
#L'image im_chang3 est l'image binaire du mouvement (matrice de zeros au départ)
im_chang3=np.zeros((a,b),np.ubyte)
#Ce tableau contiendra les indexs des régions en mouvement
tab_region_mvm=[]
list_ctr=[]
#Pour la segmentation avec noyau de Sobel :
imS1=0
imS2=0



#Debut (Lecture de la video, Analyse, Affichage)



while vid.isOpened():
	vid.read()
	# Capture de snapshot (frame de la video)
	ret,frme2=vid.read()
	#Transformation des images en GRIS
	im_chang2 = cv2.cvtColor(frme2,cv2.COLOR_BGR2GRAY)

	if i == 4:
		#Je vide le tableau contenant les précedents contours
		list_ctr[:]=[]
		tab_region_mvm[:]=[]
		### Etape 1 : binarisation de l'image (mouvement en blanc, autre en noir)

		for i in range(2,a-2):
			for j in range(2,b-2):
				#Seuille utilisé : 100 (si c'est supérieur -> il y a eu un mouvement)
				#abs pour faire disparaitre les valeurs négatives
				if abs(np.int16(im_chang[i,j])-np.int16(im_chang2[i,j])) > np.int16(100):
					im_chang3[i,j]=0 #du changement (donc mouvement) -> noir

					#index des regions en mouvement, placées dans tab_region_mvm
					tab_region_mvm.append((i,j))
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

		im_chang=im_chang2
		i=0
	else:
		for index in list_ctr:
			frme2[index[0],index[1]]=[0,255,0]

	cv2.imshow("image",frme2)
	cv2.waitKey(100)
	i=i+1









#cv2.imshow("image",im_chang)
#cv2.waitKey(0)
#cv2.imshow("image",im_chang2)
#cv2.waitKey(0)
#cv2.imshow("image",im_chang3)
#cv2.waitKey(0)
#cv2.imshow("image",imc)
cv2.waitKey(0)

#cv2.imwrite("./img_contour.png", imc)

vid.release()
cv2.destroyAllWindows()

