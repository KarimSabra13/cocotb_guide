# DV Junior Verification Exercise

## Overview
This is an **interview-level exercise** based on the 3 sections we've covered:
1. **Logging** - Professional multi-handler logging setup
2. **Variables** - Dynamic typing and data structures (dicts, lists)
3. **Operators** - Arithmetic, comparison, logical, and bitwise operations

## Your Task

Complete `verification_exercise.py` by implementing 4 functions:

### Task 1: Transaction Generator
Generate N AXI write transactions with:
- Incrementing address pattern (stride = 16 bytes)
- Alternating burst types (INCR/FIXED)
- Realistic data values
- Return as list of dictionaries

### Task 2: Control Word Encoder
Pack transaction fields into a 16-bit control word using **bitwise operations**:
```
[15:14] priority    [13:12] burst_type   [11:8] tx_id
[7:4]   write_strobe   [3:0] control_flags
```
This is a **realistic AXI control encoding** problem.

### Task 3: Response Checker with Logging
Implement a checker that:
- Sets up multi-handler logger (console + file)
- Compares expected vs received transactions
- Logs DEBUG for passes, ERROR for failures
- Returns match status and comparison details

### Task 4: Complete Test Sequence
Orchestrate a full verification:
1. Generate 5 transactions
2. Simulate DUT responses (inject controlled errors)
3. Run all comparisons
4. Report statistics (pass/fail counts, success rate)

## What Makes This Interview-Level?

✅ **Hardware Verification Realism**: Uses actual AXI transaction patterns
✅ **Bitwise Encoding**: Tests understanding of low-level register packing
✅ **Logging Best Practices**: Multi-handler setup from Section 1
✅ **Dynamic Typing**: Leverages Python flexibility with dictionaries
✅ **Error Injection**: Shows you understand real testbench failures
✅ **Statistical Analysis**: Professional pass/fail tracking

## How I'll Review Your Code

### Code Quality (60%)
- [ ] Does the code work without errors?
- [ ] Are variable names clear and descriptive?
- [ ] Is the logic easy to follow?
- [ ] Do you use Python idioms (list comprehension, dict iteration, etc.)?

### Correctness (30%)
- [ ] Transaction generator produces correct addresses/data?
- [ ] Bitwise encoding matches the bit layout specification?
- [ ] Logging captures all information at correct levels?
- [ ] Statistics calculation is accurate?

### Performance & Tricks (10%)
- [ ] Do you avoid unnecessary loops/calculations?
- [ ] Do you use modulo arithmetic effectively?
- [ ] Do you leverage collection methods (append, get, copy)?
- [ ] Any clever Python tricks for readability?

## The Review Process

When you submit:
1. **I run your code** against test cases
2. **I compare to reference solution** (verification_exercise_SOLUTION.py)
3. **I provide detailed feedback**:
   - What went well
   - What could be improved
   - Tips & tricks used in reference solution
   - Interview tips specific to DV roles

## Hints (Increasing Difficulty)

**Easy Hints:**
- Use `for i in range(num_transactions)` for the loop
- Dictionaries are perfect for storing transaction data
- Address = base + (i * stride)

**Medium Hints:**
- Modulo arithmetic: `i % 2` for alternating patterns
- List indexing with modulo: `data_pool[i % len(data_pool)]`
- Bit shifts: `value << bits_to_shift`

**Hard Hints (Don't look!):**
```
# Bitwise combination pattern:
result = (field1 << position1) | (field2 << position2) | ...

# Mask pattern to prevent overflow:
masked_value = raw_value & ((1 << num_bits) - 1)

# Logger levels: DEBUG for detail, ERROR for failures
# Use printf-style: logger.info("format %d", value)
```

## Expected Output

When you run the solution correctly:

```
INFO | Starting verification test
INFO | Generating 5 transactions...
INFO |   [Injected] Transaction 2: data error
INFO |   [Injected] Transaction 4: address error
INFO | Comparing transactions...
INFO | ============================================================
DEBUG | Transaction 0 comparison
DEBUG |   addr: 0x1000 == 0x1000 ? PASS
DEBUG |   data: 0xDEADBEEF == 0xDEADBEEF ? PASS
...
ERROR |   MISMATCH in data: expected=0x12345678, received=0x99999999
...
INFO | ============================================================
INFO | Test Statistics:
INFO |   Total transactions: 5
INFO |   Passed: 4
INFO |   Failed: 1
INFO |   Success rate: 80.0%
INFO | VERDICT: 1 TESTS FAILED - Review errors above
```

## Files

- `verification_exercise.py` - **Your work here** (template with docstrings)
- `verification_exercise_SOLUTION.py` - **Reference solution** (don't peek early!)
- `README.md` - This file

## Let's Go!

Ready? Start coding in `verification_exercise.py`. When you're done, I'll review it and provide detailed feedback with DV-specific tips and tricks.

---

**Difficulty Level:** ⭐⭐⭐ (Junior DV, 1-2 years experience)
**Time Estimate:** 45-60 minutes
**Concepts Tested:** Variables, Operators, Logging, Data Structures, Hardware Protocols
