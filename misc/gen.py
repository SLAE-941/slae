import binascii

MAX_DEPTH = 2
GOAL_DEPTH = 0

usable_chars = [ '%', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                 'X', 'Y', 'Z', '-' ]


shellcode = '9090909041435253235313542344'

def find_char(end_val, start_val, char_list, depth, byte):
    
    global usable_chars
    global GOAL_DEPTH
    global MAX_DEPTH

    success = False

    depth += 1

    if depth > MAX_DEPTH:
        return False
    
    for char in usable_chars:
        test_val = (ord(end_val) + ord(char)) & 0x000000ff
        #print("Goal: %d value: %d" % (ord(start_val),test_val))
        if chr(test_val) == start_val:
            #print("Hit!: %s" % char)
            if depth >= GOAL_DEPTH:
                char_list.insert(0,char)
                #print("Hit!: %s" % char)
                success = True        
                
    if success == True and depth > GOAL_DEPTH:
        GOAL_DEPTH = depth
        #print("Setting Goal depth: %d" % GOAL_DEPTH)
        
    if not success:
        #print("Recursion! %d" % depth)
        for char in usable_chars:
            #print("%s: " % char, end='')
            test_val = (ord(end_val) + ord(char)) & 0x000000ff
            result = find_char(chr(test_val), start_val, char_list, depth, byte)
            if result != False:
                char_list.insert(0,char)
                depth = result
                #print("%d" % depth)
                break
            
        if result == False:
            return False
        
    return depth

def check_depth(dword):
    global GOAL_DEPTH
    global MAX_DEPTH
    
    balanced = True

    if GOAL_DEPTH == 0:
        return False
    
    for byte in dword:
        if byte['depth'] == False:
            MAX_DEPTH += 1
            return False
        elif byte['depth'] != GOAL_DEPTH:
            balanced = False

    return balanced

def get_carry(byte):
    sum = ord(byte['start_val'])
    for char in byte['char_list']:
        #print("Sum: %d" % sum)
        sum += ord(char)
    #print("Carry: %d" % sum) 
    #print("Carry: %d" % ((sum & 0x0000ff00) >> 8))  
    return (sum & 0x0000ff00) >> 8

def hex_print(byte):
    global GOAL_DEPTH
    for i in range(0,GOAL_DEPTH):
        value = ''
        for byte_count in range(0,len(byte)):
            value = hex(ord(byte[byte_count]['char_list'][i]))[2:] + value
        print('0x' + value)

def hex_print_start(dword):
    hex_dword = ""

    for byte in dword:
        hex_dword += hex(ord(byte['start_val']))[2:]
    print("0x" + hex_dword)

def hex_print_end(dword):
    hex_dword = ""
  
    for byte in dword:
        hex_dword += hex(ord(byte['end_val']))[2:]
    print("0x" + hex_dword)
    
def build_byte_string(shellcode, format = "hex"):

    byte_string = []

    if format == "hex":
        pad_count = len(shellcode) // 2
        if(pad_count % 2 != 0):
            print("Invalid hex string, missing a byte")
            exit()
        pad_count = pad_count % 4
        shellcode += "90" * pad_count
       
        for i in range(0,len(shellcode),2):
            current_byte = chr(int(shellcode[i:i+2], 16))
            byte_string.append({'start_val':current_byte,'temp_val':current_byte, 'end_val':'\x00', 'depth':0, 'min_depth':(MAX_DEPTH + 1), 'char_list': []})
        
    if format == "python":
        pad_count = len(shellcode) % 4
        shellcode += "\x90" * pad_count

        for current_byte in shellcode:
            byte_string.append({'start_val':current_byte,'temp_val':current_byte, 'end_val':'\x00', 'depth':0, 'min_depth':(MAX_DEPTH + 1), 'char_list': []})

    return byte_string


def generate_shellcode(byte_string):
    dword = []
    for i in range(0,len(byte_string),4):
        dword.append(byte_string[i])
        dword.append(byte_string[i+1])
        dword.append(byte_string[i+2])
        dword.append(byte_string[i+3])
        hex_print_end(dword)
        encode_dword(dword)
        hex_print_start(dword)
        
        hex_print(dword)
        dword.clear()
        
def encode_dword(dword):
    while not check_depth(dword):
        # We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
        # each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation
        carry = 0
        for byte in dword:
            byte['temp_val'] = byte['start_val']
            byte['char_list'].clear()
            byte['depth'] = 0
            #print("Before carry: %d" % ord(byte['start_val']))
            byte['start_val']=chr(ord(byte['start_val']) + carry)
            #print("After carry: %d" % ord(byte['start_val']))
            byte['depth'] = find_char(byte['start_val'], "\x00", byte['char_list'], 0,byte)
            carry = get_carry(byte)
            #print("Done", byte['char_list'], byte['depth'])
            byte['start_val'] = byte['temp_val']
        
if __name__ == "__main__":

    # The intention is to have a start value and an end value e.g: the start value is 0x00000000
    # and an end value e.g. 0x12345678, using only the values provided in the global variable usable_chars
    # find the values that can be subtracted from the start value to reach the end value.
    #
    #   0x00000000
    # - 0x735f5f25   (%__s)
    #   ----------
    #   0x8ca0a0db
    # - 0x7a6c4a63   (cJlz)
    #   ----------
    #   0x12345678
    #
    # We will operate on 4 bytes at a time, a dword. These bytes will be stored in a list
    # dword = []

    # Establish our initial structure, loop 4 times with a dummy value, set the depth to 0 and create
    # an empty list to store our calculated steps to reach the end value
    #for i in range(0,4):
    #    dword.append({'start_val':'\x41','temp_val':'\x41', 'end_val':'\x00', 'depth':0, 'min_depth':(MAX_DEPTH + 1), 'char_list': []})

    # Intel is big endian so we need to store the byte backwards
    #dword[3]['value'] = '\x12'
    #dword[2]['value'] = '\x34'
    #dword[1]['value'] = '\x56'
    #dword[0]['value'] = '\x78'

    # We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
    # each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation

    # The main loop driving the program, one thing we need to consider is that even though we are operating byte by byte
    # through the dword, we need to cater for the byte with the longest requirement. If one byte can reach our desired value
    # in two steps, but another requires 3 we need to go back and re-work the byte with the lower requirement to be equal to
    # the byte with the higher steps. We need to reconsider how the newly generated bytes will be affected by carries as well
    #
    # The loop works via checking the depth, we record the byte with the deepest depth in the global var GOAL_DEPTH, we run through
    # this loop continually until all 4 bytes have the equivilent depth
    byte_string = []
    
    byte_string = build_byte_string(shellcode)
    generate_shellcode(byte_string)
    #print(byte_string)
    

    
