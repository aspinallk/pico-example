GetImage = bytearray(b'\x01\x02\x03')
file = open('test1.txt','w')
num = int(2)
for i in GetImage:
   file.write(str(GetImage[i-1])+',')
file.write('\n'+'abc')
file.close()
