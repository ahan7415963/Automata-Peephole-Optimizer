; 500-instruction performance and scale benchmark
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_1          ; jump to next
L_SCALE_1:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_2          ; jump to next
L_SCALE_2:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_3          ; jump to next
L_SCALE_3:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_4          ; jump to next
L_SCALE_4:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_5          ; jump to next
L_SCALE_5:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_6          ; jump to next
L_SCALE_6:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_7          ; jump to next
L_SCALE_7:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_8          ; jump to next
L_SCALE_8:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_9          ; jump to next
L_SCALE_9:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_10          ; jump to next
L_SCALE_10:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_11          ; jump to next
L_SCALE_11:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_12          ; jump to next
L_SCALE_12:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_13          ; jump to next
L_SCALE_13:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_14          ; jump to next
L_SCALE_14:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_15          ; jump to next
L_SCALE_15:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_16          ; jump to next
L_SCALE_16:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_17          ; jump to next
L_SCALE_17:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_18          ; jump to next
L_SCALE_18:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_19          ; jump to next
L_SCALE_19:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_20          ; jump to next
L_SCALE_20:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_21          ; jump to next
L_SCALE_21:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_22          ; jump to next
L_SCALE_22:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_23          ; jump to next
L_SCALE_23:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_24          ; jump to next
L_SCALE_24:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_25          ; jump to next
L_SCALE_25:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_26          ; jump to next
L_SCALE_26:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_27          ; jump to next
L_SCALE_27:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_28          ; jump to next
L_SCALE_28:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_29          ; jump to next
L_SCALE_29:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_30          ; jump to next
L_SCALE_30:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_31          ; jump to next
L_SCALE_31:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_32          ; jump to next
L_SCALE_32:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_33          ; jump to next
L_SCALE_33:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_34          ; jump to next
L_SCALE_34:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_35          ; jump to next
L_SCALE_35:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_36          ; jump to next
L_SCALE_36:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_37          ; jump to next
L_SCALE_37:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_38          ; jump to next
L_SCALE_38:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_39          ; jump to next
L_SCALE_39:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_40          ; jump to next
L_SCALE_40:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_41          ; jump to next
L_SCALE_41:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_42          ; jump to next
L_SCALE_42:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_43          ; jump to next
L_SCALE_43:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_44          ; jump to next
L_SCALE_44:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_45          ; jump to next
L_SCALE_45:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_46          ; jump to next
L_SCALE_46:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_47          ; jump to next
L_SCALE_47:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_48          ; jump to next
L_SCALE_48:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_49          ; jump to next
L_SCALE_49:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_50          ; jump to next
L_SCALE_50:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_51          ; jump to next
L_SCALE_51:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_52          ; jump to next
L_SCALE_52:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_53          ; jump to next
L_SCALE_53:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_54          ; jump to next
L_SCALE_54:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_55          ; jump to next
L_SCALE_55:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_56          ; jump to next
L_SCALE_56:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_57          ; jump to next
L_SCALE_57:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_58          ; jump to next
L_SCALE_58:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_59          ; jump to next
L_SCALE_59:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_60          ; jump to next
L_SCALE_60:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_61          ; jump to next
L_SCALE_61:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_62          ; jump to next
L_SCALE_62:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_63          ; jump to next
L_SCALE_63:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_64          ; jump to next
L_SCALE_64:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_65          ; jump to next
L_SCALE_65:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_66          ; jump to next
L_SCALE_66:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_67          ; jump to next
L_SCALE_67:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_68          ; jump to next
L_SCALE_68:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_69          ; jump to next
L_SCALE_69:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_70          ; jump to next
L_SCALE_70:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_71          ; jump to next
L_SCALE_71:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_72          ; jump to next
L_SCALE_72:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_73          ; jump to next
L_SCALE_73:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_74          ; jump to next
L_SCALE_74:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_75          ; jump to next
L_SCALE_75:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_76          ; jump to next
L_SCALE_76:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_77          ; jump to next
L_SCALE_77:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_78          ; jump to next
L_SCALE_78:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_79          ; jump to next
L_SCALE_79:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_80          ; jump to next
L_SCALE_80:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_81          ; jump to next
L_SCALE_81:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_82          ; jump to next
L_SCALE_82:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_83          ; jump to next
L_SCALE_83:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_84          ; jump to next
L_SCALE_84:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_85          ; jump to next
L_SCALE_85:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_86          ; jump to next
L_SCALE_86:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_87          ; jump to next
L_SCALE_87:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_88          ; jump to next
L_SCALE_88:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_89          ; jump to next
L_SCALE_89:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_90          ; jump to next
L_SCALE_90:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_91          ; jump to next
L_SCALE_91:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_92          ; jump to next
L_SCALE_92:
    ADD R4, R1
    MOV R5, R6
    MOV R5, R5       ; redundant move
    JMP L_SCALE_93          ; jump to next
L_SCALE_93:
    ADD R5, R1
    MOV R6, R7
    MOV R6, R6       ; redundant move
    JMP L_SCALE_94          ; jump to next
L_SCALE_94:
    ADD R6, R1
    MOV R7, R0
    MOV R7, R7       ; redundant move
    JMP L_SCALE_95          ; jump to next
L_SCALE_95:
    ADD R7, R1
    MOV R0, R1
    MOV R0, R0       ; redundant move
    JMP L_SCALE_96          ; jump to next
L_SCALE_96:
    ADD R0, R1
    MOV R1, R2
    MOV R1, R1       ; redundant move
    JMP L_SCALE_97          ; jump to next
L_SCALE_97:
    ADD R1, R1
    MOV R2, R3
    MOV R2, R2       ; redundant move
    JMP L_SCALE_98          ; jump to next
L_SCALE_98:
    ADD R2, R1
    MOV R3, R4
    MOV R3, R3       ; redundant move
    JMP L_SCALE_99          ; jump to next
L_SCALE_99:
    ADD R3, R1
    MOV R4, R5
    MOV R4, R4       ; redundant move
    JMP L_SCALE_100          ; jump to next
L_SCALE_100:
    ADD R4, R1
    HALT
