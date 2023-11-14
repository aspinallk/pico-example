from machine import UART, Pin
import time
import binascii

uart1 = UART(1, baudrate=57600, bits=8, parity=None, rxbuf= 16384, stop=2, tx=Pin(4), rx=Pin(5))

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

print('Rx: ',binascii.hexlify(ACK_Packet))

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

print('Rx: ',binascii.hexlify(ACK_Packet))


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

print('Rx: ',binascii.hexlify(ACK_Packet))

ack = ACK_Packet[len(ACK_Packet)-3]
print(ack)

if ack == 0 :
    print()
    print('Generate Feature in buff#1')
    GenChar = bytearray(b'\x01\x00\x04\x02\x01')
    checksum = sum(GenChar).to_bytes(2,'big')
    Cmd_GenChar = Header + GenChar + bytearray(checksum)

    print('Tx: ',binascii.hexlify(Cmd_GenChar))

    uart1.write(Cmd_GenChar)

    time.sleep(1)

    ACK_Packet = bytes()
    while uart1.any() > 0:
        ACK_Packet += uart1.read(1)

    print('Rx: ',binascii.hexlify(ACK_Packet))

    ack = ACK_Packet[len(ACK_Packet)-3]
    print(ack)

    if ack == 0 :
        print()
        print('upload feature or templates in buff#1')
        UpChar = bytearray(b'\x01\x00\x04\x08\x01')
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
             
        time.sleep_ms(25)
        data = bytes()
        while uart1.any() > 0:
            data += uart1.read(16384)

        no = 1
        start = data.find(b'\xef\x01')
        while start != -1:
            packet = bytes()
            end = data.find(b'\xef\x01',start + 2)
            print('start, end: ', start,end)
            if end != -1:
                packet = data[start:end]
                print('No: ',no)
                print('R6: ',binascii.hexlify(packet),"   ", len(packet))
                print('Cks: ', checksum)
            else:
                packet = data[start:]
                print('R6: ',binascii.hexlify(packet),"   ", len(packet))
            start = end
            no +=1


