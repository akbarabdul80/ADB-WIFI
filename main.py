import os
from easygui import *
import re
import netifaces
import ipaddress
import time

if not os.path.exists('ip.txt'):
    open('ip.txt', 'w')
file = open('ip.txt', 'r+')

ip_file = ''
port_file = ''
new_ip_port = ''

def get_ip_from_subnet(ip_subnet):
    ipn = ipaddress.IPv4Network(ip_subnet, strict=False)
    ips = ipaddress.ip_network(ipn)
    ip_list = [str(ip) for ip in ips]
    return ip_list

msg = "Select the mode to use!"
choices = ["Manual", "Scan", "Cancel"]
reply = buttonbox(msg, choices=choices)

if reply == "Manual":
    readfile = file.read()
    regex = re.compile("([0-9.]+):(\d+)")
    if bool(regex.match(readfile)):
        r = regex.search(readfile)
        ip_port = r.groups()
        ip_file = ip_port[0]
        port_file = ip_port[1]
    fieldNames = ["IP", "Port"]
    fields = multenterbox('Enter IP and Port', 'ADB Connect GUI', fieldNames, [ip_file, port_file])
    ip = fields[0]
    port = fields[1]

    if ip != ip_file or port != port_file:
        file.seek(0)
        new_ip_port = ip + ':' + port
        file.write(new_ip_port)
        file.close()
    os.system('adb connect ' + new_ip_port)
else:
    availableIp = []
    for ifaceName in netifaces.interfaces():
        addresses = [i['addr'] for i in
                     netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr': 'No IP addr'}])]
        netmask = [i['netmask'] for i in
                   netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'netmask': 'No Netmask'}])]

        if addresses[0] != 'No IP addr' and addresses[0] != "127.0.0.1":
            availableIp.append(addresses[0] + "/" + netmask[0])

    command = ""
    for i in get_ip_from_subnet(unicode(availableIp[0])):
        command += 'adb connect ' + i + ' & '

    os.system(command)


def check_ip(ip):
    regex = re.compile("(\d+):(\d+):(\d+):(\d+)")
    r = regex.search(ip)
    for i in r.groups():
        if not i.isdigit:
            return False
    return True



