#!/usr/bin/env python3

import socket
import platform
import subprocess
import sys


def get_hostname():
    """Get the system's hostname."""
    return socket.gethostname()


def get_ips_for_hostname(hostname):
    """Get all IP addresses associated with the hostname."""
    try:
        # Get both IPv4 and IPv6 addresses
        addrinfo = socket.getaddrinfo(hostname, None)
        # Extract unique IP addresses
        ip_addresses = set()
        for addr in addrinfo:
            ip = addr[4][0]
            ip_addresses.add(ip)
        return list(ip_addresses)
    except socket.gaierror:
        return []


def ping_target(target):
    """
    Ping a target (hostname or IP) and return whether it was successful.

    Args:
        target (str): The hostname or IP address to ping

    Returns:
        bool: True if ping was successful, False otherwise
    """
    # Adjust ping command based on operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", target]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error pinging {target}: {e}")
        return False


# Maintain backwards compatibility with original function names
def ping_hostname(hostname):
    """Ping a hostname directly and return whether it was successful."""
    return ping_target(hostname)


def ping_ip(ip):
    """Ping an IP address and return whether it was successful."""
    return ping_target(ip)


def main():
    # Get hostname
    hostname = get_hostname()
    print(f"Hostname: {hostname}")

    # Ping hostname
    hostname_ping_success = ping_hostname(hostname)
    hostname_ping_status = "successful" if hostname_ping_success else "failed"
    print(f"Ping to hostname {hostname}: {hostname_ping_status}")

    print()
    # Get IPs for hostname
    ips = get_ips_for_hostname(hostname)

    if not ips:
        print(f"No IP addresses found for {hostname}")
        return

    print(f"IP addresses for {hostname}:")
    for ip in ips:
        print(f"  {ip}")

    # Ping each IP
    print("\nPinging IP addresses:")
    for ip in ips:
        success = ping_ip(ip)
        status = "successful" if success else "failed"
        print(f"  Ping to {ip}: {status}")


if __name__ == "__main__":
    main()
