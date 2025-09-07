import serial
from serial.tools.list_ports import comports
import time

available = comports()
print(available[0].device)
ser = serial.Serial(
    available[0].device, timeout = 1,
    stopbits=1,
    bytesize = 8
    )
ser.write(f'OUT:1\r'.encode('ASCII'))
ser.write(f'PRIORITY:1\r'.encode('ASCII'))
ser.write(f'*IDN?\r'.encode('ASCII'))
print(ser.readline().decode())
ser.write(f'STATUS?\r'.encode('ASCII'))
print(ser.readline())
ser.write(f'PRIORITY?\r'.encode('ASCII'))
print(ser.readline().decode())
ser.write(f'OCP?\r'.encode('ASCII'))
print(ser.readline().decode())
ser.write(f'OVP?\r'.encode('ASCII'))
print(ser.readline().decode())
start_time = time.time()
while True:
    if time.time() - start_time > 60:
        break
    time.sleep(1)
    ser.write(b'IOUT?\r')#((b'IOUT?\r').encode('ASCII'))
    iout = ser.readline().decode()[:-1]
    ser.write(b'VOUT?\r')#((b'VOUT?\r').encode('ASCII'))
    vout = ser.readline().decode()[:-1]
    ser.write(b'IOUT?\r')#((b'IOUT?\r').encode('ASCII'))
    iset = ser.readline().decode()[:-1]
    ser.write(b'VOUT?\r')#((b'VOUT?\r').encode('ASCII'))
    vset = ser.readline().decode()[:-1]
    print(vout, vset)
    print(iout, iset)
    print()

ser.write(f'OUT:0\r'.encode('ASCII'))
ser.close()
