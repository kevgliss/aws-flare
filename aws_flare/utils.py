import ipaddress


def is_private(cidr):
    return ipaddress.ip_network(cidr).is_private


def in_network(cidr, network):
    status = ipaddress.ip_network(cidr).compare_networks(ipaddress.ip_network(network))

    # lets consider equals meaning 'in'
    if status in [0, 1]:
        return True
    else:
        return False
