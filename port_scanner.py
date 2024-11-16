import socket
from socket import AF_INET, SOCK_STREAM
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose_mode=False):
    open_ports = []

    # Resolve target to IP address
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        if target[0].isalpha():  # Likely a hostname
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"

    # Scan ports in the specified range
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(family=AF_INET, type=SOCK_STREAM) as server_socket:
            server_socket.settimeout(3)  # Increased timeout to 3 seconds
            try:
                if server_socket.connect_ex((ip_address, port)) == 0:
                    open_ports.append(port)
            except socket.error:
                continue

    # Return open ports if not verbose mode
    if not verbose_mode:
        return open_ports

    # Verbose output
    try:
        hostname = socket.gethostbyaddr(ip_address)[0] if target[0].isdigit() else target
    except socket.herror:
        hostname = ""

    if hostname:
        ans = f"Open ports for {hostname} ({ip_address})\nPORT     SERVICE\n"
    else:
        ans = f"Open ports for {ip_address}\nPORT     SERVICE\n"

    for port in open_ports:
        ans += f"{port:<9}{ports_and_services.get(port, 'unknown')}\n"

    return ans.strip()
