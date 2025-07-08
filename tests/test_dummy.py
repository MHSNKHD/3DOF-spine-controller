import serial

ser = serial.Serial('/dev/ttyUSB0', 460800, timeout=1)
print("Serial port opened successfully.")
ser.close()

