#!/usr/bin/env python3

import socket
import platform
import subprocess


def get_hostname():
    """Get the system's hostname."""
    return socket.gethostname()


def get_fqdn():
    """Get the system's fully qualified domain name."""
    return socket.getfqdn()


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


def run_checks_for_target(target_name, target_value):
    """Run all checks for a given target (hostname or FQDN)."""
    print(f"{target_name}: {target_value}")

    # Ping the target directly
    ping_success = ping_target(target_value)
    ping_status = "successful" if ping_success else "failed"
    print(f"Ping to {target_name.lower()} {target_value}: {ping_status}")

    print()
    # Get IPs for the target
    ips = get_ips_for_hostname(target_value)

    if not ips:
        print(f"No IP addresses found for {target_value}")
        return

    print(f"IP addresses for {target_value}:")
    for ip in ips:
        print(f"  {ip}")

    # Ping each IP
    print(f"\nPinging IP addresses for {target_value}:")
    for ip in ips:
        success = ping_ip(ip)
        status = "successful" if success else "failed"
        print(f"  Ping to {ip}: {status}")


def main():
    # Get hostname and FQDN
    hostname = get_hostname()
    fqdn = get_fqdn()

    # Run checks for hostname
    run_checks_for_target("Hostname", hostname)
    
    print("\n" + "="*50 + "\n")
    
    # Run checks for FQDN (only if different from hostname)
    if fqdn != hostname:
        run_checks_for_target("FQDN", fqdn)
    else:
        print(f"FQDN is the same as hostname: {fqdn}")


if __name__ == "__main__":
    main()
