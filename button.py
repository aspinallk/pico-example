import machine
import utime

button = machine.Pin(06, machine.Pin.IN, machine.Pin.PULL_DOWN)

while button.value() == 0:
    utime.sleep(0.1)
print("Pressed")        