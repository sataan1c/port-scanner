import socket
import time

while True:
    target = input("Enter IP address or host name: ")
    try:
        target_ip = socket.gethostbyname(target)
        break
    except socket.gaierror:
        print(f"Host {target} not found, please try again")

while True:
    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

    except (ValueError, TypeError):
        print("Please enter numbers only")
        continue

    if start_port < 1 or end_port > 65535:
        print("Port must be in range 1 - 65535")
    elif start_port > end_port:
        print("Starting point must be less than or equal to than end point")
    else:
        break



print(f"Start scanning {target} ({target_ip}) from port {start_port} to {end_port}")

start_time = time.perf_counter()

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(1.0)

    result = s.connect_ex((target_ip, port))

    if result == 0:
        try:
            service = socket.getservbyport(port, "tcp")

        except OSError:
            service = "unknown"
        print(f"Port {port} is open ({service})")

    s.close()

end_time = time.perf_counter()
duration = end_time - start_time

print(f"Scanning finished. Duration {duration:.2f} seconds")
