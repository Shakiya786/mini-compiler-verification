# Mini Compiler Verification Framework

A Python and C++ portfolio project demonstrating automated testing of program correctness across compiler optimization levels.

The framework generates deterministic boundary-value and pseudo-random test cases, compiles a C++17 test program with GCC using `-O0` and `-O2`, compares program outputs against an independent Python reference model, and generates a JSON test report.

> **Scope:** This is a CPU compiler-testing demonstration. It does not validate NVIDIA's compiler, CUDA, or GPU hardware.

## Features

- **Automated test generation:** Boundary-value and seeded pseudo-random test cases.
- **Arithmetic and bitwise operations:** Addition, subtraction, multiplication, AND, OR, XOR, left shift, and right shift.
- **Optimization-level comparison:** Tests builds compiled with GCC `-O0` and `-O2`.
- **Reference-based verification:** Compares C++ program outputs against expected results calculated in Python.
- **Failure tracking:** Records mismatches and execution errors.
- **JSON reporting:** Saves test results to `reports/latest_report.json`.
- **Reproducible testing:** Supports a configurable random seed.

## Technology Stack

- Python
- C++17
- GCC/G++
- JSON
- PowerShell / VS Code

## Requirements

- Python 3.9 or later
- GCC/G++ with C++17 support
- Windows, Linux, or another environment compatible with the compiler and Python script

## Project Structure

```text
mini-compiler-verification/
├── tests/
│   └── compute.cpp
├── build/
├── reports/
│   └── latest_report.json
├── verify.py
├── README.md
└── .gitignore
```

The `build/` directory contains generated executables, and `reports/` contains generated test reports. These directories may be created when the framework runs.

## Running on Windows

1. Install Python and a compatible GCC/G++ compiler.
2. Ensure `python` and `g++` are available in your terminal.
3. Open the project folder in VS Code.
4. Open a PowerShell terminal in the project directory.
5. Verify the installations:

```powershell
python --version
g++ --version
```

Run the default verification suite:

```powershell
python verify.py
```

Run additional pseudo-random test cases:

```powershell
python verify.py --random 500
```

Use a specific random seed:

```powershell
python verify.py --random 500 --seed 2026
```

If the compiler is not available under the name `g++`, specify its executable path:

```powershell
python verify.py --compiler "C:\path\to\g++.exe"
```

## Example Results

In one recorded run using seed `2026`, the framework produced the following results:

| Configuration | Passed | Failed |
|---|---:|---:|
| `-O0` | 908 | 0 |
| `-O2` | 908 | 0 |

Total successful test executions: **1,816**.

These results apply to the tested program and test cases; they do not prove that the compiler is free of bugs.

Test counts may vary depending on the selected random-case count and duplicate removal.

## How It Works

1. **Test generation:** `make_cases()` creates boundary-value and deterministic pseudo-random test cases.
2. **Reference calculation:** `reference()` computes expected results using Python and explicit 32-bit masking.
3. **Compilation:** `compile_program()` builds the C++ program at `-O0` and `-O2`.
4. **Execution:** `run_one()` supplies each test input to the compiled executable and captures its output.
5. **Comparison:** The framework compares actual results against the reference results.
6. **Reporting:** Pass counts, failures, and build configurations are written to `reports/latest_report.json`.

## Validation

The framework was tested by deliberately introducing an error into the addition operation. The verification script detected the resulting output mismatches against the Python reference model.

The original implementation was then restored and the test suite rerun.

## Limitations

- The project tests a predefined set of arithmetic and bitwise operations rather than arbitrary C++ programs.
- Passing tests establish correctness only for the tested inputs and behaviors.
- The framework does not independently validate GCC or inspect generated machine code.
- CUDA, PTX, and GPU execution are not currently supported.
- The test suite is a learning-scale demonstration, not a production compiler-validation system.

## Future Improvements

- Differential testing with GCC and Clang.
- Sanitizer-enabled builds.
- Additional regression and edge-case tests.
- More comprehensive failure diagnostics.
- CUDA kernel testing and PTX inspection when a suitable NVIDIA development environment is available.