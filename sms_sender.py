import serial
import sys
import glob
import time
import io
import re


def port_read(port,n=1):
    for _ in range(n):
        time.sleep(0.2)
        print(port.readline())

def send_command(port,word:str, cont_answ:str,n:int,m:int):
    bin_str = io.BytesIO()
    bin_str.write(word.encode('ascii'))
    answ=None
    # i=0
    for u in range(n):
        bin_str.seek(0)
        port.write(bin_str.read())
        for _ in range(m):
            time.sleep(0.3)
            answ=str(port.readline())
            # print(i, answ)
            # i+=1
            if re.search(cont_answ,answ, re.ASCII) :
                answ     = 'OK'
                break
        if answ=='OK':
            break
    return  answ

def init_serial(COMNUM='COM1'):
    port_ser= serial.Serial()
    port_ser.baudrate = 19200
    # port_ser.dsrdtr=True
    port_ser.port = COMNUM
    port_ser.timeout = 5
    port_ser.open()
    if port_ser.isOpen():
        print('Open: ' + port_ser.__str__())
    return port_ser

def sms_send(COMNUM='COM1',phone='phone'):
    port= init_serial(COMNUM)
    port_read(port,2)

    temp='AT+ENPWRSAVE=0\r\n'
    send_command(port, temp, 'OK', 3, 4)
    temp='AT+CPAS\r\n'                                    #Проверка статуса нужен 0 или ок
    if  send_command(port, temp, 'OK', 3, 4)!='OK':
        print( "Error init 1")
    temp= 'AT+CSQ\r\n'
    if send_command(port,temp, 'OK', 3, 4)!='OK':
        print("Error init 2")
    temp = 'AT+CMGF=1\r\n'                                  # режим кодировки СМС - обычный
    if send_command(port,temp,'OK', 3, 4)!='OK':
        print("Error init 3")

    print(' point 1: ' )
    time.sleep(0.3)
    temp= 'AT+CSCS="GSM"\r\n'                                     #режим
    if send_command(port,temp, 'OK', 3, 4)!='OK':
        print("Error init 3")
    time.sleep(0.2)

    print(' point 2: ' )
    temp = 'ATD+{};\r\n'.format(phone)
    resp = send_command(port, temp, 'OK', 3, 4)
    time.sleep(0.2)
    # temp = b'base reload\r\n'

    print(" point 3:  call_started")
    time.sleep(0.5)
    print(str(temp) +"//"+ str(port.readline()))
    time.sleep(10)
    temp = 'ATH0\r\n'
    send_command(port, temp, 'OK', 3, 4)

    print(' point 4: port reading: ' + str(port.readline()))
    temp = chr(26) + '\r\n'
    if send_command(port, temp, 'OK', 3, 4) != 'OK':
        print("Error  at closing")
    print(port.__str__())

    return resp

