import machine
import utime
import ssd1306
import time
import binascii
import framebuf

# Melody
# MELODY_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
# MELODY_DURATION = [0.25, 0.25, 0.15, 0.25, 0.25, 0.15, 0.25, 0.15, 0.3]
# MELODY_NOTE = [659, 759, 0, 659]
# MELODY_DURATION = [0.15, 0.35, 0.15, 0.2]
MELODY_NOTE = [659, 759]
MELODY_DURATION = [0.25, 0.35]
MELODY_NOTE_ERROR = [300, 300]
MELODY_DURATION_ERROR = [0.50, 0.35]

class finger:
    
    sda = machine.Pin(16)
    scl = machine.Pin(17)
    # sda = machine.Pin(20)
    # scl = machine.Pin(21)    
    i2c = machine.I2C(0, sda = sda, scl = scl, freq=400000)
    
    display = ssd1306.SSD1306_I2C(128, 64, i2c)

    # draw another FrameBuffer on top of the current one at the given coordinates

    fbuf = framebuf.FrameBuffer(bytearray(17 * 17 * 1), 17, 17, framebuf.MONO_VLSB)
    fbuf.fill_rect(0, 0, 15, 16, 1)
    fbuf.fill_rect(0, 0, 2, 1, 0)
    fbuf.fill_rect(0, 1, 1, 1, 0)
    fbuf.fill_rect(2, 3, 3, 3, 0)
    fbuf.fill_rect(10, 0, 5, 2, 0)
    fbuf.fill_rect(8, 2, 7, 2, 0)
    fbuf.fill_rect(12, 4, 3, 2, 0)
    fbuf.fill_rect(6, 6, 9, 2, 0)
    fbuf.fill_rect(9, 8, 6, 2, 0)
    fbuf.fill_rect(11, 10, 4, 2, 0)
    fbuf.fill_rect(8, 12, 7, 2, 0)
    fbuf.fill_rect(14, 15, 1, 1, 0)
    fbuf.fill_rect(1, 14, 2, 2, 0)
    fbuf.fill_rect(5, 14, 2, 2, 0)


    fingerImage = list()

    Header = bytearray(b'\xef\x01\xff\xff\xff\xff')
    uart1 = machine.UART(1, baudrate=57600, bits=8, parity=None, rxbuf= 8192, stop=2, tx=machine.Pin(4), rx=machine.Pin(5))
    # uart1 = machine.UART(1, baudrate=57600, bits=8, parity=None, rxbuf= 8192, stop=2, tx=machine.Pin(16), rx=machine.Pin(17))
    # def __init__(self, debug = True): 
    def __init__(self, debug = False): 
       self.debug = debug
        
    def IsDebug(self):
        print('Debug is {0}'.format(self.debug))
    
    def VfyPwd(self, password = bytearray(b'\x00\x00\x00\x00')):
        if (self.debug == True): print('VfyPwd')
        VfyPwd = bytearray(b'\x01\x00\x07\x13') + password
        checksum = sum(VfyPwd).to_bytes(2,'big')
        Cmd_VfyPwd = self.Header + VfyPwd + bytearray(checksum)

        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_VfyPwd))
        
        self.uart1.write(Cmd_VfyPwd)
        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        
        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)
    
    def ReadSysPara(self):        
        if (self.debug == True): print('ReadSysPara')
        ReadSysPara = bytearray(b'\x01\x00\x03\x0f')
        checksum = sum(ReadSysPara).to_bytes(2,'big')
        Cmd_ReadSysPara = self.Header + ReadSysPara + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_ReadSysPara))

        self.uart1.write(Cmd_ReadSysPara)
        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        values = dict()
        
        values['StateRegister'] = ACK_Packet[len(ACK_Packet)-17]
        values['SensorType'] = ACK_Packet[len(ACK_Packet)-15]
        values['DataBaseSize'] = ACK_Packet[len(ACK_Packet)-13]
        values['SecurityRank'] = ACK_Packet[len(ACK_Packet)-11]
        values['DeviceAddress'] = ACK_Packet[len(ACK_Packet)-10:len(ACK_Packet)-6]
        if ACK_Packet[len(ACK_Packet)-5] == 0 : values['DatabaseSize'] = 32
        if ACK_Packet[len(ACK_Packet)-5] == 1 : values['DatabaseSize'] = 64
        if ACK_Packet[len(ACK_Packet)-5] == 2 : values['DatabaseSize'] = 128
        if ACK_Packet[len(ACK_Packet)-5] == 3 : values['DatabaseSize'] = 256
        values['BaudConfig'] = ACK_Packet[len(ACK_Packet)-3]*9600
        values['Ack'] = ACK_Packet[len(ACK_Packet)-19]
        
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        print('PARAMETER TABLE')
        print('State register: {0}'.format(values['StateRegister']))
        print('Sensor Type:    {0}'.format(values['SensorType']))
        print('Database Size:  {0} templates'.format(values['DataBaseSize']))
        print('Security Rank:  {0}'.format(values['SecurityRank']))
        print('Device Address:',binascii.hexlify(values['DeviceAddress']))
        print('Data Pack size: {0}'.format(values['DatabaseSize']))
        print('Baud Config:    {0} bps'.format(values['BaudConfig']))
        print('Ack:            {0}'.format(values['Ack']))

        return(values)
    
    def GetImage(self):
        if (self.debug == True): print('GetImage')
        GetImage = bytearray(b'\x01\x00\x03\x01')
        checksum = sum(GetImage).to_bytes(2,'big')
        Cmd_GetImage = self.Header + GetImage + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_GetImage))

        self.uart1.write(Cmd_GetImage)
        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))

        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)

    def Empty(self):
        if (self.debug == True): print('Empty Database')
        Empty = bytearray(b'\x01\x00\x03\x0d')
        checksum = sum(Empty).to_bytes(2,'big')
        Cmd_Empty = self.Header + Empty + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_Empty))

        self.uart1.write(Cmd_Empty)
        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))

        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)

    def DeleteChar(self, pageId):
        if (self.debug == True): print('DeleteChar')
        DeleteChar = bytearray(b'\x01\x00\x07\x0c') + bytearray([(pageId>>8)]) + bytearray([pageId&0x00FF]) + bytearray(b'\x00\x01')
        checksum = sum(DeleteChar).to_bytes(2,'big')
        Cmd_DeleteChar = self.Header + DeleteChar + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_DeleteChar))
        self.uart1.write(Cmd_DeleteChar)

        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)


    def IsPressFinger(self):
        '''
             Checks to see if a finger is pressed on the FPS
             Return: true if finger pressed, false if not
        '''
        pval = self.GetImage()
        retval = True if pval == 0 else False
        return retval


    def GenChar(self, buff = 1):
    
        if (self.debug == True): print('GenChar buff:{0}'.format(buff))
        if buff == 2:
            GenChar = bytearray(b'\x01\x00\x04\x02\x02')
        else:
            # Buffer 1 default
            GenChar = bytearray(b'\x01\x00\x04\x02\x01')
        checksum = sum(GenChar).to_bytes(2,'big')
        Cmd_GenChar = self.Header + GenChar + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_GenChar))

        self.uart1.write(Cmd_GenChar)
        time.sleep(1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))

        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)

    def Search(self, buff = bytearray(b'\x01'), startPage = bytearray(b'\x00\x00'), pageNum = bytearray(b'\x00\x28')):

        if (self.debug == True): print('Search')
        Search = bytearray(b'\x01\x00\x08\x04') + buff + startPage + pageNum
        checksum = sum(Search).to_bytes(2,'big')
        Cmd_Search = self.Header + Search + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_Search))
        self.uart1.write(Cmd_Search)

        time.sleep(1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        values = dict()
        ln = len(ACK_Packet)
        values['Page'] = ACK_Packet[ln-6]*256 + ACK_Packet[ln-5]
        values['Score'] = ACK_Packet[ln-4]*256 + ACK_Packet[ln-3]
        values['Ack'] = ACK_Packet[ln-7]        
        if (self.debug == True): print(values)
        return(values)

    def Match(self):

        if (self.debug == True): print('Match')
        Match = bytearray(b'\x01\x00\x03\x03')
        checksum = sum(Match).to_bytes(2,'big')
        Cmd_Match = self.Header + Match + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_Match))
        self.uart1.write(Cmd_Match)

        time.sleep(1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        values = dict()
        ln = len(ACK_Packet)
        values['Score'] = ACK_Packet[ln-2]*256 + ACK_Packet[ln-1]
        values['Ack'] = ACK_Packet[ln-5]        
        if (self.debug == True): print(values)
        return(values)


    def LoadChar(self, buff = 1, pageId = 1):
        if (self.debug == True): print('LoadChar')
        if buff == 2:
            LoadChar = bytearray(b'\x01\x00\x06\x07\x02') + bytearray([(pageId>>8)]) + bytearray([pageId&0x00FF])
        else:
            # Buffer 1 default
            LoadChar = bytearray(b'\x01\x00\x06\x07\x01') + bytearray([(pageId>>8)]) + bytearray([pageId&0x00FF])
        checksum = sum(LoadChar).to_bytes(2,'big')
        Cmd_LoadChar = self.Header + LoadChar + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_LoadChar))
        self.uart1.write(Cmd_LoadChar)

        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)


    def UpChar(self, buff = 1):
        if (self.debug == True): print('Upload feature or templates in buff {0}'.format(buff))
        if buff == 2:
            UpChar = bytearray(b'\x01\x00\x04\x08\x02')
        else:
            # Buffer 1 default
            UpChar = bytearray(b'\x01\x00\x04\x08\x01')
        checksum = sum(UpChar).to_bytes(2,'big')
        Cmd_UpChar = self.Header + UpChar + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_UpChar))
        self.uart1.write(Cmd_UpChar)

        time.sleep(0.1)
        ACK_Packet = bytes()
        ACK_Packet = self.uart1.read(12)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))

        while self.uart1.any() == 0:
            print('Waiting')
             
        time.sleep_ms(25)
        data = bytes()
        while self.uart1.any() > 0:
            data += self.uart1.read(16384)

        no = 1
        start = data.find(b'\xef\x01')
        while start != -1:
            packet = bytes()
            end = data.find(b'\xef\x01',start + 2)
            if end != -1:
                packet = data[start:end]
                ln = len(packet)
            else:
                packet = data[start:]
                ln = len(packet)
#            if (no <7): print('No:{0}'.format(no), binascii.hexlify(packet[9:ln-2]))
            print('No:{0}'.format(no), binascii.hexlify(packet[9:ln-2]))
            start = end
            no +=1

    def RegModel(self):
        if (self.debug == True): print('RegModel')
        RegModel = bytearray(b'\x01\x00\x03\x05')
        checksum = sum(RegModel).to_bytes(2,'big')
        Cmd_RegModel = self.Header + RegModel + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_RegModel))
        self.uart1.write(Cmd_RegModel)

        time.sleep(1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))        
        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)
    
    def StoreChar(self, buff = 1, pageId = 1):
        if (self.debug == True): print('StoreChar')
        if buff == 2:
            StoreChar = bytearray(b'\x01\x00\x06\x06\x02') + bytearray([(pageId>>8)]) + bytearray([pageId&0x00FF])
        else:
            # Buffer 1 default
            StoreChar = bytearray(b'\x01\x00\x06\x06\x01') + bytearray([(pageId>>8)]) + bytearray([pageId&0x00FF])
        checksum = sum(StoreChar).to_bytes(2,'big')
        Cmd_StoreChar = self.Header + StoreChar + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_StoreChar))
        self.uart1.write(Cmd_StoreChar)

        time.sleep(0.1)
        ACK_Packet = bytes()
        while self.uart1.any() > 0:
            ACK_Packet += self.uart1.read(1)

        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        ack = ACK_Packet[len(ACK_Packet)-3]
        return(ack)


    def UploadImage(self):
        print('upload image')
        retval = True
        UploadImage = bytearray(b'\x01\x00\x03\x0a')
        checksum = sum(UploadImage).to_bytes(2,'big')
        Cmd_UploadImage = self.Header + UploadImage + bytearray(checksum)
        if (self.debug == True): print('Tx: ',binascii.hexlify(Cmd_UploadImage))
        self.uart1.write(Cmd_UploadImage)

        time.sleep(0.1)
        ACK_Packet = bytes()
        ACK_Packet = self.uart1.read(12)
        if (self.debug == True): print('Rx: ',binascii.hexlify(ACK_Packet))
        while self.uart1.any() == 0:
            if (self.debug == True): print('Waiting')    
        time.sleep_ms(25)
        data = bytes()
        count = 0

        # Stall while waiting for data to be sent 
        while self.uart1.any() == 0:
            if (self.debug == True): print('Waiting for Data')
            time.sleep_ms(1)

        # Read enough data to get the image portion          
        if (self.debug == True): print('Reading1')
        try:
            # A hard coded exception for testing reset
            # raise MemoryError('My memory error')
            data += self.uart1.read(31510)
        except MemoryError:
            retval = False

        # Empty buffer of scrap data 
        prog = 0        
        while self.uart1.any() > 0:
            if (self.debug == True): print('Scrap!')
    #       scrap = self.uart1.read(2048)
            try:
                scrap = self.uart1.read(2048)
                self.display.fill(0)
                if (prog==0):
                    self.display.text('Analysing.   ', 10, 24, 1)
                    prog = 1
                elif (prog==1):
                    self.display.text('Analysing..  ', 10, 24, 1)
                    prog = 2
                elif (prog==2):
                    self.display.text('Analysing... ', 10, 24, 1)
                    prog = 3
                elif (prog==3):
                    self.display.text('Analysing....', 10, 24, 1)
                    prog = 4
                elif (prog==4):
                    self.display.text('Analysing... ', 10, 24, 1)
                    prog = 5                    
                elif (prog==5):
                    self.display.text('Analysing..  ', 10, 24, 1)
                    prog = 6
                elif (prog==6):
                    self.display.text('Analysing.   ', 10, 24, 1)
                    prog = 7 
                elif (prog==7):
                    self.display.text('Analysing    ', 10, 24, 1)
                    prog = 0 

                self.display.show()

            except MemoryError:
                retval = False

        if (retval == True): 
            self.display.fill(0)       
            self.display.text('Generating', 10, 24, 1)            
            self.display.text('unique code', 10, 34, 1)
            self.display.show()

            self.fingerImage.clear()
            end = 0
            no = 1        
            start = data.find(b'\xef\x01')
            
            while (start != -1):
                packet = bytes()
                end = data.find(b'\xef\x01',start + 2)            
                # image is 80 bytes in centre of records 65 to 224
                if no>64 and no<225:
                    packet = data[start+33:start+113]

                    if (self.debug == True): print('No: {0} '.format(no),binascii.hexlify(packet),"   ", len(packet))
                    high = packet[0]>>4
                    low = packet[0]&0x0F
                    expandedPacket = bytearray([high]) + bytearray([low])
                    for i in range(79):
                        high = packet[i]>>4
                        low = packet[i]&0x0F
                        expandedPacket = expandedPacket + bytearray([high]) + bytearray([low])
                    self.fingerImage.append(expandedPacket)                                   
                start = end
                no +=1
        else:
            print('data Try Caught MemoryError')

        return retval


    def PrintImage(self):
        for x in self.fingerImage:
            print('fingerImage: ',x)    
        return 0

    def Display(self):
        self.display.fill(0)

        time.sleep_ms(1000)
#         self.display.fill(0)
#         self.display.show()
        y = 0
        for i in self.fingerImage:
            y += 1
            if y < 54:
                for x in range(80):
                    if i[(x-1)*2] < 10: self.display.pixel(x+20, y, 0)
                    if i[(x-1)*2] > 9: self.display.pixel(x+20, y, 1) 
        self.display.show()

        # Generate unique code...
        code = 0        
        for i in self.fingerImage:
            for x in range(80):
                code = code + i[(x-1)]*256 + i[(x-1)*2]
        print('code = ',code)
        # Range +/- 1000000                
        code2 = (code % 2000000)-1000000
        self.display.text(str(code2), 30, 56, 1)
        self.display.show()
        
    def Display2(self):
        self.display.fill(0)
        self.display.text('Hello, World!', 0, 0, 1)
        self.display.show()
        time.sleep_ms(1000)
        self.display.fill(0)
        self.display.show()
        y = 0
        for i in self.fingerImage:
            y += 1
            if y == (y/2)*2:
                for x in range(80):
                    if i[(x-1)*2] < 10: self.display.pixel(x, y, 0)
                    if i[(x-1)*2] > 9: self.display.pixel(x, y, 1) 
        self.display.show()

    def enrol(self, pageId = 1):

        print('Place finger x1')
        while not self.IsPressFinger():
            time.sleep(1)
        if self.GenChar(buff=1) == 0:
            print('Generated Image x1')
            print('Remove Finger')
            while self.IsPressFinger():
                time.sleep(1)            
            print('Place finger x2')
            while not self.IsPressFinger():
                time.sleep(1)
            if self.GenChar(buff=2) == 0:
                print('Generated Image x2')
                print('Remove Finger')
                while self.IsPressFinger():
                    time.sleep(1)            
                print('Place finger x3')
                while not self.IsPressFinger():
                    time.sleep(1)
                if self.GenChar(buff=3) == 0:
                    print('Generated Image x3')
                    print('Remove Finger')
                    while self.IsPressFinger():
                        time.sleep(1)            
                    print('Place finger x4')
                    while not self.IsPressFinger():
                        time.sleep(1)
                    if self.GenChar(buff=4) == 0:
                        print('Generated Image x4')
                        print('Remove Finger')
                        while self.IsPressFinger():
                            time.sleep(1)            
                        if self.RegModel() == 0:
                            print('Model Registered')
                            if self.StoreChar(buff = 1, pageId = pageId) == 0:
                                print('Store {0}'.format(pageId))
                            else:
                                print('Failed to Store {0}'.format(pageId))
                                return(1)
                        else:
                            print('Failed to Register Model')
                            return(1)
                    else:    
                        print('Failed to Generate x4')
                        return(1)
                else:    
                    print('Failed to Generate x3')
                    return(1)
            else:    
                print('Failed to Generate x2')
                return(1)
        else:    
            print('Failed to Generate x1')
            return(1)
        return(0)
        

    def find(self):

        print('Place finger')
        while not self.IsPressFinger():
            time.sleep(1)
        if self.GenChar(buff=1) == 0:
            print('Generated Image')
            print('Remove Finger')
            while self.IsPressFinger():
                time.sleep(1)
            print('Searching...')
            retval = self.Search()
        else:    
            print('Failed to Generate')
            return(1)
        return(retval)
        
    def Scan(self):
        print('Place Finger')
        self.display.fill(0)
        self.display.text('Place finger', 20, 24, 1)
        self.display.text('on sensor', 20, 34, 1)
        self.display.show()
        while not self.IsPressFinger():
            time.sleep(1)
        self.display.fill(0)
        self.display.text('Release finger', 10, 24, 1)
        self.display.show()
#         self.display.text('on sensor', 20, 34, 1)            
        self.UploadImage()
        return(0)

# Start of code...

beeper = machine.PWM(machine.Pin(26))

a = finger()

while True:        
    print('Place Finger')
    # Wait for finger press
    i=0
    while not a.IsPressFinger():
        a.display.fill(0)
        a.display.text('Place finger', 20, 20, 1)
        a.display.text('on sensor', 20, 30, 1)
        # Display walking ghost (no need for wait as these slow down the loop)
        a.display.blit(a.fbuf, 128-i, 45, 0)
        a.display.blit(a.fbuf, 150-i, 45, 0)
        a.display.blit(a.fbuf, 190-i, 45, 0)
        a.display.show()
        i=i+1
        if(i==206): i=0
        # utime.sleep(0.005)

    a.display.fill(0)
    a.display.text('Release finger', 10, 24, 1)
    a.display.show() 
    
    for i in range(len(MELODY_NOTE)):
        # Play melody tones
        if (MELODY_NOTE[i] > 0):
            beeper.freq(MELODY_NOTE[i])
            beeper.duty_u16(2512)
        else:
            beeper.deinit()
        utime.sleep(MELODY_DURATION[i])
    beeper.deinit()

    # Wait for finger lift
    while a.IsPressFinger():
        utime.sleep(0.01)

    a.display.fill(0)
    a.display.text('Reading data', 10, 24, 1)
    a.display.show()
    
    if (a.UploadImage() == True):
        a.Display()      
    else:
        a.display.fill(0)
        a.display.text('Ooops!', 40, 0, 1)
        a.display.text('I had a problem', 0, 24, 1)
        a.display.show()

        for i in range(len(MELODY_NOTE_ERROR)):
            # Play melody tones
            if (MELODY_NOTE_ERROR[i] > 0):
                beeper.freq(MELODY_NOTE_ERROR[i])
                beeper.duty_u16(2512)
            else:
                beeper.deinit()
            utime.sleep(MELODY_DURATION_ERROR[i])
        beeper.deinit()

        # Wait then hard reset
        time.sleep(3)
        machine.reset()
    
    # Wait for next person
    c=99
    while ((not a.IsPressFinger()) and (c>0)):
        b = str(c)
        if (c<10):b=" "+b
        c=c-1
        a.display.fill_rect(110, 5, 20, 10, 0)
        a.display.text(b, 110, 5, 1)
        a.display.show()
        utime.sleep(0.9)
    

        
