import random

#Color codes
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0;0m"

#Encode shellcode using XOR, ADD, SUB, ROL, and ROR
def encode_shellcode(shellcode, key):
    encoded_shellcode = bytearray()
    for i, byte in enumerate(shellcode):
        #XOR
        xored_byte = byte ^ key[i % len(key)]
        #ADD
        added_byte = (xored_byte + key[(i + 1) % len(key)]) % 256
        #SUB
        subbed_byte = (added_byte - key[(i + 2) % len(key)]) % 256
        #ROL
        rolled_byte = ((subbed_byte << 1) | (subbed_byte >> 7)) % 256
        #ROR
        ror_byte = ((rolled_byte >> 1) | (rolled_byte << 7)) % 256
        encoded_shellcode.append(ror_byte)
    return bytes(encoded_shellcode)

#Decode shellcode using ROR, ROL, SUB, ADD, XOR
def decode_shellcode(encoded_shellcode, key):
    decoded_shellcode = bytearray()
    for i, byte in enumerate(encoded_shellcode):
        #ROR
        ror_byte = ((byte >> 7) | (byte << 1)) % 256
        #ROL
        rolled_byte = ((ror_byte >> 1) | (ror_byte << 7)) % 256
        #SUB
        subbed_byte = (rolled_byte + key[(i + 2) % len(key)]) % 256
        #ADD
        added_byte = (subbed_byte - key[(i + 1) % len(key)]) % 256
        #XOR
        xored_byte = added_byte ^ key[i % len(key)]
        decoded_shellcode.append(xored_byte)
    return bytes(decoded_shellcode)

#Generate a random key of given length and convert it into bytes
def generate_key(length):
    return bytes([random.randint(0, 255) for i in range(length)])


def info():
    print(f"""{GREEN}
    
     _       _________ _______  _______  _        _______  _       
    ( (    /|\__   __/(  ____ \(  ____ )( (    /|(  ___  )( (    /|
    |  \  ( |   ) (   | (    \/| (    )||  \  ( || (   ) ||  \  ( |
    |   \ | |   | |   | (__    | (____)||   \ | || (___) ||   \ | |
    | (\ \) |   | |   |  __)   |     __)| (\ \) ||  ___  || (\ \) |
    | | \   |   | |   | (      | (\ (   | | \   || (   ) || | \   |
    | )  \  |___) (___| (____/\| ) \ \__| )  \  || )   ( || )  \  |
    |/    )_)\_______/(_______/|/   \__/|/    )_)|/     \||/    )_)
    
    {RESET} {RED}                        
                         Author: Abhijeet Kumar
                      Github: github.com/wand3rlust
        
    {RESET}""")

#Menu options
def main():
    info()
    while True:
        print(f"{GREEN}1. Encode shellcode")
        print("2. Decode shellcode")
        print("3. Exit")
        choice = input(f"Enter your choice [1-3]: {RESET}\n")

        if choice == "1":
            plaintext_shellcode = input("Enter plaintext shellcode:\n")
            #Encode the user unput into UTF-8 and change from string to byte
            shellcode = plaintext_shellcode.encode()
            #Generate same length key as shellcode hex
            key = generate_key(len(shellcode))
            #Call encode_shellcode function with 2 arguments i.e, UTF-8 shellcode and key
            encoded_shellcode = encode_shellcode(shellcode, key)
            print(f"Original shellcode (in hex): {RED}", shellcode.hex())
            print(f"{RESET}Key (in hex): {RED}", key.hex())
            print(f"{RESET}Encoded shellcode (in hex): {RED}", encoded_shellcode.hex())
            #Convert byte format to string
            encoded_shellcode = encoded_shellcode.hex()
            #Append \x after every 2nd character
            encoded_shellcode = "\\x" + "\\x".join(encoded_shellcode[i:i + 2] for i in range(0, len(encoded_shellcode), 2))
            print(f"{RESET}Encoded shellcode (with \\x): {RED}", encoded_shellcode)
            print(f"{RESET}\n")

        elif choice == "2":
            print(f"{GREEN}Choose the hex format:")
            print("a. Normal hex")
            print("b. \\x format")
            choice = input(f"Enter your choice [ a-b]: {RESET}\n")

            if choice == "a":
                #Convert user input hex to byte
                encoded_shellcode = bytes.fromhex(input("Enter encoded shellcode (in hex):\n"))
                #Convert user input key into byte
                key = bytes.fromhex(input("Enter key (in hex):\n"))
                #Call decode_shellcode function with 2 arguments i.e, shellcode and key
                decoded_shellcode = decode_shellcode(encoded_shellcode, key)
                #Convert encoded shellcode to hex and display
                print(f"Encoded shellcode (in hex): {RED}", encoded_shellcode.hex())
                #Convert key to hex and display
                print(f"{RESET}Key (in hex): {RED}", key.hex())
                #Convert decoded shellcode to hex and display
                print(f"{RESET}Decoded shellcode (in hex): {RED}", decoded_shellcode.hex())
                print("\n")

            elif choice == "b":
                encoded_shellcode = input("Enter encoded shellcode (with \\x):\n")
                #Remove \x from hex shellcode and convert to byte
                encoded_shellcode = bytes.fromhex(encoded_shellcode.replace("\\x", ""))
                #Convert encoded shellcode to hex and display
                print(f"Encoded shellcode (without \\x): {RED}", encoded_shellcode.hex())
                #Convert user input key into byte
                key = bytes.fromhex(input(f"{RESET}Enter key (in hex):\n"))
                #Call decode_shellcode function with 2 arguments i.e, shellcode and key
                decoded_shellcode = decode_shellcode(encoded_shellcode, key)
                print(f"Decoded shellcode (in hex): {RED}", decoded_shellcode.hex())
                print(f"{RESET}\n")

            else:
                print(f"{RED}Invalid selection, start again{RESET}\n")

        elif choice == "3":
            print(f"{GREEN}Sayonara...{RESET}")
            break

        else:
            print(f"{RED}404: choice not found{RESET}")
            print("\n")

if __name__ == "__main__":
    main()
