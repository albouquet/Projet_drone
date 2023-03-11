#Pour le gy-521 : je récupère les valeurs des registres 43 à 48 représentant l'angle de rotation X, Y et Z (valeurs sur 2 octets/registres)
#Pour avoir des valeurs conforme au type du datasheet, je transforme chacune de ces valeurs en type short (signé).

import pigpio
import time
import numpy as np
pi=pigpio.pi()

#1 c'est le port I2C
#0 c'est le flag
gy=pi.i2c_open(1,0x68,0)

def MPU_Init():
	pi.i2c_write_byte_data(gy,0x19,0x00) # de conbien diviser la fréquence d'ech ? 0
	pi.i2c_write_byte_data(gy,0x6B,0x00) # Oscillateur interne 8Mhz utilisé
	pi.i2c_write_byte_data(gy,0x1A,0x00) # registre CONFIG : input désactivé (pas de signal externe)
	pi.i2c_write_byte_data(gy,0x1B,0x18) # registre gyroscope : range de +-2000 deg/s
	pi.i2c_write_byte_data(gy,0x38,0x00) # interruption désactivée



MPU_Init()
while True:
	(a,data)=pi.i2c_read_i2c_block_data(gy,0x43,2)
	dataX=np.short((data[0]<<8)|data[1])
	(a,data)=pi.i2c_read_i2c_block_data(gy,0x45,2)
	dataY=np.short((data[0]<<8)|data[1])
	(a,data)=pi.i2c_read_i2c_block_data(gy,0x47,2)
	dataZ=np.short((data[0]<<8)|data[1])

	print(dataX," | ", dataY, " | ", dataZ)
	time.sleep(0.3)
