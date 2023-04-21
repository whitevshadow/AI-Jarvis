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
    ip1 = get_ip('02-37-cc-6e-21-aa')
    os.system(f'adb connect {ip1}')
    ip2 = get_ip('fa-ef-3b-99-67-fa')
    os.system(f"adb connect {ip2}")
    ip3 = get_ip('72-ad-6b-4b-83-b5')
    os.system(f"adb connect {ip3}")

