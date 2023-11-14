from machine import Pin, PWM
import utime

# Melody
MELODY_NOTE = [659, 759, 0, 659]
MELODY_DURATION = [0.15, 0.35, 0.15, 0.2]

beeper = PWM(Pin(22))
# beeper.freq(500)
# beeper.duty_u16(4000)
# 
# utime.sleep(0.8)
# beeper.deinit()

for i in range(len(MELODY_NOTE)):
    # Play melody tones
    if (MELODY_NOTE[i] > 0):
        beeper.freq(MELODY_NOTE[i])
        beeper.duty_u16(2512)
    else:
        beeper.deinit()
    utime.sleep(MELODY_DURATION[i])
beeper.deinit()