# Projet Drone Camera

![Drone final](images/drone.jpg)

## Description :

Mon projet consiste à réaliser un drone, muni d'une caméra.
L'objectif est de pouvoir controler le drone à distance et récupérer en même temps le flux vidéo 
envoyé par celui-ci, via un ordinateur.
Le deuxième aspect de mon projet est la traitement de la vidéo recue sur l'ordinateur, pour détecter
les mouvements dans celle-ci (lorsque le drone est stationnaire).



## Materiels utilisés :

J'ai réalisé le drone avec une Raspberry pi zero et sa caméra V2 dédiée.
Quatre petits moteurs de type 720 et leurs helices permettent au drone de prendre de l'altitude.
Quatre transistors C1815, autant de diodes et des résistances forment la partie éléctronique des moteurs.
Un module de type GY-521 est utilisé pour garder l'engin parallèle au sol.
La batterie LI-PO 3.7V 1A permet d'alimenter l'ensemble.

Et aussi, un ordinateur portable possédant une carte wifi et une carte graphique pour traiter la video.

![Materiels pour la fabrication du drone](images/materiel.jpg)

Sur l'ordinateur, j'ai créé **un point d'accès Wifi grâce à hostapd**, permettant au drone de se connecter directement dessus.



## Programmation :

Deux programmes sont utilisés :
 - Un sur la Raspberry pi zero qui permet de gérer les différents aspects du drone (moteurs, gyroscope, camera, wifi).
 - Un sur l'ordinateur permettant à l'utilisateur de controler le drone et recevoir la video.

Ces deux programmes sont en python3.

Les deux programmes s'échangent des informations (commandes pour l'un, vidéo pour l'autre).
Pour cela, j'utilise une connexion wifi, pour deux raisons : la portée et la simplicité d'utilisation des APIs.
Deux sockets réseau TCP sont donc utilisées.
Le role du serveur est dédié au programme de l'ordinateur et le client celui du drone.
Le drone se connecte donc au serveur à l'aide de deux sockets.


### Programme sur la Raspberry pi zero :

Il est séparé en trois parties :
- Le programme principale pour l'envoie du flux vidéo via la camera.
- Un thread pour la gestion des commandes recu par l'utilisateur et la transmission aux moteurs.
- Un thread pour la gestion du gyroscope et la aussi la gestion des moteurs par celui-ci.

La bibliothéque Picamera, socket, pygpio et threading sont indispensables.

#### Les threads :

Les deux threads s'exectuant en même temps, et manipulant tout les deux les moteurs, il m'a fallu introduire un système de sémaphore
pour empecher l'un de s'exécuter lorsque l'autre est en travail.
Chacun vérifie que le mutex est disponible avant de s'executer.

#### Les moteurs et le gyroscope :

Ces deux éléments sont gérés grâce aux GPIOs du Raspberry pi, et utilisé avec pigpio.

Les 4 moteurs recoivent chacun **un signal PWM de type Hardware** grâce aux broche 18,12,13 et 19. 
Cela a pour effet de ne pas utiliser le processeur pour le controle des moteurs.

Le module GY-521 est controlé à travers une liaison I2C (SDA, SDL). Il possède un gyroscope,
un accélérometre et un capteur de température. Dans mon cas, seules les valeurs du gyroscope sont récupérées 
pour stabiliser le drone.

#### La caméra :

La bibliothéque picamera permet de définir les paramètres de la caméra (framerate, résolution, qualité ...).
La fonction start_recording() permet d'envoyer le flux vidéo de type h264 directement à travers la socket réseau.


### Programme sur l'ordinateur :

Ce programme se sépare en trois parties :
- Le programme principale récupère en boucle les commandes de l'utilisateur et les envoie au drone.
- Un sous-processus est lancé : c'est le programme mpv, permettant d'afficher le contenu vidéo.
- Un thread permet de récupérer le flux vidéo et de l'envoyer au sous-processus mpv.

Les bibliothéque keyboard, socket, threading et subprocess sont indispensable.

#### La gestion du clavier :

Pour gérer les entrés utilisateur, j'utilise des fonctions de la bibliotheque keyboard.
Par exemple, lorsque la touche z est pressée, l'octet représentant le z est envoyé au drone.
Celui-ci diminue donc la vitesse des deux moteurs avant, se qui le fait avancer.
En appuyant à nouveau sur z, le drone se stabilise à nouveau.

Cinq touches sont possibles : 
- A pour que le drone prenne de l'altitude (augmente la vitesse de tous les moteurs)
- E pour que le drone diminue la vitesse de tous les moteurs.
- Z pour que le drone diminue la vitesse des deux moteurs avant (permet d'avancer).
- Q et D pour que le drone effectue une rotation respectivement à gauche ou à droite en diminuant 
la vitesse du moteur avant gauche ou droit.
- P pour arreter le programme.



## Montage éléctronique :

Un montage éléctronique permet le controle des 4 moteurs par la Raspberry pi.
En effect, les GPIOs ne peuvent délivrer qu'un courant d'environ 30 mA, ce qui est trop faible pour 
alimenter des moteurs (ici un moteur alimenté en 3.7 volt consomme 100mA).

Pour résoudre ce problème, j'utilise un transistor dont la base est reliée à la Raspberry pi 
et l'émetteur au moteur. Un signal PWM est envoyé à la base du transistor (agissant comme un interrupteur)
determinant la puissance moyenne envoyé au moteur.
La diode permet d'absorber le courant généré par le moteur en fin de rotation (évite de griller le transistor).

![Schéma montage moteur](images/Capture)

Aussi, la Raspberry pi doit être alimenté en 5v. Hors, ayant une batterie 3.7V, j'ai ajouté un convertisseur 
3.7V vers 5V pour pouvoir l'alimenter (elle ne consomme qu'environ 300mA).

La totalité du montage consomme en moyenne (rasp  -> 300mA + moteurs -> 4*100mA + gyroscope -> 20 mA + convertisseur -> X) 750 mA.



## Support du drone : 

Pour soutenir l'ensemble des composants du drone (moteurs, gyroscope, Raspberry pi, batterie, camera), j'ai réalisé 
un support en plastique à l'aide du logiciel FreeCad et l'ai imprimé avec mon imprimante 3D.

![Support du drone](images/impression_support.jpg)
![Support du drone](images/support_drone.jpg)



## Programme de détéction de mouvement :

Le programme de détéction de mouvement est réalisé en python à l'aide d'opencv.

Le programme principale récupère et affiche les images une à une, tandisqu'un thread calcul les coordonées de la zone 
en mouvement.

Les étapes du thread sont les suivantes :
- Une image est comparé à la précédente toutes les secondes (ou moins)
- La soustraction de ces deux images permet finalement de les binariser avec un noir la zone qui change et en blanc 
celle qui ne change pas.
- La recherche des contours est alors réalisé en réalisant une convolution avec un masque de Sobel et le calcul du gradient.
- Les coordonées des contours retenues sont alors envoyées au programme principale qui les colorie en vert sur les images suivantes.

Trois programmes sont disponibles dans le git : un permettant de faire le test sur deux images,
un autre de faire le test sur une vidéo (sans utiliser de thread), et le dernier traite une vidéo avec un thread.

#### Problème sur la détéction de mouvement :

Mon programme fonctionne sur un fichier vidéo, ou directement sur la caméra. Mais la fonction récupérant ces flux vidéos ne prend pas en 
parametre une socket réseau. Par conséquent, il ne m'a pas été possible de l'inclure dans le programme finale de l'ordinateur.



## Etape de réalisation du projet :

**1. Réflexion sur le materiel et l'aspect global du projet
2. Réalisation du programme de detection de mouvement
3. Test de la partie éléctronique du drone
4. Test des différentes parties des deux programmes (socket, GPIO, clavier, thread)
5. Réalisation des deux programmes.**



## Conclusion :

J'ai, au départ, surestimé le temps alloué au projet et suis partie sur une réalisation à base de microcontroleur PIC 
ou d'ESP32. Pendant les vacances d'hiver, je me suis rendu compte que c'était trop lent et qu'il fallait que je change 
de support. J'ai donc opté pour une Raspberry pi, plus facile à prendre en main et permettant d'outrepasser les réflexions 
sur la connectique/communication de la caméra et du module wifi notamment.

Au final, mon drone est piloté à distance, et envoie le flux video de la camera qui s'affiche sur l'ordinateur.
