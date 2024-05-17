#----------------------------------------
#-- Initial
#----------------------------------------
import RPi.GPIO as GPIO
import serial
import time
import requests

from datetime import datetime
from influxdb import InfluxDBClient

# InfluxDB
client = InfluxDBClient("localhost", 8086, "", "", "randx")

# GPIO
#Pin_Dipp = [21, 26, 20, 19, 16, 13, 6,12]   # Dipp-SW V00
Pin_Dipp = [21, 26, 20, 19, 16, 12, 7, 5]   # Dipp-SW V01
Pin_TX = 14                                 # UART-TX
Pin_RX = 15                                 # UART-RX
Pin_AUX = 24                                # AUX
Pin_M0 = 23                                 # M0
Pin_M1 = 25                                 # M1
Pin_B1 = 13

# UART
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)

# GPIO initialize
def initialize_gpio():
    GPIO.setmode(GPIO.BCM)

    # Dipp
    for pin in Pin_Dipp:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Pin_M0 and Pin_M1 (Output, initial value: Low)
    GPIO.setup(Pin_M0, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Pin_M1, GPIO.OUT, initial=GPIO.LOW)

    # Pin_AUX (Input)
    GPIO.setup(Pin_AUX, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Pin_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#----------------------------------------
#-- LoRa
#----------------------------------------
# LoRa flush
def flush_LoRa():
    time.sleep(0.1)
    if uart.in_waiting:
        print("LoRa Recv:", end="")
        while uart.in_waiting:
            data_byte = uart.read(1)
            print(format(int.from_bytes(data_byte, 'big'), '02X'), end="")
            time.sleep(0.01)
        print()

# LoRa Send
def send_LoRa(data, count):
    for i in range(count):
        uart.write(data[i].to_bytes(1, 'big'))

# LoRa Initialize
def initialize_LoRa():
    # Read Dipp-SW
    wDip = [GPIO.input(pin) for pin in Pin_Dipp]
    dDip = [not value for value in wDip]
    print("Dipp: ", dDip)

    # Get LoRa Reg
    GPIO.output(Pin_M0,1)
    GPIO.output(Pin_M1,1)
    time.sleep(0.05)
    flush_LoRa()

    LoRaDat = [0xC1, 0x00, 0x08]
    LoRaCnt = 3
    send_LoRa(LoRaDat, LoRaCnt)

    while uart.in_waiting < 11:
        pass

    if uart.in_waiting == 11:
        # Dummy read
        for _ in range(3):
            dummy = uart.read()
        while uart.in_waiting:
            LoRaReg = uart.read(8)
            time.sleep(0.01)
        hex_data = ' '.join('{:02X}'.format(byte) for byte in LoRaReg)
        print(f"Reg : {hex_data}")
    else:
        print("LoRa Error!")

    # Set LoRa
    LORA_BASE_ADD = 0x0200
    LORA_DB_ADD = 0x7F                      # DB Address Fixed
    LORA_BASE_CH = 0x00

    myPow = (dDip[0] * 2) + (dDip[1] * 1)
    myAdr = LORA_DB_ADD + LORA_BASE_ADD
    myCh = (dDip[3] * 16) + (dDip[4] * 8) + (dDip[5] * 4) + (dDip[6] * 2) + (dDip[7] * 1) + LORA_BASE_CH

    RegDef = [0xC0, 0x00, 0x08, 0x00, 0x00, 0x62, 0x00, 0x0F, 0x43, 0x00, 0x00]
    LoRaDat = RegDef.copy()

    # Make Register
    LoRaDat[3 + 0] = (myAdr >> 8) & 0xFF
    LoRaDat[3 + 1] = myAdr & 0xFF
    speed_mapping = {0: 0x62, 1: 0x6E, 2: 0x75, 3: 0x70}
    LoRaDat[3 + 2] = speed_mapping.get(myPow, 0x00)
    LoRaDat[3 + 4] = myCh

    # Register Update
    isMatch = all(LoRaReg[i] == LoRaDat[i + 3] for i in range(8))
    print("Set :", " ".join([format(x, '02X') for x in LoRaDat[3:11]]))

    if isMatch:
        print("LoRa No update!")
    else:
        LoRaCnt = 11
        send_LoRa(LoRaDat, LoRaCnt)
        flush_LoRa()
        print("LoRa Setup Finish!")

    GPIO.output(Pin_M0,0)
    GPIO.output(Pin_M1,0)
    time.sleep(0.05)

#----------------------------------------
#-- Influx
#----------------------------------------
# InfluxDB Upload
def write_to_influxdb(id, cur_data,vBat):
    json_body = [
        {
            "measurement": "RandxCL",
            "tags": {
                "ID": id
            },
            "fields": {
                "CUR1": cur_data[0],
                "CUR2": cur_data[1],
                "CUR3": cur_data[2],
                "CUR4": cur_data[3],
                "CUR5": cur_data[4],
                "CUR6": cur_data[5],
                "CUR7": cur_data[6],
                "CUR8": cur_data[7],
                "Bat" : vBat,
            }
        }
    ]

    try:
        # UPLOAD
        client.write_points(json_body)
        print("InfluxDB Write: OK")
    except Exception as e:
        print(f"Influx Error: {e}")

#----------------------------------------
#-- Main
#----------------------------------------
def main():
    initialize_gpio()
    initialize_LoRa()

    try:
        while True:
            # UART Check
            while uart.in_waiting:
                time.sleep(0.05)
                if uart.in_waiting > 23:
                    receive_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]     # datetime get
                    uart_data = uart.read(24)                                               # UART
                    hex_data = ''.join('{:02x}'.format(byte) for byte in uart_data)
                    print(f"UART:{receive_time} : {hex_data}")

                    id = ''.join('{:02X}'.format(byte) for byte in uart_data[:6])           # 0-5
                    vBat = int(uart_data[6]) * 3.6 / 256                                    # 6
                    # 2Byte単位の電流を取り出す
                    cur_data = [int.from_bytes(uart_data[i:i+2], byteorder='big') / 100.0 for i in range(7, 23, 2)]
                    print(f"ID: {id}  BAT: {vBat:.2f}V |  Cur: {cur_data}")

                    # UPLOAD
                    write_to_influxdb(id, cur_data,vBat)
                else:
                    uart.reset_input_buffer()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()
        uart.close()

if __name__ == "__main__":
    main()
