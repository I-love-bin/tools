import struct
import binascii
import sys

def getSecName(time,size,off,hdr,name,ELF):
	shstrtab={}
	secOff=((ELF[62]+(16**2)*ELF[63])*size+off)+(sum(hdr[0:4]))
	shStrTabOff=ELF[secOff]+(16**2)*(ELF[secOff+1]+(16**2)*(ELF[secOff+2]+(16**2)*(ELF[secOff+3]+(16**2)*\
					(ELF[secOff+4]+(16**2)*(ELF[secOff+5]+(16**2)*(ELF[secOff+6]+(16**2)*(ELF[secOff+7])))))))
	shStrTabLen=ELF[secOff+8]+(16**2)*(ELF[secOff+9]+(16**2)*(ELF[secOff+10]+(16**2)*(ELF[secOff+11]+(16**2)*\
					(ELF[secOff+12]+(16**2)*(ELF[secOff+13]+(16**2)*(ELF[secOff+14]+(16**2)*(ELF[secOff+15])))))))
	for i in range(shStrTabLen):
		name.append(chr(ELF[shStrTabOff+i]))
	
def writeSecHdrTable(size,base,off,pat,name,hdr,ELF,exText):
	secName=''
	count=0

	while(name[ELF[base+pat]+count]!='\0'):
		secName+=name[ELF[base+pat]+count]
		count+=1

	#Something is wrong
	secOff=(off+pat)+(sum(hdr[0:4]))
	SshOffsetOff=ELF[secOff]+(16**2)*(ELF[secOff+1]+(16**2)*(ELF[secOff+2]+(16**2)*(ELF[secOff+3]+(16**2)*\
					(ELF[secOff+4]+(16**2)*(ELF[secOff+5]+(16**2)*(ELF[secOff+6]+(16**2)*(ELF[secOff+7])))))))

	EshOffsetOff=SshOffsetOff+ELF[secOff+8]+(16**2)*(ELF[secOff+9]+(16**2)*(ELF[secOff+10]+(16**2)*(ELF[secOff+11]+(16**2)*\
					(ELF[secOff+12]+(16**2)*(ELF[secOff+13]+(16**2)*(ELF[secOff+14]+(16**2)*(ELF[secOff+15])))))))-1
	exText.write('Section : '+secName+'\n')
	exText.write('StartSecOffset : 0x'+format(SshOffsetOff,'x').zfill(8)+'\n')
	exText.write('EndSecOffset : 0x'+format(EshOffsetOff,'x').zfill(8)+'\n')
	exText.write('SecHdrOffset : 0x'+format(base+pat,'x').zfill(8)+'\n')
	exText.write('---'*16)

	for i in range(size):
		if( (i%16)==0 ):
			exText.write('\n')
		strData=format(ELF[i+base+pat],'x')
		exText.write(strData.zfill(2)+' ')
	exText.write('\n'*2)

def writeProHdrTable(msg,size,base,pat,ELF,exText):
	msg+='\n'
	exText.write(msg)
	exText.write('Offset : 0x'+format(base+pat,'x').zfill(8)+'\n')
	exText.write('---'*16)

	for i in range(size):
		if( (i%16)==0 ):
			exText.write('\n')
		strData=format(ELF[i+base+pat],'x')
		exText.write(strData.zfill(2)+' ')
	exText.write('\n'*2)

def writeELFHdr(msg,size,ELF,exText):
	msg+='\n'
	exText.write(msg)
	exText.write('---'*16)
	for i in range(size):
		if( (i%16)==0 ):
			exText.write('\n')
		strData=format(ELF[i],'x')
		exText.write(strData.zfill(2)+' ')
	exText.write('\n'*2)

def ELF32Info(wbSize,wbTime,wbOff,ELF):
	tmp={"e_ehsize":ELF[52]+(16*16)*ELF[53]}
	wbSize.update(tmp)

def ELF64Info(wbSize,wbTime,wbOff,ELF):
	tmp={"e_ehsize":ELF[52]+(16**2)*ELF[53]}
	wbSize.update(tmp)
	tmp={'e_phsize':ELF[54]+(16**2)*ELF[55]}
	wbSize.update(tmp)
	tmp={'e_shsize':ELF[58]+(16**2)*ELF[59]}
	wbSize.update(tmp)

	tmp={'e_phnum':ELF[56]+(16**2)*ELF[57]}
	wbTime.update(tmp)
	tmp={'e_shnum':ELF[60]+(16**2)*ELF[61]}
	wbTime.update(tmp)

	tmp={'e_phoff':ELF[32]+(16**2)*(ELF[33]+(16**2)*(ELF[34]+(16**2)*\
			(ELF[35]+(16**2)*(ELF[36]+(16**2)*(ELF[37]+(16**2)*\
			(ELF[38]+(16**2)*ELF[39]))))))}
	wbOff.update(tmp)
	tmp={'e_shoff':ELF[40]+(16**2)*(ELF[41]+(16**2)*(ELF[42]+(16**2)*\
			(ELF[43]+(16**2)*(ELF[44]+(16**2)*(ELF[45]+(16**2)*\
			(ELF[46]+(16**2)*ELF[47]))))))}
	wbOff.update(tmp)

def main(imFileName,exFileName):
	ELFHdr=[16,2,2,4,8,8,8,4,2,2,2,2,2,2]
	ProHdr=[4,4,8,8,8,8,8,8]
	SecHdr=[4,4,8,8,8,8,4,4,8,8]

	secName=[]

	size={}
	time={}
	off={}

	with open(imFileName,mode='rb') as FILE:
		imELF=FILE.read()

	if(imELF[4]==0):
		print("****ERROR*****")
		print("Invalid class.")
	elif(imELF[4]==1):
		ELF32Info(size,time,off,imELF)
	elif(imELF[4]==2):
		ELF64Info(size,time,off,imELF)

	with open(exFileName,mode='w') as TEXT:
		writeELFHdr('ElLF header',size['e_ehsize'],imELF,TEXT)
		TEXT.write('***'*16+'\n')
		TEXT.write('***'*16+'\n\n')
		for i in range(time['e_phnum']):
			writeProHdrTable('Program header'+str(i+1),size['e_phsize'],off['e_phoff'],i*size['e_phsize'],imELF,TEXT)
		TEXT.write('***'*16+'\n')
		TEXT.write('***'*16+'\n\n')

		getSecName(time['e_shnum'],size['e_shsize'],off['e_shoff'],SecHdr,secName,imELF)

		for i in range(time['e_shnum']):
			writeSecHdrTable(size['e_shsize'],off['e_shoff'],off['e_shoff'],i*size['e_shsize'],secName,SecHdr,imELF,TEXT)

		TEXT.write('***'*16+'\n')
		TEXT.write('***'*16+'\n')

if __name__=="__main__":
	length=len(sys.argv)
	if( length<2 ):
		print("**********ERROR**********")
		print("Input imported file name.")
	elif((2<=length)&(length<3)):
		print("**********ERROR**********")
		print("Input exported file name.")
	main(sys.argv[1],sys.argv[2])
