Trois programmes peuvent être utilisés :

	test_im.py : utilisé pour tester sur deux images provenant d'une video
		Il contient toutes les explications du programme et de l'analyse effectuée

	test_vid1.py : utilisé pour appliquer la méthode sur la totalité d'une vidéo (sans thread)
		Une autre video peut être utilisée car le programme est adaptatif.

	test_vid2.py : utilisé pour résoudre les problèmes du premier programme en utilisant un thread pour l'analyse.
		Il n'y a qu'un thread qui se lance à chaque fois. Si un thread 
		n'a pas fini mais que 24 images sont passées alors les images continueront 
		à défilé et aucun thread ne sera lancé avant la fin de celui en cours.

Pour lancer l'un des trois programmes python sur linux :
	Il faut que la vidéo soit dans le même dossier
	Utiliser python3 test_im.py
