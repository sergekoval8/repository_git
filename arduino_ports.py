import serial.tools.list_ports as port_list


def serial_ports():
    ports = list(port_list.comports())
    result_list=[]
    for port in ports:
        try:
            if port.__getattribute__('vid') is None:
                continue
            res= (port.__getattribute__('device'), port.__getattribute__('description'))
            if res in result_list:
                continue
            result_list.append(res)
        except AttributeError:
            pass
    return result_list
