#!/usr/bin/env python3

import socket
import platform
import subprocess
import sys


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


def run_checks_for_target(target_name, target_value):
    """Run all checks for a given target (hostname or FQDN).

    Returns:
        bool: True if all checks passed, False if any failed
    """
    print(f"{target_name}: {target_value}")
    has_failures = False

    # Ping the target directly
    ping_success = ping_target(target_value)
    ping_status = "successful" if ping_success else "failed"
    print(f"Ping to {target_name.lower()} {target_value}: {ping_status}")
    if not ping_success:
        has_failures = True

    print()
    # Get IPs for the target
    ips = get_ips_for_hostname(target_value)

    if not ips:
        print(f"No IP addresses found for {target_value}")
        return False

    print(f"IP addresses for {target_value}:")
    for ip in ips:
        print(f"  {ip}")

    # Ping each IP
    print(f"\nPinging IP addresses for {target_value}:")
    for ip in ips:
        success = ping_target(ip)
        status = "successful" if success else "failed"
        print(f"  Ping to {ip}: {status}")
        if not success:
            has_failures = True

    return not has_failures


def main():
    # Get hostname and FQDN
    hostname = socket.gethostname()
    fqdn = socket.getfqdn()

    all_passed = True

    # Run checks for hostname
    hostname_passed = run_checks_for_target("Hostname", hostname)
    if not hostname_passed:
        all_passed = False

    print("\n" + "=" * 50 + "\n")

    # Run checks for FQDN (only if different from hostname)
    if fqdn != hostname:
        fqdn_passed = run_checks_for_target("FQDN", fqdn)
        if not fqdn_passed:
            all_passed = False
    else:
        print(f"FQDN is the same as hostname: {fqdn}")

    # Exit with appropriate status code
    if not all_passed:
        print("\nSome checks failed. Exiting with status code 1.")
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
