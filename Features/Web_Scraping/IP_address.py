import socket


def Ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ip = "Sir, Your Device name : " + hostname + " has the IP Address : " + ip_address
    return ip
