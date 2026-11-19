# Q43 - Peephole Optimizer (Roll No. 43)

**Course:** Automata Theory and Compiler Design  
**Topic:** Code Optimization / Peephole Optimization  
**Language:** Python 3 (standard library only; no external dependencies required)  
**Requirements:** Python 3.6+ (utilizes f-strings and dictionary unpacking `{**base, ...}`)

---

## 1. Project Overview

This project implements a multi-pass **Peephole Optimizer** for assembly listings. Peephole optimization is a machine-independent/dependent local code optimization technique that inspects a sliding window of target instructions and replaces or eliminates redundant, inefficient operations with semantically equivalent, shorter sequences.

### Target Optimization Rules
1. **Redundant Moves (`MOV X, X`)**:
   Eliminates register-to-register or memory moves where the destination register and source register are identical. Because moving a value into itself does not change processor state or register content, the instruction is dead code and safe to remove.
2. **Jumps to Next Instruction (`JMP L` / `Jcc L`)**:
   Eliminates unconditional jumps (`JMP`) and conditional jumps (`JZ`, `JNZ`, `JE`, `JNE`, etc.) that target a label immediately following the jump instruction (skipping intervening non-executable label definitions). In sequential execution, falling through reaches the exact same target address without incurring branching overhead.

### Fixed-Point Iteration (Cascade Elimination)
Removing one redundant instruction can shorten the distance to a target label, exposing new optimization opportunities (e.g., removing an intervening `MOV R4, R4` allows a preceding `JZ L2` to become a jump to the next instruction). The optimizer repeatedly iterates over the instruction list until a full pass produces zero modifications (a mathematical **fixed point**).

---

## 2. Directory Structure

```text
Automata Mini Project/
├── peephole.py             # Main enhanced & bug-fixed peephole optimizer
├── peephole_baseline.py    # Original baseline AI-generated optimizer (for comparison)
├── run_tests.py            # Automated test suite runner (benchmarks T1 - T13)
├── sample1.asm             # Standard sample demonstrating cascade behavior
├── README.md               # Project documentation and user guide
├── REPORT.md               # Comprehensive 3-5 page technical report & AI declaration
└── tests/                  # Directory containing all 13 test cases
    ├── t01_empty.asm       # Boundary: Empty file
    ├── t02_halt_only.asm   # Single HALT instruction
    ├── t03_single_mov.asm  # Isolated redundant move
    ├── t04_jmp_next.asm    # Basic JMP to next instruction
    ├── t05_jz_next.asm     # Conditional JZ to next instruction
    ├── t06_jmp_multi_label.asm # Jump across intervening label definitions
    ├── t07_jmp_not_next.asm    # Non-removable jump (intervening ADD)
    ├── t08_mov_pair.asm    # Inverted MOV pair (verifies optimization scope)
    ├── t09_case_insensitivity.asm # Case-insensitive register matching
    ├── t10_cascade.asm     # Multi-pass cascade elimination (sample1.asm)
    ├── t11_long_500.asm    # 500-instruction performance stress test
    ├── t12_label_same_line.asm    # Bug Fix 1 verification: inline labels
    └── t13_mixed_case_jump.asm    # Bug Fix 2 verification: mixed-case labels
```

---

## 3. Installation & Prerequisites

No third-party packages or virtual environments are needed. The program runs purely on Python's built-in `re` and `sys` modules.

To verify your Python environment:
```bash
python3 --version
```
*(Ensure Python version is 3.6 or higher).*

---

## 4. Execution Guide

### Basic Usage
To optimize an assembly file and display the transformation details on the terminal:
```bash
python3 peephole.py sample1.asm
```

### Saving Optimized Output to a File
To output the cleaned assembly code to a new file:
```bash
python3 peephole.py sample1.asm optimized_sample1.asm
```

### Running the Full Automated Test Suite
To execute all 13 test cases, verify edge cases, and inspect the performance comparison:
```bash
python3 run_tests.py
```

---

## 5. Sample Input and Output

### Input (`sample1.asm`)
```assembly
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
```

### Command
```bash
python3 peephole.py sample1.asm
```

### Terminal Output
```text
=== Before ===
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

=== After ===
        MOV R1, R2
L1:
        ADD R1, R3
L2:
END:
        HALT

=== Removed ===
line 3: MOV R3, R3      ; redundant -> redundant move (dst == src)
line 4: JMP L1          ; jumps to the next instruction -> JMP to next instruction
line 8: MOV R4, R4      ; redundant; its removal exposes JZ L2 -> redundant move (dst == src)
line 7: JZ  L2                 -> JZ to next instruction
line 10: JMP END         ; jumps to the next instruction -> JMP to next instruction

11 instructions before, 6 after.
```

---

## 6. Key Improvements over Baseline AI Code

In accordance with project guidelines, the initial AI-generated baseline was critically analyzed, identifying two functional bugs and one performance bottleneck:
1. **Handling Inline Labels (`L1: MOV R1, R2`)**:
   - *Baseline Issue:* The regex `^([A-Za-z_]\w*):$` strictly demanded labels occupy an entire isolated line. Lines containing both a label and an instruction were misclassified as `other`, disabling optimization and dropping label recognition.
   - *Fix:* Integrated `LABEL_LEAD_RE = re.compile(r'^([A-Za-z_]\w*):(?:\s*(.*))?$', re.IGNORECASE)` to decouple label definitions from trailing instructions while preserving line linkage.
2. **Case Sensitivity in Jump Targets**:
   - *Baseline Issue:* Jump targets and label identifiers were compared with strict case sensitivity (`==`), missing valid jumps such as `jmp exit` targeting `EXIT:`.
   - *Fix:* Folded comparison to `.upper()` in `jumps_to_next()`.
3. **Worst-Case Quadratic Loop Bottleneck ($O(n^2)$)**:
   - *Baseline Issue:* The baseline issued a `del instrs[i]; break` on every deletion, restarting the search from index 0 across all elements.
   - *Fix:* Implemented a localized backtrack `i = max(0, i - 1)`, transforming performance from $O(n^2)$ to $O(n)$ in typical listings (yielding a 4.7x speedup on a 500-line test).
