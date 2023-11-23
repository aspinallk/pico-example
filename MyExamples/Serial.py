from machine import UART, Pin
import time
import binascii

uart1 = UART(1, baudrate=9600, bits=8, parity=None, stop=2, tx=Pin(8), rx=Pin(9))

#uart1.init(baudrate=9600, bits=8, parity=None, stop=2)

#txData = b'hello world\n\r'

txData = bytearray(b'\x00\x65\x6c\x6c\x6f\x20')
print('One:',txData)
txData += bytearray(b'\x57\x6f\x72\x6c\x64\x21')
#txData = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21'
print('Two:',txData)
#txData = b'\x2f\x34\x38'
#txData = b'\x48\x65'

uart1.write(txData)


time.sleep(0.1)
rxData = bytes()
while uart1.any() > 0:
    rxData += uart1.read(1)

temp_byte = b'\x48'
print('Byte:',temp_byte)
temp_hex = binascii.hexlify(temp_byte)
print('Hex: ',temp_hex)
print('Byte:',binascii.unhexlify(temp_hex))
print('Decoded:',temp_byte.decode('utf-8'))
print()
print(binascii.hexlify(txData))
print(txData)
print(txData.decode('utf-8'))




