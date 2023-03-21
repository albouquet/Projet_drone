import cv2
import numpy as np
import time
import matplotlib.pyplot as mp
import math

#import de la video
vid = cv2.VideoCapture("test.h264")


i=0

#Test.h264 est une video avec 24 fps (24 images par secondes)
#à la 48 eme image, la vidéo s'est écoulée sur 2 secondes

while vid.isOpened() and i<48:
	vid.read()
	# Capture de snapshot (frame de la video)
	if i==47:
		ret,frme2=vid.read()
	elif i==10:
		ret,frme=vid.read()
	i=i+1



#Transformation des images en GRIS
im_chang = cv2.cvtColor(frme,cv2.COLOR_BGR2GRAY)
im_chang2 = cv2.cvtColor(frme2,cv2.COLOR_BGR2GRAY)

#Taille de l'image en abcisse et en ordonnée
a,b = im_chang.shape



### Etape 1 : binarisation de l'image (mouvement en blanc, autre en noir)

	#L'image im_chang3 est l'image binaire du mouvement (matrice de zeros au départ)
im_chang3=np.zeros((a,b),np.ubyte)
	#Ce tableau contiendra les indexs des régions en mouvement
tab_region_mvm=[]
	#Ce tableau contiendra les indexs des contours des régions en mouvement
tab_index_cont=[]

	#Pour la segmentation avec noyau de Sobel :
imc=np.zeros((a-1,b-1),np.ubyte)
imS1=0
imS2=0

#Pourquoi le range(2,a-2) (et range(b-2)) ? :
#	l'image faisant 320x240 le tableau va de 0 à 319 et de 0 à 239
#	Pour que le noyau de Sobel puisse être appliqué -> (1,a-1) = 318 max,(1,b-1) = 238 max
#	MAIS, les coordonées passées à l'étape 2 (pour Sobel)
#	proviennent d'une étape incluant i+1 (donc 318+1 = 319)
#	Le masque de Sobel s'appliquera sur 319+1 donc hors de l'index de l'image
#	Voila pourquoi au départ je fais range(2,a-2) et range(2,b-2)

for i in range(2,a-2):
	for j in range(2,b-2):
		#Seuille utilisé : 100 (si c'est supérieur -> il y a eu un mouvement)
		#abs pour faire disparaitre les valeurs négatives
		if abs(np.int16(im_chang[i,j])-np.int16(im_chang2[i,j])) > np.int16(100):
			im_chang3[i,j]=0 #du changement (donc mouvement) -> noir

			#index des regions en mouvement, placées dans tab_region_mvm
			tab_region_mvm.append((i,j))
			tab_region_mvm.append((i-1,j-1))
			tab_region_mvm.append((i,j-1))
			tab_region_mvm.append((i+1,j-1))
			tab_region_mvm.append((i-1,j))
			tab_region_mvm.append((i+1,j))
			tab_region_mvm.append((i-1,j+1))
			tab_region_mvm.append((i,j+1))
			tab_region_mvm.append((i+1,j+1))


		else:
			im_chang3[i,j]=255 # peu de changement -> blanc


### Etape2 :  Segmentation en contour

	#Application du filtre de sobel (noyau 3x3):

for a in tab_region_mvm:
	i=a[0]
	j=a[1]
	imS1 = im_chang3[i-1,j-1]*(-1) + im_chang3[i,j-1]*(-2) + im_chang3[i+1,j-1]*(-1)
	+ im_chang3[i-1,j+1] + (im_chang3[i,j+1]*2) + im_chang3[i+1,j+1]

	imS2 = im_chang3[i-1,j-1]*(-1) + im_chang3[i-1,j]*(-2) + im_chang3[i-1,j+1]*(-1)
	+ im_chang3[i+1,j-1] + (im_chang3[i+1,j]*2) + im_chang3[i+1,j+1]

	imc[i,j] = np.ubyte(math.sqrt(imS1**2 + imS2**2))
	if imc[i,j]> 200:
		tab_index_cont.append((i,j))

#Coloration en vert de l'image final (de l'image 2)
for index in tab_index_cont:
	frme2[index[0],index[1]]=[0,255,0]

#Affichage histogramme de l'image finale
#hist=cv2.calcHist([im_chang3],[0], None, [255], [0,255])
#mp.plot(hist)
#mp.show()

#cv2.imwrite("./img1.png", im_chang)
#cv2.imwrite("./img2.png", im_chang2)
#cv2.imwrite("./img_region.png", im_chang3)
#cv2.imwrite("./img_contour.png", imc)
#cv2.imwrite("./img_final.png", frme2)

cv2.imshow("image",im_chang)
cv2.waitKey(0)
cv2.imshow("image",im_chang2)
cv2.waitKey(0)
cv2.imshow("image",im_chang3)
cv2.waitKey(0)
cv2.imshow("image",imc)
cv2.waitKey(0)
cv2.imshow("image",frme2)
cv2.waitKey(0)


vid.release()
cv2.destroyAllWindows()

