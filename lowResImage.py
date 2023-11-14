from machine import UART, Pin
import time
import binascii

#uart1 = UART(1, baudrate=57600, bits=8, parity=None, stop=2, rxbuf= 16384, tx=Pin(4), rx=Pin(5))
uart1 = UART(1, baudrate=57600, bits=8, parity=None, stop=2, rxbuf= 8192, tx=Pin(4), rx=Pin(5))

file = open('imagedata.txt','w')

Header = bytearray(b'\xef\x01\xff\xff\xff\xff')

print('VfyPwd')
VfyPwd = bytearray(b'\x01\x00\x07\x13\x00\x00\x00\x00')
checksum = sum(VfyPwd).to_bytes(2,'big')
Cmd_VfyPwd = Header + VfyPwd + bytearray(checksum)

print('Tx: ',binascii.hexlify(Cmd_VfyPwd))

uart1.write(Cmd_VfyPwd)

time.sleep(0.1)

ACK_Packet = bytes()
while uart1.any() > 0:
    ACK_Packet += uart1.read(1)

print('R1: ',binascii.hexlify(ACK_Packet))

print()
print('ReadSysPara')
ReadSysPara = bytearray(b'\x01\x00\x03\x0f')
checksum = sum(ReadSysPara).to_bytes(2,'big')
Cmd_ReadSysPara = Header + ReadSysPara + bytearray(checksum)

print('Tx: ',binascii.hexlify(Cmd_ReadSysPara))

uart1.write(Cmd_ReadSysPara)

time.sleep(0.1)

ACK_Packet = bytes()
while uart1.any() > 0:
    ACK_Packet += uart1.read(1)

print('R2: ',binascii.hexlify(ACK_Packet))


print()
print('GetImage')
GetImage = bytearray(b'\x01\x00\x03\x01')
checksum = sum(GetImage).to_bytes(2,'big')
Cmd_GetImage = Header + GetImage + bytearray(checksum)

print('Tx: ',binascii.hexlify(Cmd_GetImage))

uart1.write(Cmd_GetImage)

time.sleep(0.1)

ACK_Packet = bytes()
while uart1.any() > 0:
    ACK_Packet += uart1.read(1)

print('R3: ',binascii.hexlify(ACK_Packet))

ack = ACK_Packet[len(ACK_Packet)-3]

if ack == 0 :
    print()
    print('upload image')
    UpChar = bytearray(b'\x01\x00\x03\x0a')
    checksum = sum(UpChar).to_bytes(2,'big')
    Cmd_UpChar = Header + UpChar + bytearray(checksum)

    print('Tx: ',binascii.hexlify(Cmd_UpChar))

    uart1.write(Cmd_UpChar)

    time.sleep(0.1)

    ACK_Packet = bytes()
    ACK_Packet = uart1.read(12)
    print('R4: ',binascii.hexlify(ACK_Packet))


    while uart1.any() == 0:
        print('Waiting')
        
#    image = bytes()
#    image = uart1.read(139)
#    print('R5: ',binascii.hexlify(image))
    
    time.sleep_ms(25)
    data = bytes()
    while uart1.any() > 0:
        data += uart1.read(8192)
    end = 0
    no = 1
    start = data.find(b'\xef\x01')
    while (start != -1) and (no !=225):
        packet = bytes()
        end = data.find(b'\xef\x01',start + 2)
        print('start, end: ', start,end)
        if no>64 :
            packet = data[start+33:start+113]
            print('No: ',no)
            print('R6: ',binascii.hexlify(packet),"   ", len(packet))

            print('len: ',len(packet))
            
            high = int(0)
            low = int(0)
            if (packet[0]>>4)>4:
                high = 1
            else:
                high = 0
            
            if (packet[0]&0x0F)>4:
                low = 1
            else:
                low = 0

            file.write(str(high)+','+str(low))
            for i in range(79):
                if (packet[i]>>4)>4:
                    high = 1
                else:
                    high = 0
                
                if (packet[i]&0x0F)>4:
                    low = 1
                else:
                    low = 0

                file.write(','+str(high)+','+str(low))
              
            file.write('\n')
            
        start = end
        no +=1
file.flush()
file.close()
        



