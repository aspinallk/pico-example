from machine import Pin, PWM
import utime

# Melody
# MELODY_NOTE = [659, 759, 0, 659]
# MELODY_DURATION = [0.15, 0.35, 0.15, 0.2]
# MELODY_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
# MELODY_DURATION = [0.25, 0.25, 0.15, 0.25, 0.25, 0.15, 0.25, 0.15, 0.3]
# MELODY_NOTE = [659, 759, 0, 659]
# MELODY_DURATION = [0.15, 0.35, 0.15, 0.2]
MELODY_NOTE = [300, 300]
MELODY_DURATION = [0.50, 0.35]

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