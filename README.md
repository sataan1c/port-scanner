# Python Port Scanner

A little TCP port scanner I wrote while learning networking and security. You
point it at a host and a range of ports, and it tells you which ones are open,
what usually runs there, and what the service actually says when you poke it.

It's part of my learning journey – my notes on networking, Linux and CTFs are
in [cybersecurity-learning-log](https://github.com/sataan1c/cybersecurity-learning-log).
I built it one feature at a time, so the commit history is basically my
progress log.

## How it works

For each port the scanner just tries to connect. If the TCP handshake goes
through, the port is open; if the host says `RST`, it's closed; if nothing
comes back at all, it's probably a firewall, so I wait a second and move on.

I wasn't sure what was really happening at first, so I opened Wireshark and
watched a scan. Seeing the `SYN → SYN,ACK → ACK` on an open port and just
`SYN → RST` on a closed one is what finally made TCP click for me.

It's a plain connect scan (like `nmap -sT`) – simple, no root needed, but easy
to notice because the target sees a full connection.

**Service names.** Next to each open port I show what usually runs there
(`22 → ssh`, `80 → http`), straight from the system's port list. But that's
just a guess from the number – nothing stops someone running SSH on 2220, like
OverTheWire does.

**Banner grabbing.** So instead of guessing, the scanner talks to the service.
SSH and FTP introduce themselves right away; web servers stay quiet until you
send them something, so I fire off a tiny `HEAD /` request and read the reply.
That's how a web server on 8000 goes from `unknown` to `HTTP/1.0 200 OK`. It's
a baby version of `nmap -sV`.

## Running it

Python 3, nothing to install. Arguments go on the command line:

```
python3 scanner.py <target> <start_port> <end_port>
```

```
$ python3 scanner.py 127.0.0.1 7995 8005
Start scanning 127.0.0.1 (127.0.0.1) from port 7995 to 8005
Port 8000 is open (unknown) - HTTP/1.0 200 OK
Scanning finished. Duration 1.01 seconds
```

The target can be an IP or a name like `scanme.nmap.org`. `python3 scanner.py -h`
prints the help (argparse makes it for free). Bad input doesn't crash it – a
missing argument, a letter instead of a port, an unknown host or a backwards
range all get a clear message.

## Testing it

Easiest way to get an open port is Python's own web server:

```
python3 -m http.server 8000 > /dev/null 2>&1 &
python3 scanner.py 127.0.0.1 7995 8005
kill %1
```

For a banner that the service sends on its own, I scan `scanme.nmap.org` on 22
and get the SSH version.

## Versions

- **v1** – one hardcoded port, just to see it work.
- **v2** – a whole range, prints only the open ones.
- **v3** – host names, service names, input checks, a timer.
- **v4** – threads, so remote scans don't take forever.
- **v5** – banner grabbing: ask the service what it really is.
- **v6** – command-line arguments with argparse.

## A note

This is a learning project. I only scan my own machine, my own VMs, or
`scanme.nmap.org`, which the Nmap team put up for exactly this. Scanning other
people's stuff without permission is a good way to get in real trouble.
