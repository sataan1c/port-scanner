import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Simple TCP port scanner")

parser.add_argument("target", help="IP address or host name")
parser.add_argument("start_port", type=int, help="first port to scan")
parser.add_argument("end_port", type=int, help="last port to scan")

args = parser.parse_args()

target = args.target
start_port = args.start_port
end_port = args.end_port

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(f"Host {target} not found")
    exit()

if start_port < 1 or end_port > 65535:
    print("Port must be in range 1 - 65535")
    exit()
elif start_port > end_port:
    print("Starting point must be less or equal to than end point")
    exit()

def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((ip, port))

        try:
            banner = s.recv(1024)    
        except socket.timeout:
            banner = b""

        if not banner:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024)

        s.close()

        text = banner.decode(errors="ignore").strip()
        return text.splitlines()[0] if text else ""
    except OSError:
        return ""

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)

    result = s.connect_ex((target_ip, port))

    if result == 0:
        try:
            service = socket.getservbyport(port, "tcp")

        except OSError:
            service = "unknown"

        banner = grab_banner(target_ip, port)

        if banner:
            print(f"Port {port} is open ({service}) - {banner}")
        else:
            print(f"Port {port} is open ({service})")

    s.close()

print(f"Start scanning {target} ({target_ip}) from port {start_port} to {end_port}")

start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

end_time = time.perf_counter()
duration = end_time - start_time

print(f"Scanning finished. Duration {duration:.2f} seconds")
