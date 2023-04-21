import os


def get_ip(my_mac=''):
    os.system("adb tcpip 5555")
    check = os.popen('arp -a').readlines()
    for i in check:
        i = i.split()

        if len(i) == 3:
            ip = i[0]
            mac = i[1]

            if my_mac != '':
                if my_mac == mac:
                    return ip

            else:
                print(mac, '-->', ip)
                pass


def Connect():
    ip1 = get_ip('02-37-cc-6e-21-aa') # Call get_ip Function and Find Your Phone IP address with has "02-37-cc-6e-21-aa" this kind of Address
    os.system(f'adb connect {ip1}')
