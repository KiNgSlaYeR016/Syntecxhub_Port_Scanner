# Simple TCP port scanner
# Checks a range of ports on a given host and tells you which ones are open
# Uses threading so it doesn't take forever on bigger ranges

import socket
import threading
import logging
from datetime import datetime

# logging setup - keeping a log file so I have a full record, not just what prints to screen
logging.basicConfig(
    filename="scan_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# needed this because multiple threads were printing at the same time and messing up the output
print_lock = threading.Lock()


def scan_port(host, port):
    # tries to connect to one port, reports back if it's open or not
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 + TCP
        sock.settimeout(1)  # don't want it hanging forever on dead ports

        # connect_ex gives back an error code instead of throwing an exception
        # 0 = success = port is open
        result = sock.connect_ex((host, port))

        with print_lock:
            if result == 0:
                msg = f"Port {port}: OPEN"
                print(msg)
                logging.info(msg)
            else:
                # not printing every closed port or the terminal gets flooded
                # but still logging it so the file has the complete picture
                logging.info(f"Port {port}: closed")

        sock.close()

    except socket.gaierror:
        with print_lock:
            print(f"Couldn't resolve hostname: {host}")
        logging.error(f"Hostname resolution failed for {host}")

    except socket.error:
        with print_lock:
            print(f"Connection error reaching {host}:{port}")
        logging.error(f"Connection error - {host}:{port}")


def scan_range(host, start_port, end_port):
    # kicks off a thread per port so we're not waiting on each one sequentially
    print(f"Scanning {host} - ports {start_port} to {end_port}")
    logging.info(f"--- New scan: {host} ({start_port}-{end_port}) ---")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

    # wait for every thread to actually finish before saying we're done
    for t in threads:
        t.join()

    print("Done. Check scan_results.log for the full results (open + closed).")


# entry point - just asks for the basic info and runs the scan
if __name__ == "__main__":
    target_host = input("Host/IP to scan: ").strip()
    start = int(input("Start port: ").strip())
    end = int(input("End port: ").strip())

    scan_range(target_host, start, end)   