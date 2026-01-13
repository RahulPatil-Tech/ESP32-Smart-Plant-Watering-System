from machine import Pin, I2C, SoftI2C
import time
import network
import ntptime
# import ssd1306
from tm1637 import TM1637
from ds3231 import DS3231


# ===========================
#  SETTINGS
# ===========================
SSID     = "SSID NAME"
PASSWORD = "password"

# IST offset (UTC + 5:30)
IST_OFFSET = 5*3600 + 30*60

# Watering schedule (HH,MM)
WATER_TIMES = [(10,0), (13,0), (17,0), (19,40)]
WATER_DURATION = 5   # seconds


# ===========================
#  HARDWARE
# ===========================
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
rtc = DS3231(i2c)

#oled_width = 128
#oled_height = 64
#oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


tm = TM1637(clk=Pin(4), dio=Pin(2))

PUMP_PIN = 14
pump = Pin(PUMP_PIN, Pin.OUT)
pump.value(1)

# Prevent multiple triggers in same day
last_trigger = {(h, m): -1 for (h, m) in WATER_TIMES}


# ===========================
#  WIFI + NTP
# ===========================
def sync_time_ntp():
    wlan = network.WLAN(network.STA_IF)

    wlan.active(False)
    time.sleep(0.2)
    wlan.active(True)

    wlan.disconnect()
    wlan.connect(SSID, PASSWORD)

    timeout = 4
    while not wlan.isconnected() and timeout > 0:
        #oled.fill(0)
        #oled.text(f"Connecting WiFi...{timeout}",0,5)
        print(f"Connecting WiFi...{timeout}")
        time.sleep(1)
        timeout -= 1

    if not wlan.isconnected():
        #oled.text(f"⚠️ No WiFi — using DS3231 battery time",0,10)
        print(f"⚠️ No WiFi — using DS3231 battery time")
        return

    ntptime.host = "pool.ntp.org"

    for i in range(5):
        try:
            print("🔄 NTP attempt:", i+1)
            ntptime.settime()
            break
        except Exception as e:
            print("NTP error:", e)
            time.sleep(1)
    else:
        print("⚠️ NTP failed after 5 attempts")
        return

    t = time.time() + IST_OFFSET
    t_local = time.localtime(t)

    rtc.datetime((
        t_local[0], t_local[1], t_local[2], t_local[6],
        t_local[3], t_local[4], t_local[5], 0
    ))
    #oled.fill(0)
    #oled.text(f"✔️ Time synced to IST",0,20)
    print(f"✔️ Time synced to IST")


# ===========================
#  PUMP CONTROL
# ===========================
def run_pump(h, m):
    print("💧 Pump START:", h, m)
    pump.value(0)
    time.sleep(WATER_DURATION)
    pump.value(1)
    print("💧 Pump STOP")


# ===========================
#  MAIN LOOP
# ===========================
sync_time_ntp()
time.sleep(0)

while True:
    y, mo, d, wd, h, m, s, ms = rtc.datetime()

    #oled.text(f"{h:02d}:{m:02d}", 0, 5)
    #oled.show()
    # Auto brightness
    if 22 <= h or h < 6:
        tm.set_brightness(1)
    else:
        tm.set_brightness(7)

    tm.numbers(h, m)
    #print(f"{h:02d}:{m:02d}")


    for (hh, mm) in WATER_TIMES:
        if h == hh and m == mm and last_trigger[(hh, mm)] != d:
            run_pump(hh, mm)
            last_trigger[(hh, mm)] = d

    time.sleep(0)

