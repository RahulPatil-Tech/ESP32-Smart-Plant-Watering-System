import framebuf
import time

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr

        self.buffer = bytearray(width * height // 8)
        self.fb = framebuf.FrameBuffer(
            self.buffer, width, height, framebuf.MONO_VLSB
        )

        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, b'\x00' + bytes([cmd]))

    def init_display(self):
        cmds = [
            0xAE,       # Display OFF
            0x20, 0x00, # Horizontal addressing mode
            0x40,       # Start line = 0
            0xA1,       # Segment remap
            0xC8,       # COM scan direction
            0x81, 0x7F, # Contrast
            0xA6,       # Normal display
            0xA8, self.height - 1,  # Multiplex
            0xD3, 0x00, # Display offset
            0xD5, 0x80, # Clock divide
            0xD9, 0xF1, # Pre-charge
            0xDA, 0x12, # COM pins
            0xDB, 0x40, # VCOM detect
            0x8D, 0x14, # Charge pump
            0xA4,       # Display RAM
            0xAF        # Display ON
        ]

        for cmd in cmds:
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def show(self):
        self.write_cmd(0x21)  # Column address
        self.write_cmd(0)
        self.write_cmd(self.width - 1)

        self.write_cmd(0x22)  # Page address
        self.write_cmd(0)
        self.write_cmd((self.height // 8) - 1)

        self.i2c.writeto(self.addr, b'\x40' + self.buffer)

    def fill(self, c):
        self.fb.fill(c)

    def text(self, s, x, y):
        self.fb.text(s, x, y)
      
    def scroll_yellow_text(self, text, speed=1):
        if not hasattr(self, "_scroll_x"):
            self._scroll_x = self.width

        text_width = len(text) * 8

        self.text(text, self._scroll_x, 0)
        self._scroll_x -= speed

        if self._scroll_x < -text_width:
            self._scroll_x = self.width

