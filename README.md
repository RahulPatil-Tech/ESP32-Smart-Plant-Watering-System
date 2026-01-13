# 🌱 ESP32 Smart Plant Watering System

An **ESP32-based automatic plant watering system** built using **MicroPython**, featuring **DS3231 RTC**, **TM1637 4-digit display**, optional **SSD1306 OLED**, and **WiFi NTP time synchronization (IST)**.

---

## ✨ Features

- ⏰ Accurate timekeeping with **DS3231 RTC** (battery-backed)
- 🌐 **WiFi + NTP** time synchronization (IST timezone)
- 💧 Automatic watering at predefined schedules
- 🔁 Prevents multiple watering events on the same day
- 🔢 **TM1637 display** shows live time (auto brightness)
- 📟 Optional **SSD1306 OLED** support
- 🔌 Relay-controlled water pump
- ⚡ Low-power & standalone operation

---

## 🧩 Hardware Requirements

- ESP32 Dev Board  
- DS3231 RTC Module  
- TM1637 4-Digit Display  
- Relay Module + Water Pump  
- (Optional) SSD1306 OLED Display (128x64)  
- Power Supply, Tubes, Water Source  

---

## 📁 Project Structure
```
ESP32-Smart-Watering/
│
├── main.py  # Main application logic
├── ds3231.py  # DS3231 RTC driver
├── tm1637.py  # TM1637 display driver
├── ssd1306_custom.py  # Custom SSD1306 OLED driver (optional)
├── wiring.md  # Wiring & GPIO connections
└── README.md  # Project documentation
```


---

## 🔌 GPIO Connections

| Component      | ESP32 Pin |
|----------------|----------|
| DS3231 SDA     | GPIO 21  |
| DS3231 SCL     | GPIO 22  |
| TM1637 CLK     | GPIO 4   |
| TM1637 DIO     | GPIO 2   |
| Relay / Pump  | GPIO 14  |

---

## 🌐 WiFi & Time Sync

```python
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

# IST Offset (UTC +5:30)
IST_OFFSET = 5*3600 + 30*60
```
- Syncs time from **pool.ntp.org**
- Automatically falls back to **DS3231 RTC** if WiFi is unavailable

---

## 📟 Display Behavior

### TM1637
- Displays **HH:MM**
- Auto brightness control:
  - 🌙 Night (22:00–06:00) → Dim
  - ☀️ Day → Bright

### OLED (Optional)
- Displays status messages
- Supports **scrolling text**

---

## 🚀 How to Run

1. Flash **MicroPython** on ESP32
2. Upload project files using **Thonny / mpremote / ampy**
3. Update WiFi credentials in `main.py`
4. Connect all hardware components
5. Power ON 🚀

---

## 🧠 Future Improvements

- 🌧 Soil moisture sensor integration
- 🌍 Web dashboard (ESP32 WebServer)
- 📱 MQTT / Home Assistant support
- ⏸ Manual override button
- ☔ Rain-delay logic

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Rahul Patil**  
Embedded Systems | ESP32 | IoT | MicroPython

