import binascii

png=open("queen.png","rb").read()

for i in range(1500):
	for j in range(1500):
		data=png[12:16]+i.to_bytes(4,byteorder='big')+j.to_bytes(4,byteorder='big')+png[24:29]
		crc32=binascii.crc32(data)&0xffffffff
		if crc32 == 0xdb3f6c0:
			print(i)
			print(j)
