# -----------------------------------------------------
# ds3231.py – RTC Driver
# -----------------------------------------------------
class DS3231:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

    def bcd2dec(self, b):
        return (b >> 4) * 10 + (b & 0x0F)

    def dec2bcd(self, d):
        return ((d // 10) << 4) | (d % 10)

    def datetime(self, dt=None):
        if dt is None:
            d = self.i2c.readfrom_mem(self.addr, 0x00, 7)
            return (
                self.bcd2dec(d[6]) + 2000,
                self.bcd2dec(d[5]),
                self.bcd2dec(d[4]),
                self.bcd2dec(d[3]),
                self.bcd2dec(d[2]),
                self.bcd2dec(d[1]),
                self.bcd2dec(d[0]),
                0
            )
        else:
            y, mo, d, wd, h, m, s, _ = dt
            buf = bytearray(7)
            buf[0] = self.dec2bcd(s)
            buf[1] = self.dec2bcd(m)
            buf[2] = self.dec2bcd(h)
            buf[3] = self.dec2bcd(wd)
            buf[4] = self.dec2bcd(d)
            buf[5] = self.dec2bcd(mo)
            buf[6] = self.dec2bcd(y - 2000)
            self.i2c.writeto_mem(self.addr, 0x00, buf)


