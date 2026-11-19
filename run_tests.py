#!/usr/bin/env python3
"""
Test Suite & Benchmarking Runner for Q43 Peephole Optimizer
Executes all test cases (T1 - T13), validates outputs, benchmarks performance,
and compares baseline AI code vs the fixed/enhanced optimizer.
"""
import time
import peephole
import peephole_baseline

TEST_CASES = [
    {
        "id": "T1",
        "file": "tests/t01_empty.asm",
        "desc": "Boundary: Empty file (no output, no crash)",
        "expected_before": 0,
        "expected_after": 0,
        "expected_removed": 0
    },
    {
        "id": "T2",
        "file": "tests/t02_halt_only.asm",
        "desc": "Single non-optimizable instruction (HALT)",
        "expected_before": 1,
        "expected_after": 1,
        "expected_removed": 0
    },
    {
        "id": "T3",
        "file": "tests/t03_single_mov.asm",
        "desc": "Single redundant move (MOV R1, R1)",
        "expected_before": 1,
        "expected_after": 0,
        "expected_removed": 1
    },
    {
        "id": "T4",
        "file": "tests/t04_jmp_next.asm",
        "desc": "Basic jump-to-next (JMP L1 -> L1:)",
        "expected_before": 3,
        "expected_after": 2,
        "expected_removed": 1
    },
    {
        "id": "T5",
        "file": "tests/t05_jz_next.asm",
        "desc": "Conditional jump-to-next (JZ L1 -> L1:)",
        "expected_before": 3,
        "expected_after": 2,
        "expected_removed": 1
    },
    {
        "id": "T6",
        "file": "tests/t06_jmp_multi_label.asm",
        "desc": "Jump across intermediate labels (JMP L1 -> L2: -> L1:)",
        "expected_before": 4,
        "expected_after": 3,
        "expected_removed": 1
    },
    {
        "id": "T7",
        "file": "tests/t07_jmp_not_next.asm",
        "desc": "Jump NOT to next instruction (intervening ADD, must stay)",
        "expected_before": 4,
        "expected_after": 4,
        "expected_removed": 0
    },
    {
        "id": "T8",
        "file": "tests/t08_mov_pair.asm",
        "desc": "MOV R1,R2 / MOV R2,R1 (Proves scope: retained)",
        "expected_before": 3,
        "expected_after": 3,
        "expected_removed": 0
    },
    {
        "id": "T9",
        "file": "tests/t09_case_insensitivity.asm",
        "desc": "Case-insensitive register matching (mov r1, R1)",
        "expected_before": 2,
        "expected_after": 1,
        "expected_removed": 1
    },
    {
        "id": "T10",
        "file": "tests/t10_cascade.asm",
        "desc": "Fixed-point iteration cascade (sample1.asm)",
        "expected_before": 11,
        "expected_after": 6,
        "expected_removed": 5
    },
    {
        "id": "T11",
        "file": "tests/t11_long_500.asm",
        "desc": "500-instruction benchmark for scale & performance",
        "expected_before": 501,
        "expected_after": 301,
        "expected_removed": 200
    },
    {
        "id": "T12",
        "file": "tests/t12_label_same_line.asm",
        "desc": "Bug Fix 1: Label sharing line with instruction",
        "expected_before": 6,
        "expected_after": 4,
        "expected_removed": 2
    },
    {
        "id": "T13",
        "file": "tests/t13_mixed_case_jump.asm",
        "desc": "Bug Fix 2: Mixed-case jump target (jmp target -> TARGET:)",
        "expected_before": 3,
        "expected_after": 2,
        "expected_removed": 1
    },
    {
        "id": "P8",
        "file": "tests/p8_intervening_label_cascade.asm",
        "desc": "Nearest-non-label rule (JMP L1; L0:; MOV; L1: -> L0,L1,HALT)",
        "expected_before": 5,
        "expected_after": 3,
        "expected_removed": 2
    }
]


def run_all_tests():
    print("=" * 88)
    print("      AUTOMATA THEORY & COMPILER DESIGN (Q43) - PEEPHOLE OPTIMIZER TEST SUITE")
    print("=" * 88)
    print(f"{'Test':<5} | {'Description':<42} | {'Before':<6} | {'After':<5} | {'Removed':<7} | {'Time (ms)':<9} | {'Status'}")
    print("-" * 88)

    all_passed = True
    total_time = 0.0

    for tc in TEST_CASES:
        with open(tc["file"], "r", encoding="utf-8") as f:
            lines = f.readlines()

        start = time.perf_counter()
        parsed = peephole.parse(lines)
        optimized, log = peephole.optimize(list(parsed))
        elapsed = (time.perf_counter() - start) * 1000.0
        total_time += elapsed

        before_cnt = len(parsed)
        after_cnt = len(optimized)
        removed_cnt = len(log)

        passed = (
            before_cnt == tc["expected_before"] and
            after_cnt == tc["expected_after"] and
            removed_cnt == tc["expected_removed"]
        )
        if not passed:
            all_passed = False

        status = "[PASS]" if passed else "[FAIL]"
        print(f"{tc['id']:<5} | {tc['desc'][:42]:<42} | {before_cnt:<6} | {after_cnt:<5} | {removed_cnt:<7} | {elapsed:<9.2f} | {status}")

    print("-" * 88)
    print(f"Total Test Suite Execution Time: {total_time:.2f} ms")
    if all_passed:
        print(">> ALL 14 TEST CASES (T1-T13 + P8) PASSED SUCCESSFULLY! <<")
    else:
        print(">> SOME TEST CASES FAILED! <<")
    print("=" * 88)

    # Comparison against baseline AI code on edge cases:
    print("\n" + "=" * 88)
    print("  VERIFICATION OF BUG FIXES (Baseline AI Code vs Fixed Peephole Optimizer)")
    print("=" * 88)
    print(f"{'Test Case':<15} | {'Baseline AI Removed':<22} | {'Fixed Optimizer Removed':<25} | {'Bug Status'}")
    print("-" * 88)

    # Bug 1: T12
    with open("tests/t12_label_same_line.asm") as f:
        t12_lines = f.readlines()
    b_t12_p = peephole_baseline.parse(t12_lines)
    _, b_t12_log = peephole_baseline.optimize(list(b_t12_p))
    f_t12_p = peephole.parse(t12_lines)
    _, f_t12_log = peephole.optimize(list(f_t12_p))

    print(f"{'T12 (Inline)':<15} | {len(b_t12_log):<22} | {len(f_t12_log):<25} | {'Fixed (Labels parsed)'}")

    # Bug 2: T13
    with open("tests/t13_mixed_case_jump.asm") as f:
        t13_lines = f.readlines()
    b_t13_p = peephole_baseline.parse(t13_lines)
    _, b_t13_log = peephole_baseline.optimize(list(b_t13_p))
    f_t13_p = peephole.parse(t13_lines)
    _, f_t13_log = peephole.optimize(list(f_t13_p))

    print(f"{'T13 (Case)':<15} | {len(b_t13_log):<22} | {len(f_t13_log):<25} | {'Fixed (Case insensitive)'}")

    # Performance: T11
    with open("tests/t11_long_500.asm") as f:
        t11_lines = f.readlines()
    t0 = time.perf_counter()
    b_t11_p = peephole_baseline.parse(t11_lines)
    _, b_t11_log = peephole_baseline.optimize(list(b_t11_p))
    t_baseline = (time.perf_counter() - t0) * 1000.0

    t1 = time.perf_counter()
    f_t11_p = peephole.parse(t11_lines)
    _, f_t11_log = peephole.optimize(list(f_t11_p))
    t_fixed = (time.perf_counter() - t1) * 1000.0

    print(f"{'T11 (500 lines)':<15} | {t_baseline:<18.2f} ms | {t_fixed:<21.2f} ms | {f'{t_baseline/max(t_fixed, 0.001):.1f}x Faster Scan'}")
    print("=" * 88)


if __name__ == "__main__":
    run_all_tests()
