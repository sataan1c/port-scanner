# Python Port Scanner

This is a small TCP port scanner I'm writing in Python while I learn
networking and cybersecurity. You give it a host and a range of ports, and
it tells you which ports are open.

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

## How to run it

You only need Python 3. No extra libraries.

```
python3 scanner.py
```

It asks for a target and a port range:

```
Enter IP address: 127.0.0.1
Enter start port: 7990
Enter end port: 8010
Start scanning from port 7990 to 8010
Port 8000 is open
Scanning finished
```

You can also type a host name like `localhost` instead of an IP.

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

## Versions

- **v1** – checked one hardcoded port on localhost. Just to see if it works.
- **v2** – asks for a target and a range, checks every port, and prints
  only the open ones.

## What's next

- [ ] Show the usual service next to each port (`22 → ssh`)
- [ ] Handle mistakes, like a wrong address or letters instead of a port
- [ ] Use command-line arguments instead of typing everything in
- [ ] Use threads – right now scanning a remote host can take ages, because
  every silent port means waiting a full second
- [ ] Banner grabbing – read what the service says first, to find out
  what's actually running

## Please scan responsibly

This is a learning project. I only scan my own machine, my own VMs, or
`scanme.nmap.org`, where the Nmap team allows it. Scanning other people's
systems without permission can get you into real trouble.