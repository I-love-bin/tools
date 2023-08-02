with open("./sample.txt","rb") as f:
	data = f.read()
result=b''

for i in range(len(data)):
	if( (i%12)!=0 ):
		adds=1
	else:
		adds=-1
	byte=int.from_bytes(data[i:i+1])
	if( byte==0xff and adds==1 ):
		result=result+b'\x00'
		continue
	if( byte==0x0 and adds==-1 ):
		result=result+b'\xff'
		continue
	result=result+(byte+adds).to_bytes(1,'big')

try:
	with open("./result",'wb') as f:
		f.write(result)
except FileExistsError:
	pass
