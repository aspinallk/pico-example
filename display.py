import machine
import ssd1306
import time

sda = machine.Pin(16)
scl = machine.Pin(17)
i2c = machine.I2C(0, sda = sda, scl = scl, freq=400000)
print(i2c.scan())


# using default address 0x3C

display = ssd1306.SSD1306_I2C(128, 64, i2c)

# display.text('Hello, World!', 0, 0, 1)
display.show()
display.rotate(True)
display.contrast(90) 

# display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# display.vline(9, 8, 22, 1)
# display.vline(16, 2, 22, 1)
# display.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 2)
# display.text('SSD1306', 40, 12, 2)
# display.text('OLED 128x64', 40, 24, 2)
# b = str(123)
# display.text(b, 40, 34, 2)
# display.show()

# draw another FrameBuffer on top of the current one at the given coordinates
import framebuf
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

while True:
    for i in range(144):
        display.fill(0)
        display.text('Place finger', 20, 20, 1)
        display.text('on sensor', 20, 30, 1)

        display.blit(fbuf, 128-i, 45, 0)           # draw on top at x=10, y=10, key=0
        # display.blit(fbuf, 128-i, 45, 0)           # draw on top at x=10, y=10, key=0

        display.show()
        time.sleep(0.02)
