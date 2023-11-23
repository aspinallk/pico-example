import machine 
import time

led = machine.Pin("LED", machine.Pin.OUT)

for n in range(20):
    led.toggle()
    time.sleep(0.250)
        
time.sleep(5)
machine.reset()

