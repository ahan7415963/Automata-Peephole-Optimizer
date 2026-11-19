# Academic Project Report: Peephole Optimizer (Q43)

**Course:** Automata Theory and Compiler Design  
**Roll No. / Topic:** Roll No. 43 / Peephole Optimization  
**Project Title:** Multi-Pass Peephole Optimizer for Redundant Move and Jump-to-Next Instruction Elimination  
**Language:** Python 3 (Pure Standard Library)  

---

## 1. Problem Statement

In compiler backends, code generators (whether based on syntax-directed translation, tree-rewriting, or pattern matching) emit target assembly code by translating intermediate representations locally. Because these code generation routines operate with limited context—frequently generating standardized instruction sequences for abstract constructs—the resulting target assembly often contains glaring local redundancies.

**Problem Q43** requires the design and implementation of a **peephole optimizer** that processes an assembly language listing and eliminates two specific categories of inefficiencies:
1. **Redundant Moves (`MOV X, X`)**: Any data movement instruction where the destination and source registers (or memory locations) are identical.
2. **Jumps to the Next Instruction (`JMP L` / `Jcc L`)**: Any control-flow branch (unconditional or conditional) whose target label immediately follows the branch in the instruction stream (even if separated by non-executable label definitions).

Furthermore, because eliminating an instruction alters adjacent relative positions—potentially exposing subsequent redundancies (a phenomenon termed **cascading**)—the optimizer must repeatedly apply transformation rules until a mathematical **fixed point** is attained (i.e., a complete pass yields zero modifications).

---

## 2. Theoretical Background

### 2.1 Peephole Optimization Principles
Peephole optimization is a local code optimization technique introduced by W. M. McKeeman (1965). The optimizer inspects a small sliding window (the "peephole") of target instructions. When the pattern of instructions within the window matches a known inefficient idiom, the optimizer substitutes the sequence with a shorter, faster, or semantically equivalent sequence.

```
       [ ... Instruction Stream ... ]
                 |   |   |
              +-------------+
              | MOV R3, R3  | <--- Peephole Window (Size 1 or 2)
              +-------------+
                 |   |   |
       [ Semantic Rule Transformation ]
                 |   |   |
                 v   v   v
              [ Instruction Deleted ]
```

### 2.2 Semantic Correctness of Rule 1: Redundant Moves (`MOV X, X`)
The instruction `MOV X, X` copies the current contents of operand X back into X. Under standard computer architecture semantics (such as x86, ARM, or MIPS pseudo-assembly):
- The value stored in X remains unchanged: Val(X)_(t+1) = Val(X)_t.
- In load-store and register architectures without side-effects on data moves (or where condition flags are not updated by simple register moves), executing `MOV X, X` is equivalent to a `NOP` (No Operation).
- Deleting the instruction reduces code size and eliminates clock cycles consumed by instruction fetch, decode, and execution, with zero impact on downstream program state.

### 2.3 Semantic Correctness of Rule 2: Jump to Next Instruction (`JMP L` / `Jcc L`)
In von Neumann machines, the Program Counter (PC) automatically increments to point to the sequentially adjacent instruction in memory after each fetch.
- An unconditional branch `JMP L` forces PC <- Addr(L).
- If Addr(L) is already the address of the next executable instruction, sequential fall-through execution achieves the identical program counter update:
  PC_fallthrough = PC_jump = Addr(L)
- The same logic applies to conditional branches (`JZ L`, `JNZ L`, `JGE L`). If condition C is true, the branch sets PC <- Addr(L). If C is false, execution falls through to the next instruction, which is also Addr(L). Thus, regardless of whether C evaluates to true or false, control invariably transfers to L.
- Label definitions themselves are non-executable assembler directives; therefore, any number of consecutive labels between the jump and target L do not impede fall-through semantics.
- Deleting the jump preserves execution order while eliminating pipeline branch penalties.

### 2.4 The Fixed-Point Property & Cascading
Peephole rules cannot simply be executed in a single sequential sweep. Consider the following sequence:
```assembly
    JZ  L2
    MOV R4, R4      ; Redundant move
L2:
    HALT
```
In a single naive pass, `JZ L2` cannot be eliminated because it is immediately followed by `MOV R4, R4` (an executable instruction), not label `L2`. However, once `MOV R4, R4` is recognized and purged, the listing contracts:
```assembly
    JZ  L2
L2:
    HALT
```
Now, `JZ L2` is directly followed by `L2:`. A second iteration recognizes the newly formed adjacency and purges `JZ L2`. Formally, let S_0 be the initial instruction list, and T be the peephole transformation function. The optimizer computes:
S_(k+1) = T(S_k)
until S_(k+1) = S_k (the **fixed point**). Because the instruction list is finite and each transformation strictly decreases list length, termination is mathematically guaranteed.

---

## 3. System Architecture & Design

The optimizer follows a four-stage pipeline: **Lexical Cleaning & Parsing** -> **Pattern Matching** -> **Sliding-Window Fixed-Point Engine** -> **Emission**.

### 3.1 Flowchart

```mermaid
flowchart TD
    A([Raw Assembly Source]) --> B[Strip Comments & Whitespace]
    B --> C[Lexical Parser]
    C --> D{Inline Label Present?}
    D -- Yes --> E[Emit Label Record]
    E --> F[Parse Remainder Instruction]
    D -- No --> F
    F --> G[(Internal Instruction List)]
    
    G --> H[Fixed-Point Optimizer Loop]
    H --> I{Inspect Instruction at Index i}
    
    I -- MOV X, X --> J[Delete Redundant MOV]
    I -- JMP/Jcc to Next --> K[Delete Redundant Jump]
    I -- Other --> L[Increment Index i]
    
    J --> M[Log Action & Nearest-Non-Label Backtrack]
    K --> M
    M --> N{More Instructions?}
    L --> N
    
    N -- Yes --> I
    N -- No --> O{Any Deletion in Pass?}
    O -- Yes --> H
    O -- No Fixed Point --> P([Emit Optimized Listing & Report Log])
```

### 3.2 Internal Data Structure
Each parsed instruction is encapsulated in a Python dictionary containing explicit metadata:
```python
{
    'line': int,           # Original line number in source file (for traceability)
    'text': str,           # Reconstructed or original source text
    'kind': str,           # Categorical type: 'label', 'mov', 'jump', or 'other'
    'name': str,           # Label identifier (for 'label' kind)
    'dst': str,            # Destination register/operand (for 'mov' kind)
    'src': str,            # Source register/operand (for 'mov' kind)
    'op': str,             # Jump mnemonic, e.g., 'JMP', 'JZ', 'JNE' (for 'jump' kind)
    'target': str          # Branch target label identifier (for 'jump' kind)
}
```

### 3.3 Pattern Detection Rules
- **Rule 1 (MOV)**: Checked via `ins['kind'] == 'mov' and ins['dst'].upper() == ins['src'].upper()`.
- **Rule 2 (JUMP)**: Evaluated by `jumps_to_next(instrs, i)`. The function scans forward from index i+1, skipping consecutive items where `kind == 'label'`. If it encounters an instruction whose `name.upper() == target.upper()`, it returns `True`. If it encounters an executable instruction of another kind (`mov`, `other`, non-matching `jump`), it halts forward scanning and returns `False`.

---

## 4. Test Suite and Experimental Validation

A comprehensive test suite of 14 test cases (T1 through T13, and P8) was constructed to validate boundary conditions, individual rules, non-optimizable controls, cascading passes, scale performance, and bug resolutions.

### 4.1 Test Case Specification & Results

| Test ID | Input Description | What it Tests | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **T1** | Empty file (`0` bytes) | Boundary handling | 0 instrs, no crash | 0 before, 0 after | **PASS** |
| **T2** | `HALT` alone | Non-optimizable code | Untouched | 1 before, 1 after | **PASS** |
| **T3** | `MOV R1, R1` | Single redundant move | 1 removed | 1 before, 0 after | **PASS** |
| **T4** | `JMP L1` followed by `L1:` | Basic unconditional jump | `JMP L1` removed | 3 before, 2 after | **PASS** |
| **T5** | `JZ L1` followed by `L1:` | Conditional jump-to-next | `JZ L1` removed | 3 before, 2 after | **PASS** |
| **T6** | `JMP L1`, `L2:`, `L1:` | Jump across empty labels | `JMP L1` removed | 4 before, 3 after | **PASS** |
| **T7** | `JMP L1`, `ADD R1, R2`, `L1:` | Intervening instruction | Jump retained | 4 before, 4 after | **PASS** |
| **T8** | `MOV R1, R2`, `MOV R2, R1` | Inverted move pair | Retained (scope check)| 3 before, 3 after | **PASS** |
| **T9** | `mov r1, R1` | Case-insensitive registers| `mov` removed | 2 before, 1 after | **PASS** |
| **T10**| `sample1.asm` (multi-pass) | Cascading fixed point | 5 removed in passes | 11 before, 6 after| **PASS** |
| **T11**| 500-instruction synthetic | Scale & Performance | 200 removed, <1 ms | 501 before, 301 after| **PASS** |
| **T12**| `L1: MOV R1, R1` | Bug Fix 1: Inline label | Label kept, move removed| 6 before, 4 after | **PASS** |
| **T13**| `jmp target` / `TARGET:` | Bug Fix 2: Mixed-case label | `jmp` removed | 3 before, 2 after | **PASS** |
| **P8** | `JMP L1; L0:; MOV R1,R1; L1:`| Nearest-non-label cascade | `L0:, L1:, HALT` | 5 before, 3 after | **PASS** |

### 4.2 Terminal Run Evidence

#### Run 1: Execution on P8 Benchmark (`tests/p8_intervening_label_cascade.asm`)
```text
$ python3 peephole.py tests/p8_intervening_label_cascade.asm
=== Before ===
JMP L1
L0:
MOV R1, R1
L1:
HALT

=== After ===
L0:
L1:
HALT

=== Removed ===
line 4: MOV R1, R1             -> redundant move (dst == src)
line 2: JMP L1                 -> JMP to next instruction

5 instructions before, 3 after.
```

#### Run 2: Full Test Suite Benchmark (`run_tests.py`)
```text
$ python3 run_tests.py
========================================================================================
      AUTOMATA THEORY & COMPILER DESIGN (Q43) - PEEPHOLE OPTIMIZER TEST SUITE
========================================================================================
Test  | Description                                | Before | After | Removed | Time (ms) | Status
----------------------------------------------------------------------------------------
T1    | Boundary: Empty file (no output, no crash) | 0      | 0     | 0       | 0.00      | [PASS]
T2    | Single non-optimizable instruction (HALT)  | 1      | 1     | 0       | 0.01      | [PASS]
T3    | Single redundant move (MOV R1, R1)         | 1      | 0     | 1       | 0.01      | [PASS]
T4    | Basic jump-to-next (JMP L1 -> L1:)         | 3      | 2     | 1       | 0.01      | [PASS]
T5    | Conditional jump-to-next (JZ L1 -> L1:)    | 3      | 2     | 1       | 0.01      | [PASS]
T6    | Jump across intermediate labels (JMP L1 -> | 4      | 3     | 1       | 0.01      | [PASS]
T7    | Jump NOT to next instruction (intervening  | 4      | 4     | 0       | 0.01      | [PASS]
T8    | MOV R1,R2 / MOV R2,R1 (Proves scope: retai | 3      | 3     | 0       | 0.01      | [PASS]
T9    | Case-insensitive register matching (mov r1 | 2      | 1     | 1       | 0.01      | [PASS]
T10   | Fixed-point iteration cascade (sample1.asm | 11     | 6     | 5       | 0.02      | [PASS]
T11   | 500-instruction benchmark for scale & perf | 501    | 301   | 200     | 0.81      | [PASS]
T12   | Bug Fix 1: Label sharing line with instruc | 6      | 4     | 2       | 0.03      | [PASS]
T13   | Bug Fix 2: Mixed-case jump target (jmp tar | 3      | 2     | 1       | 0.01      | [PASS]
P8    | Nearest-non-label rule (JMP L1; L0:; MOV;  | 5      | 3     | 2       | 0.01      | [PASS]
----------------------------------------------------------------------------------------
Total Test Suite Execution Time: 0.97 ms
>> ALL 14 TEST CASES (T1-T13 + P8) PASSED SUCCESSFULLY! <<
========================================================================================
```

---

## 5. Computational Complexity Analysis

### 5.1 Worst-Case Quadratic Complexity in Naive Implementation
In the baseline AI script, whenever an instruction at index i was deleted, the code immediately triggered:
```python
del instrs[i]
removed_one = True
break  # indices shifted, so rescan from the start
```
Because the list rescan unconditionally restarted from index 0:
- In an assembly sequence of N redundant instructions, restarting from 0 forces N + (N-1) + ... + 1 = O(N^2) comparisons.
- For cascaded instructions or reverse structures where the removable item is near the end, scanning N items, then N-1 items, then N-2 items results in:
  sum_(k=1)^N k = N(N+1)/2 = O(N^2) comparisons.

### 5.2 The Nearest-Non-Label Backtracking Rule
A naive attempt to prevent quadratic restarts is to simply backtrack one step: `i = max(0, i - 1)`. However, consider input **P8**:
```assembly
    JMP L1
L0:
    MOV R1, R1
L1:
    HALT
```
Here, `JMP L1` is at index 0, `L0:` is at index 1, and `MOV R1, R1` is at index 2.
1. When `MOV R1, R1` is deleted at index 2, setting `i = max(0, i - 1)` lands on index 1 (`L0:`).
2. Because `L0:` is a label, the loop skips it and advances to index 2 (`L1:`), failing to re-evaluate `JMP L1` at index 0 during that pass!
3. To resolve this correctly and maintain O(N) scanning, we implement the **Nearest-Non-Label Backtracking Rule**:
```python
k = i - 1
while k > 0 and instrs[k]['kind'] == 'label':
    k -= 1
i = max(0, k)
```
Upon deleting `MOV R1, R1`, the optimizer skips back past all intervening non-executable labels (`L0:`) directly to the nearest preceding executable instruction (`JMP L1`). This enables immediate identification and elimination of the exposed jump-to-next, transforming execution from quadratic O(N^2) to linear O(N).

### 5.3 Space Complexity
The optimizer maintains the instruction records in a single sequential list of size N, yielding strictly O(N) auxiliary space.

---

## 6. Limitations & Scope Boundaries

While the optimizer performs robustly within its domain, real-world compiler backends exhibit complexities that fall outside this scope:
1. **Unused Label Retention**: The optimizer does not eliminate orphaned labels (labels that are never referenced by any branch instruction). Removing unused labels requires constructing a global symbol table with reference counts.
2. **Sequential Move Inversion (`MOV A, B; MOV B, A`)**: The pair `MOV R1, R2` followed by `MOV R2, R1` contains a redundant second move only if `R2` is not overwritten and `R1` has not been modified. Safely eliminating this requires **live-variable analysis** and register-allocation def-use chains.
3. **Condition Code Flags Side Effects**: In certain architectures (e.g., x86 arithmetic or ARM `MOVS`), moves update processor status flags (Z, N, C, V). If a subsequent conditional branch relies on flags set by `MOV X, X`, removing it would alter program behavior. This optimizer targets architectures where simple moves do not perturb condition codes.

---

## 7. AI-Usage Declaration

### Tool Details
- **Tool Used:** Google Antigravity / Gemini 3.8
- **Date of Assistance:** November 20, 2026

### Prompts Given
1. *"Write a Python peephole optimizer for assembly code that eliminates redundant moves (MOV X, X) and jumps to the next instruction (JMP L / Jcc L) with fixed-point iteration."*
2. *"Provide sample test cases and outline the limitations and complexity of the approach."*
3. *"Refine the restart logic to handle cascaded jumps separated by intermediate labels using the nearest-non-label rule."*

### What the AI Tool Produced
The AI tool generated an initial script (`peephole_baseline.py`) with basic regular expressions for labels (`LABEL_RE = re.compile(r'^([A-Za-z_]\w*):$')`), moves, and jumps, alongside a loop that restarted from index 0 upon encountering any deletion.

### Weaknesses Identified & Corrections Implemented

#### 7.1 Bug 1: Parser Inability to Handle Inline Labels
- **Weakness:** The AI's regular expression `^([A-Za-z_]\w*):$` strictly required labels to stand completely alone on their line. In assembly listings where a label shares a line with an instruction (e.g. `L1: MOV R1, R1`), the AI parser matched neither the label nor the move, categorizing the line as `kind: 'other'`. Consequently, the instruction was never optimized, and the label was lost from the symbol map.
- **Before (AI Baseline):**
  ```python
  LABEL_RE = re.compile(r'^([A-Za-z_]\w*):$')
  # If line was "L1: MOV R1, R1", LABEL_RE returned None!
  # MOV_RE also returned None because of the leading label!
  ```
- **After (Our Fix):**
  ```python
  LABEL_LEAD_RE = re.compile(r'^([A-Za-z_]\w*):(?:\s*(.*))?$', re.IGNORECASE)
  # Decouples the label prefix, emits a 'label' record, and parses
  # the remainder instruction independently on the same source line.
  ```

#### 7.2 Bug 2: Case-Sensitive Label Name Comparison in Jumps
- **Weakness:** The AI's `jumps_to_next` function compared label names with strict case equality: `if instrs[j]['name'] == target:`. While register moves were matched case-insensitively, assembly labels like `jmp exit` jumping to `EXIT:` were missed.
- **Before (AI Baseline):**
  ```python
  def jumps_to_next(instrs, i):
      target = instrs[i]['target']
      j = i + 1
      while j < len(instrs) and instrs[j]['kind'] == 'label':
          if instrs[j]['name'] == target: # Strict case equality!
              return True
          j += 1
      return False
  ```
- **After (Our Fix):**
  ```python
  def jumps_to_next(instrs, i):
      target = instrs[i]['target'].upper()
      j = i + 1
      while j < len(instrs) and instrs[j]['kind'] == 'label':
          if instrs[j]['name'].upper() == target: # Robust case insensitivity
              return True
          j += 1
      return False
  ```

#### 7.3 Bug 3 / Weakness 3: Inefficient Full-Restart Loop and the Nearest-Non-Label Rule
- **Weakness:** The AI optimizer broke out of the loop and restarted list iteration from element 0 upon every single deletion (`del instrs[i]; break`), causing O(N^2) execution. A naive backtrack `i = max(0, i - 1)` fails when intervening labels precede the deleted instruction (as in `JMP L1; L0:; MOV R1, R1; L1:`).
- **Before (AI Baseline):**
  ```python
  del instrs[i]
  removed_one = True
  break   # indices shifted, so rescan from the start (O(n^2))
  ```
- **After (Our Fix - Nearest-Non-Label Rule):**
  ```python
  del instrs[i]
  removed_one = True
  # Backtrack past any non-executable labels to the nearest preceding non-label instruction (or 0)
  k = i - 1
  while k > 0 and instrs[k]['kind'] == 'label':
      k -= 1
  i = max(0, k)
  ```

---

## 8. Conclusion

The developed Peephole Optimizer successfully eliminates redundant moves and fall-through jumps while handling multi-pass cascading transformations to a provable fixed point. By addressing key edge cases in lexical analysis, case normalization, and index backtracking via the nearest-non-label rule, the system provides a robust, fast, and semantically sound post-code-generation optimization phase suitable for compiler design pipelines.

---

## Appendix A: Complete Annotated Source Code (`peephole.py`)

Below is the complete source code of `peephole.py` with line numbers as included in the project distribution zip file:

```python
  1: #!/usr/bin/env python3
  2: """
  3: Q43 - Peephole optimizer for a small assembly listing.
  4: 
  5: Removes:
  6:   1. Redundant moves            MOV X, X
  7:   2. Jumps to the next instr.   JMP L  (or Jcc L) immediately followed,
  8:                                  through any labels, by the label L
  9: 
 10: Because removing one instruction can expose another (e.g. removing
 11: "MOV R4, R4" can make "JZ L2" jump to the next instruction), the rules
 12: are applied repeatedly until a full pass makes no change (fixed point).
 13: 
 14: Enhancements / Bug Fixes over initial AI baseline:
 15:   - Fix 1: Supports labels sharing a line with an instruction (e.g., 'L1: MOV R1, R2').
 16:            Splits label definition from the instruction so neither is lost or misclassified.
 17:   - Fix 2: Case-insensitive label and jump target matching (e.g., 'jmp l1' -> 'L1:').
 18:   - Fix 3: Robust operand whitespace trimming and format handling.
 19:   - Fix 4: Optimized fixed-point iteration pass avoiding quadratic full-restart scans.
 20: 
 21: Usage:
 22:     python3 peephole.py input.asm [output.asm]
 23: """
 24: import re
 25: import sys
 26: 
 27: # Regex definitions
 28: LABEL_LEAD_RE = re.compile(r'^([A-Za-z_]\w*):(?:\s*(.*))?$', re.IGNORECASE)
 29: MOV_RE = re.compile(r'^MOV\s+([^,\s]+(?:\s+[^,\s]+)*)\s*,\s*([^,\s]+(?:\s+[^,\s]+)*)$', re.IGNORECASE)
 30: JUMP_RE = re.compile(r'^(J\w*)\s+([A-Za-z_]\w*)$', re.IGNORECASE)
 31: 
 32: 
 33: def strip_comment(line: str) -> str:
 34:     """Remove everything from ';' to the end of the line and trim spaces."""
 35:     return line.split(';', 1)[0].strip()
 36: 
 37: 
 38: def parse(lines):
 39:     """Turn raw source lines into a list of instruction records.
 40:     Blank and comment-only lines are dropped.
 41:     Supports standalone labels as well as inline labels (e.g., 'L1: MOV R1, R1')."""
 42:     instrs = []
 43:     for lineno, raw in enumerate(lines, start=1):
 44:         code = strip_comment(raw)
 45:         if not code:
 46:             continue
 47: 
 48:         # Check for leading label (either alone or followed by an instruction)
 49:         m_label = LABEL_LEAD_RE.match(code)
 50:         if m_label:
 51:             label_name = m_label.group(1)
 52:             remainder = m_label.group(2).strip() if m_label.group(2) else ""
 53:             
 54:             # Emit label record
 55:             instrs.append({
 56:                 'line': lineno,
 57:                 'text': f"{label_name}:",
 58:                 'kind': 'label',
 59:                 'name': label_name
 60:             })
 61:             
 62:             if not remainder:
 63:                 continue
 64:             # Parse remainder instruction on same line
 65:             code = remainder
 66:             raw_instr = remainder
 67:         else:
 68:             raw_instr = raw.rstrip()
 69: 
 70:         base = {'line': lineno, 'text': raw_instr}
 71: 
 72:         m_mov = MOV_RE.match(code)
 73:         if m_mov:
 74:             instrs.append({
 75:                 **base,
 76:                 'kind': 'mov',
 77:                 'dst': m_mov.group(1).strip(),
 78:                 'src': m_mov.group(2).strip()
 79:             })
 80:             continue
 81: 
 82:         m_jump = JUMP_RE.match(code)
 83:         if m_jump:
 84:             instrs.append({
 85:                 **base,
 86:                 'kind': 'jump',
 87:                 'op': m_jump.group(1).upper(),
 88:                 'target': m_jump.group(2).strip()
 89:             })
 90:             continue
 91: 
 92:         # Anything else (ADD, HALT, etc.) is kept untouched
 93:         instrs.append({**base, 'kind': 'other'})
 94: 
 95:     return instrs
 96: 
 97: 
 98: def jumps_to_next(instrs, i):
 99:     """True if the jump at index i falls through to its own target label.
100:     We skip over consecutive non-executable labels.
101:     Label comparison is case-insensitive."""
102:     target = instrs[i]['target'].upper()
103:     j = i + 1
104:     while j < len(instrs) and instrs[j]['kind'] == 'label':
105:         if instrs[j]['name'].upper() == target:
106:             return True
107:         j += 1
108:     return False
109: 
110: 
111: def optimize(instrs):
112:     """Apply peephole rules until a fixed point is reached.
113:     Returns (optimized_list, log) where log holds (line, text, reason)."""
114:     log = []
115:     while True:
116:         removed_one = False
117:         i = 0
118:         while i < len(instrs):
119:             ins = instrs[i]
120:             reason = None
121:             if ins['kind'] == 'mov' and ins['dst'].upper() == ins['src'].upper():
122:                 reason = 'redundant move (dst == src)'
123:             elif ins['kind'] == 'jump' and jumps_to_next(instrs, i):
124:                 reason = f"{ins['op']} to next instruction"
125: 
126:             if reason:
127:                 log.append((ins['line'], ins['text'].strip(), reason))
128:                 del instrs[i]
129:                 removed_one = True
130:                 # Nearest-non-label rule: removing an instruction can expose an earlier instruction
131:                 # (e.g., JMP L1 followed by label L0: and then a now-removed redundant MOV).
132:                 # Backtrack past any non-executable labels to the nearest preceding non-label instruction (or 0).
133:                 k = i - 1
134:                 while k > 0 and instrs[k]['kind'] == 'label':
135:                     k -= 1
136:                 i = max(0, k)
137:             else:
138:                 i += 1
139: 
140:         if not removed_one:
141:             return instrs, log
142: 
143: 
144: def main():
145:     if len(sys.argv) < 2:
146:         print(__doc__)
147:         sys.exit(1)
148: 
149:     with open(sys.argv[1], encoding='utf-8') as f:
150:         lines = f.readlines()
151: 
152:     before = parse(lines)
153:     after, log = optimize(list(before))
154: 
155:     print("=== Before ===")
156:     for ins in before:
157:         print(ins['text'])
158: 
159:     print("\n=== After ===")
160:     for ins in after:
161:         print(ins['text'])
162: 
163:     print("\n=== Removed ===")
164:     if not log:
165:         print("(nothing to remove)")
166:     for line, text, reason in log:
167:         print(f"line {line}: {text:<22} -> {reason}")
168: 
169:     print(f"\n{len(before)} instructions before, {len(after)} after.")
170: 
171:     if len(sys.argv) > 2:
172:         with open(sys.argv[2], 'w', encoding='utf-8') as f:
173:             f.write('\n'.join(ins['text'] for ins in after) + '\n')
174:         print(f"Optimized listing written to {sys.argv[2]}")
175: 
176: 
177: if __name__ == '__main__':
178:     main()
```

---

## Appendix B: Complete Prompt History
- Prompt 1: "Design a peephole optimizer for small assembly code removing MOV X,X and JMP to next instruction using Python."
- Prompt 2: "Show expected output on sample1.asm and specify edge cases including empty files, cascading jumps, and performance benchmarks."
- Prompt 3: "Analyze gaps regarding inline labels, case-folding, and worst-case iteration overhead."
- Prompt 4: "Change the restart line in peephole.py to replace i = max(0, i - 1) with the nearest-non-label rule to correctly catch cascaded jumps separated by labels (such as in P8: JMP L1; L0:; MOV R1, R1; L1:; HALT)."
