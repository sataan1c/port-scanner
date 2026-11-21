# Python Port Scanner

This is a small TCP port scanner I'm writing in Python while I learn
networking and cybersecurity. You give it a host and a range of ports, and
it tells you which ports are open and what usually runs on them.

It's part of my cybersecurity learning journey – my notes on networking,
Linux and CTFs live in
[cybersecurity-learning-log](https://github.com/sataan1c/cybersecurity-learning-log).

I'm building it step by step. Every version adds one new thing, so the
commit history is also a log of what I learned.

## How it works

For each port, the scanner simply tries to connect to it. Python's `socket`
module asks the operating system to do a normal TCP handshake, and the
result tells me what's going on:

- **Open port** – the handshake works (`SYN → SYN, ACK → ACK`), so
  `connect_ex()` returns `0`.
- **Closed port** – the host answers with `RST`, which basically means
  "nobody's here".
- **Filtered port** – no answer at all, usually because of a firewall. The
  scanner waits one second and moves on.

When I first wrote it, I wasn't sure what was really happening under the
hood, so I opened Wireshark and watched it. For the open port I could see
the whole handshake and then the `FIN` packets when the socket closed. For
the closed port there were just two packets: `SYN` and `RST, ACK`. Seeing
it with my own eyes made the TCP theory finally click.

This kind of scan is called a **TCP connect scan** (like `nmap -sT`). It's
simple and doesn't need admin rights, but it's easy to spot, because the
target sees a real connection. Nmap's default SYN scan is sneakier: it
never finishes the handshake, but it needs root.

### Service names

Next to each open port, the scanner shows the service that *usually* runs
there, like `22 → ssh` or `80 → http`. It gets the name from the system's
list of well-known ports with `socket.getservbyport()`. If a port isn't in
that list, it just says `unknown`.

It's only a guess based on the port number, though. Nothing stops someone
from running SSH on port 2220 (OverTheWire does exactly that). To know what
is really running, you have to actually talk to the service – that's on my
to-do list.

## How to run it

You only need Python 3. No extra libraries.

```
python3 scanner.py
```

It asks for a target and a port range. The target can be an IP address or
a host name like `localhost` – the scanner looks up the IP by itself:

```
Enter IP address or host name: 127.0.0.1
Enter start port: 7990
Enter end port: 8010
Start scanning 127.0.0.1 (127.0.0.1) from port 7990 to 8010
Port 8000 is open (unknown)
Scanning finished. Duration 0.01 seconds
```

### If you make a mistake

The scanner doesn't crash on bad input anymore. It just asks again:

- a host that doesn't exist → "Host … not found, please try again"
- letters instead of a port → "Please enter numbers only"
- a port outside 1–65535 → "Port must be in range 1 - 65535"
- a start port bigger than the end port → it asks you to fix the order

This was my first real use of `try` / `except`. I learned to catch specific
errors like `ValueError` or `socket.gaierror` instead of a bare `except`,
which would also swallow things like Ctrl+C.

## How I test it

I need an open port to test against, and Python has a tiny built-in web
server that's perfect for this:

```
python3 -m http.server 8000 > /dev/null 2>&1 &
python3 scanner.py
kill %1
```

While the server runs, port 8000 shows up as open. After `kill %1`, it's
gone.

The scan timer shows something interesting: on `localhost` a scan takes
almost no time, because ports answer instantly. On a remote host, every
silent port makes the scanner wait a full second, so the same range can
take minutes. That's the main reason threads are next on my list.

## Versions

- **v1** – checked one hardcoded port on localhost. Just to see if it works.
- **v2** – asks for a target and a range, checks every port, and prints
  only the open ones.
- **v3** – accepts host names, shows service names, checks the input for
  mistakes and measures how long the scan takes.

## What's next

- [x] Show the usual service next to each port (`22 → ssh`)
- [x] Handle mistakes, like a wrong address or letters instead of a port
- [x] Show how long the scan takes
- [ ] Use threads – scan many ports at the same time, so a remote scan
  doesn't take ages
- [ ] Banner grabbing – read what the service says (or send it an HTTP
  request) to find out what's actually running
- [ ] Use command-line arguments instead of typing everything in

## Please scan responsibly

This is a learning project. I only scan my own machine, my own VMs, or
`scanme.nmap.org`, where the Nmap team allows it. Scanning other people's
systems without permission can get you into real trouble.