import socket
import time

host = '192.168.1.24'
port = 8000

soc_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_serv.bind((host,port))
#soc_serv.listen(1)
#conn, addr = soc_serv.accept()[0]

f = open("img2.jpg", 'wb')

#lg=soc_serv.recv(1024)
#print(int.from_bytes(lg, 'little', signed=False))
data=soc_serv.recv(65535)

f.write(data)
f.close()

#conn.close()
soc_serv.close()

