/* Serveur réseaux pour reception video via socket

Le test de reception d'une image a été fait avec une socket TCP.
Le TCP est utilisé car la taille de l'image recu (envoyé par la rasp)
est variable. En UDP il aurait fallu faire un protocole pour recevoir
la taille d'abord, puis adapter la reception pour l'envoi de l'image.

*/



#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
typedef int SOCKET;
typedef struct sockaddr_in SOCKADDR_IN;
typedef struct sockaddr SOCKADDR;


/**************/
int lenbuf = 2048;

/**************/


void main(){

	SOCKET sock = socket(AF_INET,SOCK_DGRAM,0);
	SOCKADDR_IN sin = { 0 };
	sin.sin_addr.s_addr = inet_addr("192.168.1.24");
	sin.sin_family = AF_INET;
	sin.sin_port = htons(8000);
	bind(sock, (SOCKADDR *) &sin, sizeof sin);

	SOCKADDR_IN from = { 0 };
	int from_taille=sizeof(from);
	char buffer1[lenbuf];

	int n=0;
	n=recvfrom(sock, &buffer1, 1,0, (SOCKADDR *) &from,&from_taille);
	buffer1[n]='\0';
	printf("Taille recu %d;\n Nombre=%s",n,buffer1);

	close(sock);
}
