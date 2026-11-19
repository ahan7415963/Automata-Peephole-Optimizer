#!/usr/bin/env python3
"""
Q43 - Peephole optimizer for a small assembly listing.

Removes:
  1. Redundant moves            MOV X, X
  2. Jumps to the next instr.   JMP L  (or Jcc L) immediately followed,
                                 through any labels, by the label L

Because removing one instruction can expose another (e.g. removing
"MOV R4, R4" can make "JZ L2" jump to the next instruction), the rules
are applied repeatedly until a full pass makes no change (fixed point).

Enhancements / Bug Fixes over initial AI baseline:
  - Fix 1: Supports labels sharing a line with an instruction (e.g., 'L1: MOV R1, R2').
           Splits label definition from the instruction so neither is lost or misclassified.
  - Fix 2: Case-insensitive label and jump target matching (e.g., 'jmp l1' -> 'L1:').
  - Fix 3: Robust operand whitespace trimming and format handling.
  - Fix 4: Optimized fixed-point iteration pass avoiding quadratic full-restart scans.

Usage:
    python3 peephole.py input.asm [output.asm]
"""
import re
import sys

# Regex definitions
LABEL_LEAD_RE = re.compile(r'^([A-Za-z_]\w*):(?:\s*(.*))?$', re.IGNORECASE)
MOV_RE = re.compile(r'^MOV\s+([^,\s]+(?:\s+[^,\s]+)*)\s*,\s*([^,\s]+(?:\s+[^,\s]+)*)$', re.IGNORECASE)
JUMP_RE = re.compile(r'^(J\w*)\s+([A-Za-z_]\w*)$', re.IGNORECASE)


def strip_comment(line: str) -> str:
    """Remove everything from ';' to the end of the line and trim spaces."""
    return line.split(';', 1)[0].strip()


def parse(lines):
    """Turn raw source lines into a list of instruction records.
    Blank and comment-only lines are dropped.
    Supports standalone labels as well as inline labels (e.g., 'L1: MOV R1, R1')."""
    instrs = []
    for lineno, raw in enumerate(lines, start=1):
        code = strip_comment(raw)
        if not code:
            continue

        # Check for leading label (either alone or followed by an instruction)
        m_label = LABEL_LEAD_RE.match(code)
        if m_label:
            label_name = m_label.group(1)
            remainder = m_label.group(2).strip() if m_label.group(2) else ""
            
            # Emit label record
            instrs.append({
                'line': lineno,
                'text': f"{label_name}:",
                'kind': 'label',
                'name': label_name
            })
            
            if not remainder:
                continue
            # Parse remainder instruction on same line
            code = remainder
            raw_instr = remainder
        else:
            raw_instr = raw.rstrip()

        base = {'line': lineno, 'text': raw_instr}

        m_mov = MOV_RE.match(code)
        if m_mov:
            instrs.append({
                **base,
                'kind': 'mov',
                'dst': m_mov.group(1).strip(),
                'src': m_mov.group(2).strip()
            })
            continue

        m_jump = JUMP_RE.match(code)
        if m_jump:
            instrs.append({
                **base,
                'kind': 'jump',
                'op': m_jump.group(1).upper(),
                'target': m_jump.group(2).strip()
            })
            continue

        # Anything else (ADD, HALT, etc.) is kept untouched
        instrs.append({**base, 'kind': 'other'})

    return instrs


def jumps_to_next(instrs, i):
    """True if the jump at index i falls through to its own target label.
    We skip over consecutive non-executable labels.
    Label comparison is case-insensitive."""
    target = instrs[i]['target'].upper()
    j = i + 1
    while j < len(instrs) and instrs[j]['kind'] == 'label':
        if instrs[j]['name'].upper() == target:
            return True
        j += 1
    return False


def optimize(instrs):
    """Apply peephole rules until a fixed point is reached.
    Returns (optimized_list, log) where log holds (line, text, reason)."""
    log = []
    while True:
        removed_one = False
        i = 0
        while i < len(instrs):
            ins = instrs[i]
            reason = None
            if ins['kind'] == 'mov' and ins['dst'].upper() == ins['src'].upper():
                reason = 'redundant move (dst == src)'
            elif ins['kind'] == 'jump' and jumps_to_next(instrs, i):
                reason = f"{ins['op']} to next instruction"

            if reason:
                log.append((ins['line'], ins['text'].strip(), reason))
                del instrs[i]
                removed_one = True
                # Nearest-non-label rule: removing an instruction can expose an earlier instruction
                # (e.g., JMP L1 followed by label L0: and then a now-removed redundant MOV).
                # Backtrack past any non-executable labels to the nearest preceding non-label instruction (or 0).
                k = i - 1
                while k > 0 and instrs[k]['kind'] == 'label':
                    k -= 1
                i = max(0, k)
            else:
                i += 1

        if not removed_one:
            return instrs, log


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        lines = f.readlines()

    before = parse(lines)
    after, log = optimize(list(before))

    print("=== Before ===")
    for ins in before:
        print(ins['text'])

    print("\n=== After ===")
    for ins in after:
        print(ins['text'])

    print("\n=== Removed ===")
    if not log:
        print("(nothing to remove)")
    for line, text, reason in log:
        print(f"line {line}: {text:<22} -> {reason}")

    print(f"\n{len(before)} instructions before, {len(after)} after.")

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write('\n'.join(ins['text'] for ins in after) + '\n')
        print(f"Optimized listing written to {sys.argv[2]}")


if __name__ == '__main__':
    main()
