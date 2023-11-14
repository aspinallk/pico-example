import machine
import ssd1306

sda = machine.Pin(16)
scl = machine.Pin(17)
i2c = machine.I2C(0, sda = sda, scl = scl, freq=400000)
print(i2c.scan())


# using default address 0x3C

display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text('Hello, World!', 0, 0, 1)
display.show()
display.rotate(True)
display.contrast(90) 

display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('MicroPython', 40, 0, 2)
display.text('SSD1306', 40, 12, 2)
display.text('OLED 128x64', 40, 24, 2)
b = str(123)
display.text(b, 40, 34, 2)
display.show()



