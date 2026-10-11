#!/usr/bin/env python3
"""Small compiler regression-testing demo for well-defined uint32 operations."""
from __future__ import annotations
import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "tests" / "compute.cpp"
BUILD = ROOT / "build"
REPORTS = ROOT / "reports"
MASK = (1 << 32) - 1
OPS = ("add", "sub", "mul", "and", "or", "xor", "shl", "shr")


def reference(op: str, a: int, b: int) -> int:
    if op == "add": value = a + b
    elif op == "sub": value = a - b
    elif op == "mul": value = a * b
    elif op == "and": value = a & b
    elif op == "or": value = a | b
    elif op == "xor": value = a ^ b
    elif op == "shl": value = a << (b % 32)
    elif op == "shr": value = a >> (b % 32)
    else: raise ValueError(f"Unknown operation: {op}")
    return value & MASK


def make_cases(random_count: int, seed: int):
    # Boundary values and pairs, then deterministic pseudo-random cases.
    values = [0, 1, 2, 31, 32, 255, 256, 65535, 0x7fffffff, 0xffffffff]
    cases = [(op, a, b) for op in OPS for a, b in (
        (0, 0), (1, 0), (0, 1), (MASK, 1), (MASK, MASK),
        (0x7fffffff, 2), (255, 1), (1, 31), (1, 32), (0x80000000, 1)
    )]
    for op in OPS:
        for a in values:
            for b in values:
                cases.append((op, a, b))
    rng = random.Random(seed)
    for _ in range(random_count):
        cases.append((rng.choice(OPS), rng.getrandbits(32), rng.randrange(0, 64)))
    # Keep each test case unique while preserving order.
    return list(dict.fromkeys(cases))


def compile_program(compiler: str, optimization: str) -> Path:
    BUILD.mkdir(exist_ok=True)
    exe = BUILD / ("compute_" + optimization.replace("-", ""))
    cmd = [compiler, "-std=c++17", optimization, "-Wall", "-Wextra", str(SOURCE), "-o", str(exe)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Compilation failed ({' '.join(cmd)}):\n{result.stderr}")
    return exe


def run_one(exe: Path, op: str, a: int, b: int) -> int:
    proc = subprocess.run([str(exe)], input=f"{op} {a} {b}\n", capture_output=True, text=True, timeout=3)
    if proc.returncode != 0:
        raise RuntimeError(f"Program exited {proc.returncode}: {proc.stderr.strip()}")
    try:
        return int(proc.stdout.strip())
    except ValueError as exc:
        raise RuntimeError(f"Unexpected output: {proc.stdout!r}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", default="g++", help="C++ compiler executable (default: g++)")
    parser.add_argument("--random", type=int, default=100, help="number of deterministic random tests")
    parser.add_argument("--seed", type=int, default=2026, help="random test seed")
    args = parser.parse_args()
    if args.random < 0:
        parser.error("--random must be non-negative")
    cases = make_cases(args.random, args.seed)
    REPORTS.mkdir(exist_ok=True)
    summary = {"project": "Mini Compiler Verification Framework", "compiler": args.compiler,
               "seed": args.seed, "test_cases_per_build": len(cases), "builds": []}
    total_failed = 0

    for optimization in ("-O0", "-O2"):
        exe = compile_program(args.compiler, optimization)
        failures = []
        for op, a, b in cases:
            expected = reference(op, a, b)
            try:
                actual = run_one(exe, op, a, b)
                if actual != expected:
                    failures.append({"op": op, "a": a, "b": b, "expected": expected, "actual": actual})
            except (RuntimeError, subprocess.TimeoutExpired) as exc:
                failures.append({"op": op, "a": a, "b": b, "error": str(exc)})
        passed = len(cases) - len(failures)
        total_failed += len(failures)
        summary["builds"].append({"optimization": optimization, "passed": passed,
                                  "failed": len(failures), "failures": failures[:50]})
        print(f"[{optimization}] {passed}/{len(cases)} passed; {len(failures)} failed")
        for failure in failures[:5]:
            print("  FAILURE:", failure)

    report_path = REPORTS / "latest_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Report saved to: {report_path.relative_to(ROOT)}")
    print("RESULT:", "PASS" if total_failed == 0 else "FAIL")
    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
