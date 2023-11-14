from neopixel import Neopixel
import utime

# Initialize Neopixel RGB LEDs
pixels = Neopixel(2, 0, 18, "GRB")
pixels.fill((220,0,0))


color = 0
state = 0

# Animate RGB LEDs
while True:
    if state == 0:
        if color < 0x101010:
            color += 0x010101   # increase rgb colors to 0x10 each
        else:
            state += 1
    elif state == 1:
        if (color & 0x00FF00) > 0:
            color -= 0x000100   # decrease green to zero
        else:
            state += 1
    elif state == 2:
        if (color & 0xFF0000) > 0:
            color -= 0x010000   # decrease red to zero
        else:
            state += 1
    elif state == 3:
        if (color & 0x00FF00) < 0x1000:
            color += 0x000100   # increase green to 0x10
        else:
            state += 1
    elif state == 4:
        if (color & 0x0000FF) > 0:
            color -= 1          # decrease blue to zero
        else:
            state += 1
    elif state == 5:
        if (color & 0xFF0000) < 0x100000:
            color += 0x010000   # increase red to 0x10
        else:
            state += 1
    elif state == 6:
        if (color & 0x00FF00) > 0:
            color -= 0x000100   # decrease green to zero
        else:
            state += 1
    elif state == 7:
        if (color & 0x00FFFF) < 0x001010:
            color += 0x000101   # increase gb to 0x10
        else:
            state = 1
    pixels.fill((color & 0x0000FF, (color & 0x00FF00)/256,(color & 0xFF0000)/(256*256) ))  # fill the color on both RGB LEDs
    pixels.show()
    utime.sleep(0.01)
