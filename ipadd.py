import ipaddress


def get_ip_from_subnet(ip_subnet):
    ipn = ipaddress.IPv4Network(ip_subnet, strict=False)
    ips = ipaddress.ip_network(ipn)
    ip_list = [str(ip) for ip in ips]
    return ip_list


ip_subnet = "192.168.2.16/28"
print(get_ip_from_subnet(unicode(ip_subnet)))
