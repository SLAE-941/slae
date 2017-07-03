
waterline = 0
max_depth = 4

usable_chars = [ '%', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                 'X', 'Y', 'Z', '-' ]

def test_char(start, target):
    global usable_chars
    for char in usable_chars:
        if ((ord(char) + start) & 0x000000ff) == ord(target):
            return char
    
    return False   

def find_char(byte):
    
    global usable_chars
    global waterline
    global max_depth

    char_list = []

    success = False
    
    for char in usable_chars:
        #print("Trying %s" % char);
        test_val = ord(end_val) + ord(char)
        if test_val == start_val:
            if checking:
                
            if (depth + 1) >= waterline:
                depth += 1
                if depth > max_depth:
                    return False
                success = True
                char_list.append(char)
                break
        
        result = test_char(test_val, start_val)
        if result is not False:
            if (depth + 2) >= waterline:
                success = True
                depth += 2
                print("Late winner")
                char_list.append(char)
                char_list.append(result)
                break
    
    if not success:
        print("Recursion!")
        depth += 1
        for char in usable_chars:
                temp_byte = byte
                temp_byte['end_val'] = (ord(end_val) + ord(char)) & 0x000000ff
                result = find_char(temp_byte)
        if depth > waterline:
            waterline = depth
        return find_char(chr(test_val), start_val, char_list, depth)

    if depth > waterline:
        print("Getting deeper")
        waterline = depth
        
    return depth

def check_depth(byte):
    global waterline
    balanced = True

    if waterline == 0:
        return False
    
    for i in range(0,len(byte)):
        if byte[i]['depth'] != waterline:
            balanced = False
    return balanced

def get_carry(byte):
    sum = ord(byte['value'])
    for char in byte['char_list']:
        sum += ord(char)
    return (sum & 0x0000ff00) >> 8

def hex_print(byte):
    global waterline
    for i in range(0,waterline):
        value = ''
        for byte_count in range(0,len(byte)):
            value = hex(ord(byte[byte_count]['char_list'][i]))[2:] + value
        print('0x' + value)

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
    dword = []

    # Establish our initial structure, loop 4 times with a dummy value, set the depth to 0 and create
    # an empty list to store our calculated steps to reach the end value
    for i in range(0,4):
        dword.append({'start_val':'\x41', 'end_val':'\x00', 'depth':0, 'min_depth':0, 'char_list': [], 'checking':True})

    # Intel is big endian so we need to store the byte backwards
    dword[3]['value'] = '\x07'
    dword[2]['value'] = '\x98'
    dword[1]['value'] = '\x23'
    dword[0]['value'] = '\x43'

    # We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
    # each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation
    carry = 0

    # The main loop driving the program, one thing we need to consider is that even though we are operating byte by byte
    # through the dword, we need to cater for the byte with the longest requirement. If one byte can reach our desired value
    # in two steps, but another requires 3 we need to go back and re-work the byte with the lower requirement to be equal to
    # the byte with the higher steps. We need to reconsider how the newly generated bytes will be affected by carries as well
    #
    # The loop works via checking the depth, we record the byte with the deepest depth in the global var waterline, we run through
    # this loop continually until all 4 bytes have the equivilent depth
    
##    while not check_depth(dword):
##        # We will work one byte at a time, if the addition of two values results in a carry (i.e the values subtracted from
##        # each other require borrowing from the neighboring byte) we need to be aware of that and factor it into our calculation
##        carry = 0
##        for byte in dword:
##            byte['char_list'].clear()
##            byte['depth'] = 0
##            print("Before carry: %d" % ord(byte['value']))
##            byte['value'] = chr(ord(byte['value']) + carry)
##            print("After carry: %d" % ord(byte['value']))
##            byte['depth'] = find_char(byte['value'], "\x00", byte['char_list'], 0)
##            carry = get_carry(byte)
##            print("Done", byte['char_list'], byte['depth'])
        


    # The first run, 
    for byte in dword:
        print("Before carry: %d" % ord(byte['value']))
        byte['value'] = chr(ord(byte['value']) + carry)
        print("After carry: %d" % ord(byte['value']))
        byte['depth'] = find_char(byte['value'], "\x00", byte['char_list'], 0)
        carry = get_carry(byte)
        print("Done", byte['char_list'], byte['depth'])
        
    while not check_depth(dword):
        print("Unbalanced: %d" % waterline)
        for byte in dword:
            if byte['depth'] < waterline:
                byte['char_list'].clear()
                byte['depth'] = 0
                byte['depth'] = find_char(byte['value'], "\x00", byte['char_list'], 0)

    hex_print(dword)
