/* Demonstration of the theory behind a find socket shellcode, use nc -nv <ip> 4444 -p 10000 to connect */

#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

int main(void) {
        int sockfd, newsockfd; /* two sockets, one for the server and a second for the newly connected client */
        struct sockaddr_in serverSA, clientSA, tempSA; 
        int clientSaSize = sizeof(struct sockaddr_in);
        int i,j = sizeof (struct sockaddr_in);
        char *arg_list[] = { { "/bin/sh" }, NULL };

        sockfd = socket(PF_INET, SOCK_STREAM, 0); /* create our socket for the server */

        /* Populate our sockaddr_in structure with our server details */
        memset(serverSA.sin_zero, '\0', sizeof(serverSA.sin_zero)); 
        serverSA.sin_family = AF_INET; 
        serverSA.sin_addr.s_addr = htonl(INADDR_ANY);
        serverSA.sin_port = htons(4444);

        /* Start our server listening on the port */
        bind(sockfd, (struct sockaddr *)&serverSA, sizeof(serverSA));
        listen(sockfd, 2);
        newsockfd = accept(sockfd, (struct sockaddr *)&clentSA, &clientSaSize);

        /* For reference so we can see the getpeername loop in action */ 
        printf("newsockfd: %d\n", newsockfd);

        /* This is where we demonstrate the process behind the socket find shellcode
           Rather than using the socket allocated by accept() to newsockfd we loop through
           socket descriptors using getpeername to identify our client */
        
        for(i=256;i>=0;i--){
                if(getpeername(i,(struct sockaddr *)&tempSA,&j)==-1) {
                /* if a socket descriptor is not valid, getpeername returns -1, move on to the next */
                        continue;
                }
                /* If we made it here, the socketfd is valid, print it out and the port that it is using */
                printf("Socket: %d, Port: %d\n", i, ntohs(tempSA.sin_port));
                /* Check the port number in use by the socket descriptor, if it matches 10000 thats us! */
                if(tempSA.sin_port==htons(10000)) break;
        }
        /* We will assume if we made it all the way to 0 we didn't find ourselves :( */
        if(i == 0) return 1;
        /* normally we would reference newsockfd here, instead we are using the value found in our loop */
        send(i, "Hello!", 6, 0);
        close(sockfd);
        close(newsockfd);
        return 0;
}
