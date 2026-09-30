# TCP Port Scanner

A simple multi-threaded TCP port scanner built in Python as part of my Syntecxhub Cybersecurity internship (Week 1 task).

## What it does
Scans a given host across a range of ports and reports which ones are open. Results are printed to the console (open ports only, to keep it readable) and fully logged to `scan_results.log` (open + closed + errors).

## Features
- Scans a single host across a custom port range
- Uses threading so ports are checked concurrently instead of one by one
- Handles common errors: bad hostnames, unreachable hosts, timeouts
- Logs every result with a timestamp for later review

## Technologies used
- Python 3
- `socket` — for the actual TCP connection attempts
- `threading` — for concurrency
- `logging` — for persistent results

## How it works
For each port in the given range, the script spins up a thread that tries to open a TCP connection to that port using `socket.connect_ex()`. This function returns `0` on success (port open) rather than throwing an exception, which makes it easy to check thousands of ports without wrapping everything in try/except. A short timeout (1 second) is used so the scan doesn't stall on non-responsive ports. All threads are started together and then joined, so the script waits for the full scan to finish before reporting completion.

## How to run
```bash
python port_scanner.py
```
You'll be prompted for a host/IP and a port range. Example test target: `scanme.nmap.org` (a host maintained specifically for scanner testing).

## Security considerations
- Only scan hosts you own or have explicit permission to scan — port scanning unauthorized systems can violate terms of service or local laws.
- This is a basic scanner for learning purposes, not a production security tool — it doesn't do service/version detection, stealth scanning, or rate limiting.

## Limitations
- No OS/service fingerprinting (just open/closed status)
- No UDP support (TCP only)
- Threading is unbounded — scanning a very large port range spawns a large number of threads at once, which isn't ideal for big scans

## Future improvements
- Add a thread pool instead of unbounded threads
- Add banner grabbing to identify what service is running on open ports
- Add UDP scanning support
- Add command-line arguments instead of interactive input

## Real-world relevance
Port scanning is a core part of network reconnaissance — used by network engineers to verify firewall rules, by security teams for attack-surface visibility, and by attackers during the recon phase of an attack. Understanding how scanners work from the builder's side makes it easier to recognize scanning activity in logs (e.g., many connection attempts across ports from one source in a short window), which is a common early indicator analyzed in SOC environments.