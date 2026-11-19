#!/usr/bin/env python3
"""
Baseline (Original AI-generated) Peephole Optimizer
Q43 - Peephole optimizer for a small assembly listing.

Removes:
  1. Redundant moves            MOV X, X
  2. Jumps to the next instr.   JMP L  (or Jcc L) immediately followed,
                                 through any labels, by the label L
"""
import re
import sys

# Comments start with ';'. Labels look like "L1:" on their own line.
LABEL_RE = re.compile(r'^([A-Za-z_]\w*):$')
MOV_RE = re.compile(r'^MOV\s+([^,\s]+)\s*,\s*([^,\s]+)$', re.IGNORECASE)
JUMP_RE = re.compile(r'^(J\w*)\s+([A-Za-z_]\w*)$', re.IGNORECASE)


def strip_comment(line):
    """Remove everything from ';' to the end of the line and trim spaces."""
    return line.split(';', 1)[0].strip()


def parse(lines):
    """Turn raw source lines into a list of instruction records.
    Blank and comment-only lines are dropped."""
    instrs = []
    for lineno, raw in enumerate(lines, start=1):
        code = strip_comment(raw)
        if not code:
            continue
        base = {'line': lineno, 'text': raw.rstrip()}

        m = LABEL_RE.match(code)
        if m:
            instrs.append({**base, 'kind': 'label', 'name': m.group(1)})
            continue

        m = MOV_RE.match(code)
        if m:
            instrs.append({**base, 'kind': 'mov',
                           'dst': m.group(1), 'src': m.group(2)})
            continue

        m = JUMP_RE.match(code)
        if m:
            instrs.append({**base, 'kind': 'jump',
                           'op': m.group(1).upper(), 'target': m.group(2)})
            continue

        # Anything else (ADD, HALT, ...) is kept untouched.
        instrs.append({**base, 'kind': 'other'})
    return instrs


def jumps_to_next(instrs, i):
    """True if the jump at index i falls through to its own target label.
    We skip over consecutive labels, since they are not executable."""
    target = instrs[i]['target']
    j = i + 1
    while j < len(instrs) and instrs[j]['kind'] == 'label':
        if instrs[j]['name'] == target:
            return True
        j += 1
    return False


def optimize(instrs):
    """Apply the peephole rules until nothing changes.
    Returns (optimized_list, log) where log holds (line, text, reason)."""
    log = []
    while True:
        removed_one = False
        for i, ins in enumerate(instrs):
            reason = None
            if ins['kind'] == 'mov' and ins['dst'].upper() == ins['src'].upper():
                reason = 'redundant move (dst == src)'
            elif ins['kind'] == 'jump' and jumps_to_next(instrs, i):
                reason = f"{ins['op']} to next instruction"

            if reason:
                log.append((ins['line'], ins['text'].strip(), reason))
                del instrs[i]
                removed_one = True
                break   # indices shifted, so rescan from the start
        if not removed_one:
            return instrs, log


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    with open(sys.argv[1]) as f:
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
        with open(sys.argv[2], 'w') as f:
            f.write('\n'.join(ins['text'] for ins in after) + '\n')
        print(f"Optimized listing written to {sys.argv[2]}")


if __name__ == '__main__':
    main()
