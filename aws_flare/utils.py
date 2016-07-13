import ipaddress


def is_private(cidr):
    return ipaddress.ip_network(cidr).is_private


def in_network(cidr, network):
    return ipaddress.ip_network(cidr) in ipaddress.ip_network(network)