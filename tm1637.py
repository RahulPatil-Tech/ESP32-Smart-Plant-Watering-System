# =====================================================
# NORMAL MicroPython DRIVERS
# =====================================================

# -----------------------------------------------------
# tm1637.py  – 4-Digit Display Driver
# -----------------------------------------------------
from machine import Pin

class TM1637:
    DIGITS = [
        0x3F, 0x06, 0x5B, 0x4F, 0x66,
        0x6D, 0x7D, 0x07, 0x7F, 0x6F
    ]

    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        self.clk.init(Pin.OUT)
        self.dio.init(Pin.OUT)
        self.brightness = 7
        self.command(0x40)
        self.set_brightness(7)

    def start(self):
        self.dio(1)
        self.clk(1)
        self.dio(0)

    def stop(self):
        self.clk(1)
        self.dio(1)

    def write_byte(self, b):
        for _ in range(8):
            self.clk(0)
            self.dio(b & 1)
            b >>= 1
            self.clk(1)
        self.clk(0)
        self.dio(1)
        self.clk(1)

    def command(self, cmd):
        self.start()
        self.write_byte(cmd)
        self.stop()

    def set_brightness(self, val):
        if val < 0: val = 0
        if val > 7: val = 7
        self.command(0x88 | val)

    def numbers(self, h, m):
        data = [
            self.DIGITS[h // 10],
            self.DIGITS[h % 10] | 0x80,
            self.DIGITS[m // 10],
            self.DIGITS[m % 10]
        ]
        self.start()
        self.write_byte(0xC0)
        for d in data:
            self.write_byte(d)
        self.stop()
