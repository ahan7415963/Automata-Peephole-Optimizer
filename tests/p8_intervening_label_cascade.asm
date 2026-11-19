; P8 Test: JMP L1 separated from redundant MOV by label L0
JMP L1
L0:
MOV R1, R1
L1:
HALT
