"""
================================================================================
Python Variables and Data Types for Hardware Verification
================================================================================

This module demonstrates Python's dynamic typing system and core data types
with emphasis on hardware verification applications.

Key Difference from SystemVerilog:
- Python: Dynamic typing (inferred at runtime, changeable)
- SystemVerilog: Static typing (declared once, fixed)

This flexibility allows rapid testbench development while retaining clarity
through type hints and runtime checks.
================================================================================
"""

# ============================================================================
# SECTION 1: NUMERIC TYPES AND DYNAMIC TYPING
# ============================================================================
"""
Python infers variable types from assigned values. No explicit declarations
are needed. This contrasts with SystemVerilog (e.g., 'int x = 5;').

Benefit: Write code faster; check types at runtime when needed.
Risk: Implicit type conversions can hide bugs; use type() to verify.
"""

# Integer: Unlimited precision (no overflow unlike SystemVerilog logic[31:0])
transaction_id = 42
register_address = 0xDEADBEEF
# Python handles arbitrarily large integers automatically
large_value = 123456789123456789123456789

# Float: IEEE 754 64-bit double precision
clock_frequency = 100.5  # MHz
duty_cycle = 0.5         # 50% duty cycle
delay = 1.23e-9          # 1.23 nanoseconds (scientific notation)

# Complex: For signal processing (rare in verification, included for completeness)
# signal = 3 + 4j  # Real + Imaginary

# Type checking (useful in testbenches to catch errors early)
print(f"transaction_id type: {type(transaction_id)}")      # <class 'int'>
print(f"clock_frequency type: {type(clock_frequency)}")    # <class 'float'>

# Type conversion (coercion)
int_from_float = int(clock_frequency)        # 100 (truncates)
float_from_int = float(transaction_id)       # 42.0
string_number = str(register_address)        # '0xDEADBEEF'


# ============================================================================
# SECTION 2: STRING HANDLING (Critical for Verification)
# ============================================================================
"""
Strings are immutable sequences of characters. Crucial for:
- Test configuration and naming
- Log message construction
- Protocol field representations
- Report generation
"""

# Single vs double quotes (both equivalent in Python)
test_name_single = 'Write Transaction Test'
test_name_double = "Write Transaction Test"

# Triple quotes for multi-line strings (common in docstrings and long messages)
test_description = """
This test verifies write transaction:
1. Generate random address
2. Generate random data
3. Apply to DUT
4. Monitor response
"""

# String concatenation methods
addr = 0x1000
data = 0xCAFEBABE

# Method 1: Comma-separated (avoids string coercion errors)
log_msg_1 = "addr =", addr, "data =", data
print(log_msg_1)  # Prints as tuple

# Method 2: f-strings (recommended, efficient, readable)
log_msg_2 = f"addr = 0x{addr:08X}, data = 0x{data:08X}"
print(log_msg_2)  # addr = 0x00001000, data = 0xCAFEBABE

# Method 3: String formatting with .format()
log_msg_3 = "addr = 0x{:08X}, data = 0x{:08X}".format(addr, data)
print(log_msg_3)

# String methods (useful for parsing and text manipulation)
test_result = "PASS: All Assertions Cleared"
is_pass = test_result.startswith("PASS")    # True
is_fail = test_result.startswith("FAIL")    # False
uppercase = test_result.upper()             # "PASS: ALL ASSERTIONS CLEARED"
lowercase = test_result.lower()


# ============================================================================
# SECTION 3: BOOLEAN TYPE (Essential for Testbench Conditions)
# ============================================================================
"""
Boolean (bool) values are True or False. Critical for:
- Test pass/fail conditions
- Conditional stimulus application
- State machine logic
- Assertion evaluations
"""

# Boolean literals
test_passed = True
simulation_complete = False

# Boolean results from comparisons
response_valid = True
timeout_occurred = False
data_matches = (0xCAFEBABE == 0xCAFEBABE)    # True

# Boolean operators (all return bool)
both_true = test_passed and simulation_complete    # False
either_true = test_passed or simulation_complete   # True
not_passed = not test_passed                       # False

# Practical testbench condition
cycle_count = 150
max_cycles = 100
timeout = cycle_count > max_cycles  # True

if timeout:
    print("Timeout! Transaction did not complete within max cycles")

# Boolean as index/mask (common in verification)
transaction_types = ["read", "write", "burst"]
is_read_transaction = True
selected_type = transaction_types[0 if is_read_transaction else 1]  # "read"


# ============================================================================
# SECTION 4: COLLECTIONS - LISTS (Ordered, Mutable)
# ============================================================================
"""
List: Ordered collection, changeable, allows duplicates.
Used in testbenches for:
- Sequences of transactions
- Stimulus vectors
- Results collection
- Transaction queues
"""

# List creation and access
address_sequence = [0x1000, 0x1004, 0x1008, 0x100C]
print(address_sequence[0])          # 0x1000 (first element, index 0)
print(address_sequence[-1])         # 0x100C (last element)

# List modification (mutable)
write_data = [0xAA, 0xBB, 0xCC]
write_data.append(0xDD)             # Add to end: [0xAA, 0xBB, 0xCC, 0xDD]
write_data[1] = 0xFF                # Modify index 1: [0xAA, 0xFF, 0xCC, 0xDD]
write_data.pop()                    # Remove last: [0xAA, 0xFF, 0xCC]
write_data.insert(0, 0x11)          # Insert at index 0: [0x11, 0xAA, 0xFF, 0xCC]

# List iteration (fundamental in testbenches)
responses = [0x1, 0x2, 0x4, 0x8]
for i, response in enumerate(responses):
    print(f"Transaction {i}: response = 0x{response:X}")

# List slicing (powerful for sub-ranges)
all_addresses = list(range(0x1000, 0x1010, 4))      # [0x1000, 0x1004, 0x1008, 0x100C]
first_half = all_addresses[0:2]                     # First 2 elements
second_half = all_addresses[2:]                     # From index 2 onward


# ============================================================================
# SECTION 5: COLLECTIONS - TUPLES (Ordered, Immutable)
# ============================================================================
"""
Tuple: Ordered collection, unchangeable, allows duplicates.
Used for:
- Fixed transaction structure
- Return multiple values from functions
- Immutable transaction records
"""

# Tuple creation
transaction_fixed = (0x1000, 0xDEADBEEF, 0x1)  # (address, data, valid)
print(transaction_fixed[0])                    # 0x1000 (access by index)

# Tuple unpacking (clean assignment of multiple values)
address, data, valid = transaction_fixed
print(f"Address: 0x{address:X}, Data: 0x{data:X}, Valid: {valid}")

# Tuples are immutable (cannot modify)
# transaction_fixed[0] = 0x2000  # Would raise TypeError

# Single-element tuple (note the trailing comma)
single_element_tuple = (42,)
not_a_tuple = (42)  # This is just 42, not a tuple!


# ============================================================================
# SECTION 6: COLLECTIONS - DICTIONARIES (Key-Value Mapping)
# ============================================================================
"""
Dictionary: Unordered key-value pairs, mutable, keys must be hashable.
Essential for testbenches:
- Configuration storage (test_config["max_delay"])
- Transaction field access (tx["addr"], tx["data"])
- Named parameter passing
- Result collection and reporting
"""

# Dictionary creation
transaction = {
    "address": 0x1000,
    "data": 0xCAFEBABE,
    "write_enable": True,
    "burst_length": 16
}

# Accessing values by key
print(transaction["address"])       # 0x1000
print(transaction["write_enable"])  # True

# Modifying values
transaction["data"] = 0xDEADBEEF
transaction["status"] = "COMPLETED"  # Add new key-value pair

# Checking key existence
if "error" in transaction:
    print("Error field exists")
else:
    print("No error field yet")

# Iterating over dictionary
for key, value in transaction.items():
    print(f"{key}: {value}")

# Common testbench pattern: configuration dictionary
test_config = {
    "timeout_cycles": 1000,
    "clock_freq_mhz": 100,
    "max_transactions": 100,
    "verbose": True
}

# Safe access with .get() (returns None if key missing)
verbosity = test_config.get("verbose", False)  # True
debug_level = test_config.get("debug", 0)      # 0 (default)


# ============================================================================
# SECTION 7: BINARY TYPES (Register Access, Protocol Data)
# ============================================================================
"""
Bytes, bytearray, memoryview: Low-level binary data handling.
Critical for:
- Register read/write values
- Protocol packet construction
- Memory buffer simulation
"""

# Bytes: Immutable sequence of integers (0-255)
register_value_bytes = b'\xFF\x00\xAA'  # 3 bytes
print(register_value_bytes[0])          # 255 (first byte)
print(register_value_bytes.hex())       # 'ff00aa' (hex representation)

# Bytearray: Mutable equivalent of bytes
packet_data = bytearray([0x12, 0x34, 0x56, 0x78])
packet_data[1] = 0xFF               # Modify second byte
print(packet_data)                  # bytearray(b'\x12\xff\x56\x78')

# Memoryview: Efficient read/write without copying
buffer = bytearray([1, 2, 3, 4, 5])
view = memoryview(buffer)
print(view[2])                      # 3 (read at index 2)
view[2] = 99                        # Modify in-place
print(buffer)                       # bytearray(b'\x01\x02\x63\x04\x05')


# ============================================================================
# SECTION 8: NONE TYPE (Absence of Value)
# ============================================================================
"""
None: Represents absence of value (like null in other languages).
Common uses:
- Default parameter value
- Function return when no result
- Uninitialized variable
"""

# None as default value
response_data = None

if response_data is None:
    print("Response not yet received")

# Checking with 'is' operator (not '==')
status = None
if status is None:
    status = "INITIALIZED"  # Set initial value


# ============================================================================
# SECTION 9: PRACTICAL TESTBENCH EXAMPLE
# ============================================================================
"""
Demonstrate realistic variable usage combining all concepts.
"""

# Configuration (mixed types in dict)
testbench_config = {
    "name": "AXI Write Transaction Test",
    "max_transactions": 100,
    "verbose_logging": True,
    "timeout_ns": 10000.0,
    "valid_addresses": [0x0000, 0x1000, 0x2000]
}

# Transaction structure (mixed types in dict)
transactions = [
    {"addr": 0x0000, "data": 0xDEADBEEF, "status": None},
    {"addr": 0x1000, "data": 0xCAFEBABE, "status": None},
    {"addr": 0x2000, "data": 0x12345678, "status": None},
]

# Process transactions
passed_count = 0
failed_count = 0

for i, tx in enumerate(transactions):
    # Validate address
    is_valid_addr = tx["addr"] in testbench_config["valid_addresses"]
    
    if is_valid_addr and testbench_config["verbose_logging"]:
        log_msg = f"TX[{i}]: addr=0x{tx['addr']:04X} data=0x{tx['data']:08X}"
        print(log_msg)
        tx["status"] = "PASSED"
        passed_count += 1
    else:
        tx["status"] = "FAILED"
        failed_count += 1

# Final report
print(f"\nResults: {passed_count} passed, {failed_count} failed")
 