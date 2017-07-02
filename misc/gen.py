import random
max_depth = 0

def test_char(start, target, usable_chars):
    for char in usable_chars:
    #print(char)
    #print((ord(char) + attempt) & 0x000000ff)
    #print(char_list)
        #print("Trying subchar %s" % char);
        #print((ord(char) + start) & 0x000000ff)
        if ((ord(char) + start) & 0x000000ff) == ord(target):
            #print(char)
            return char
    
    return False   

def find_char(end_val, start_val , usable_chars, char_list, depth):
    global max_depth
    success = False
    
    for char in usable_chars:
        #print("Trying %s" % char);
        test_val = ord(end_val) + ord(char)
        if test_val == start_val:
            print("Early winner")
            if (depth + 1) >= max_depth:
                depth += 1
                success = True
                char_list.append(char)
                break
        
        result = test_char(test_val, start_val, usable_chars)
        if result is not False:
            if (depth + 2) >= max_depth:
                success = True
                depth += 2
                print("Late winner")
                char_list.append(char)
                char_list.append(result)
                break
    
    if not success:
        print("Recursion!")
        print(char_list)
        depth += 1
        char_list.append(usable_chars[0])
        test_val = ord(end_val) + ord(usable_chars[0])
        if depth > max_depth:
            max_depth = depth
        return find_char(chr(test_val), start_val, usable_chars, char_list, depth)

    if depth > max_depth:
        print("Getting deeper")
        max_depth = depth
        
    return depth

def check_depth(byte1, byte2, byte3, byte4):
    if byte1[1] == max_depth and byte2[1] == max_depth and byte3[1] == max_depth and byte4[1] == max_depth:
        return True
    return False

def get_carry(value_list):
    sum = 0
    for char in value_list:
        sum += ord(char)
    return (sum & 0x0000ff00) >> 8

def hex_print(byte1, byte2, byte3, byte4):
    depth = byte1[1]
    for i in range(0,depth):
        print(hex(ord(byte1[2][i])))

if __name__ == "__main__":
    
    usable_chars = [ '%', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                     'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                     'X', 'Y', 'Z', '-' ]
    
    byte1 = ['\x41', 0, []]
    byte2 = ['\x41', 0, []]
    byte3 = ['\x00', 0, []]
    byte4 = ['\x41', 0, []]

    random.seed()
    
    char_list = []
    byte1[1] = find_char(byte1[0], "\x00", usable_chars, byte1[2], 0)
    print("Done", byte1[2], byte1[1])
    byte2[1] = find_char(byte2[0], "\x00", usable_chars, byte2[2], 0)
    print("Done", byte2[2], byte2[1])
    byte3[1] = find_char(byte3[0], "\x00", usable_chars, byte3[2], 0)
    print("Done", byte3[2], byte3[1])
    byte4[1] = find_char(byte4[0], "\x00", usable_chars, byte4[2], 0)
    print("Done", byte4[2], byte4[1])
    while not check_depth(byte1, byte2, byte3, byte4):
        print("Unbalanced: %d" % max_depth)
        input()
        if byte1[1] < max_depth:
            byte1[2].clear()
            byte1[1] = 0
            byte1[1] = find_char(byte1[0], "\x00", usable_chars, byte1[2], 0)
        if byte2[1] < max_depth:
            byte2[1] = 0
            byte2[2].clear()
            byte2[1] = find_char(byte2[0], "\x00", usable_chars, byte2[2], 0)
        if byte3[1] < max_depth:
            byte3[1] = 0
            byte3[2].clear()
            byte3[1] = find_char(byte3[0], "\x00", usable_chars, byte3[2], 0)
        if byte4[1] < max_depth:
            byte4[1] = 0
            byte4[2].clear()
            byte4[1] = find_char(byte4[0], "\x00", usable_chars, byte4[2], 0)
            
    hex_print(byte1, byte2, byte3, byte4)
    print("Done", byte1[2])
    print("Done", byte2[2])
    print("Done", byte3[2])
    print("Done", byte4[2])
