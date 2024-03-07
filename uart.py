# installed pyserial - pip3 install pyserial
import serial.tools.list_ports

def get_ports():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])

    # return commPort
    print(commPort)
    return "/dev/ttys010"

if get_ports() != "None":
    ser = serial.Serial(port=get_ports(), baudrate=115200)
    print("Connected to: " + str(ser))

mess = ""
def process_data(client, data):
    print("[DEBUG] Processing data: " + data)
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sensor1", splitData[2])
    elif splitData[1] == "L":
        client.publish("sensor2", splitData[2])
    elif splitData[1] == "H":
        client.publish("sensor3", splitData[2])

def read_serial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            process_data(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]