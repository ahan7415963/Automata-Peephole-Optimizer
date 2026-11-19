; Sample 1: redundant move, jump to next, and a cascade
        MOV R1, R2
        MOV R3, R3      ; redundant
        JMP L1          ; jumps to the next instruction
L1:
        ADD R1, R3
        JZ  L2
        MOV R4, R4      ; redundant; its removal exposes JZ L2
L2:
        JMP END         ; jumps to the next instruction
END:
        HALT
