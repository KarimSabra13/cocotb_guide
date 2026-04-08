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

All output uses logging (from Logging section) instead of print().
================================================================================
"""

import logging
from pathlib import Path

# Setup logging with both console and file handlers (from Logging section lessons)
def setup_variables_logger(log_file="variables_demo.log"):
    """Configure logger with console and file output."""
    logger = logging.getLogger("VariablesDemo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # Console handler: show INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))
    
    # File handler: log everything (DEBUG+)
    log_path = Path(__file__).parent / log_file
    file_handler = logging.FileHandler(str(log_path), mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(message)s'
    ))
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger

# Initialize logger
logger = setup_variables_logger()
logger.info("Variables and Data Types Demo Started")

# ============================================================================
# SECTION 1: NUMERIC TYPES AND DYNAMIC TYPING
# ============================================================================
"""
Python infers variable types from assigned values. No explicit declarations
are needed. This contrasts with SystemVerilog (e.g., 'int x = 5;').

Benefit: Write code faster; check types at runtime when needed.
Risk: Implicit type conversions can hide bugs; use type() to verify.
"""

logger.debug("SECTION 1: Numeric Types and Dynamic Typing")

# Integer: Unlimited precision (no overflow unlike SystemVerilog logic[31:0])
transaction_id = 42
register_address = 0xDEADBEEF
# Python handles arbitrarily large integers automatically
large_value = 123456789123456789123456789

# Float: IEEE 754 64-bit double precision
clock_frequency = 100.5  # MHz
duty_cycle = 0.5         # 50% duty cycle
delay = 1.23e-9          # 1.23 nanoseconds (scientific notation)

# Type checking (useful in testbenches to catch errors early)
logger.info("transaction_id type: %s", type(transaction_id))
logger.info("clock_frequency type: %s", type(clock_frequency))
logger.debug("large_value: %d (unlimited precision)", large_value)

# Type conversion (coercion)
int_from_float = int(clock_frequency)        # 100 (truncates)
float_from_int = float(transaction_id)       # 42.0
string_number = str(register_address)        # '0xDEADBEEF'

logger.debug("Conversions: int(%.1f) = %d, float(%d) = %.1f", 
             clock_frequency, int_from_float, transaction_id, float_from_int)


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

logger.debug("SECTION 2: String Handling")

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

logger.debug("Test name: %s", test_name_single)
logger.debug("Test description:%s%s", "\n", test_description)

# String concatenation methods
addr = 0x1000
data = 0xCAFEBABE

# Method 2: f-strings (recommended, efficient, readable)
log_msg_2 = f"addr = 0x{addr:08X}, data = 0x{data:08X}"
logger.info(log_msg_2)

# Method 3: String formatting with .format()
log_msg_3 = "addr = 0x{:08X}, data = 0x{:08X}".format(addr, data)
logger.debug("Formatted string: %s", log_msg_3)

# String methods (useful for parsing and text manipulation)
test_result = "PASS: All Assertions Cleared"
is_pass = test_result.startswith("PASS")    # True
is_fail = test_result.startswith("FAIL")    # False
uppercase = test_result.upper()             # "PASS: ALL ASSERTIONS CLEARED"
lowercase = test_result.lower()

logger.debug("Test result: %s (is_pass=%s)", test_result, is_pass)
logger.debug("String transforms: upper='%s', lower='%s'", uppercase, lowercase)


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

logger.debug("SECTION 3: Boolean Type")

# Boolean literals
test_passed = True
simulation_complete = False

# Boolean results from comparisons
response_valid = True
timeout_occurred = False
data_matches = (0xCAFEBABE == 0xCAFEBABE)    # True

logger.debug("Boolean values: test_passed=%s, simulation_complete=%s", 
             test_passed, simulation_complete)

# Boolean operators (all return bool)
both_true = test_passed and simulation_complete    # False
either_true = test_passed or simulation_complete   # True
not_passed = not test_passed                       # False

logger.debug("Boolean operators: both_true=%s, either_true=%s, not_passed=%s", 
             both_true, either_true, not_passed)

# Practical testbench condition
cycle_count = 150
max_cycles = 100
timeout = cycle_count > max_cycles  # True

if timeout:
    logger.warning("Timeout! Transaction did not complete (cycles %d > max %d)", 
                   cycle_count, max_cycles)
else:
    logger.info("Transaction completed within max cycles")

# Boolean as index/mask (common in verification)
transaction_types = ["read", "write", "burst"]
is_read_transaction = True
selected_type = transaction_types[0 if is_read_transaction else 1]  # "read"
logger.debug("Selected transaction type: %s", selected_type)


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

logger.debug("SECTION 4: Lists (Ordered, Mutable)")

# List creation and access
address_sequence = [0x1000, 0x1004, 0x1008, 0x100C]
logger.info("Address sequence: %s", [f"0x{a:04X}" for a in address_sequence])
logger.debug("First address: 0x%04X, last address: 0x%04X", 
             address_sequence[0], address_sequence[-1])

# List modification (mutable)
write_data = [0xAA, 0xBB, 0xCC]
write_data.append(0xDD)             # Add to end: [0xAA, 0xBB, 0xCC, 0xDD]
logger.debug("After append: %s", [f"0x{d:02X}" for d in write_data])

write_data[1] = 0xFF                # Modify index 1: [0xAA, 0xFF, 0xCC, 0xDD]
logger.debug("After modification: %s", [f"0x{d:02X}" for d in write_data])

write_data.pop()                    # Remove last: [0xAA, 0xFF, 0xCC]
write_data.insert(0, 0x11)          # Insert at index 0: [0x11, 0xAA, 0xFF, 0xCC]
logger.debug("After pop and insert: %s", [f"0x{d:02X}" for d in write_data])

# List iteration (fundamental in testbenches)
responses = [0x1, 0x2, 0x4, 0x8]
for i, response in enumerate(responses):
    logger.debug("Transaction %d: response = 0x%X", i, response)

# List slicing (powerful for sub-ranges)
all_addresses = list(range(0x1000, 0x1010, 4))      # [0x1000, 0x1004, 0x1008, 0x100C]
first_half = all_addresses[0:2]                     # First 2 elements
second_half = all_addresses[2:]                     # From index 2 onward
logger.debug("List slicing: first_half=%s, second_half=%s", 
             [f"0x{a:X}" for a in first_half], [f"0x{a:X}" for a in second_half])


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

logger.debug("SECTION 5: Tuples (Ordered, Immutable)")

# Tuple creation
transaction_fixed = (0x1000, 0xDEADBEEF, 0x1)  # (address, data, valid)
logger.info("Transaction tuple: (addr=0x%X, data=0x%X, valid=%d)", 
            transaction_fixed[0], transaction_fixed[1], transaction_fixed[2])

# Tuple unpacking (clean assignment of multiple values)
address, data, valid = transaction_fixed
logger.debug("Unpacked: address=0x%X, data=0x%X, valid=%d", 
             address, data, valid)

# Tuples are immutable (cannot modify)
# transaction_fixed[0] = 0x2000  # Would raise TypeError
logger.debug("Tuples are immutable by design")

# Single-element tuple (note the trailing comma)
single_element_tuple = (42,)
not_a_tuple = (42)  # This is just 42, not a tuple!
logger.debug("Single element tuple type: %s", type(single_element_tuple))
logger.debug("Without comma (just 42) type: %s", type(not_a_tuple))


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

logger.debug("SECTION 6: Dictionaries (Key-Value Mapping)")

# Dictionary creation
transaction = {
    "address": 0x1000,
    "data": 0xCAFEBABE,
    "write_enable": True,
    "burst_length": 16
}

# Accessing values by key
logger.info("Transaction: addr=0x%X, data=0x%X, write_en=%s", 
            transaction["address"], transaction["data"], transaction["write_enable"])

# Modifying values
transaction["data"] = 0xDEADBEEF
transaction["status"] = "COMPLETED"  # Add new key-value pair
logger.debug("After update: data=0x%X, status=%s", 
             transaction["data"], transaction.get("status"))

# Checking key existence
if "error" in transaction:
    logger.warning("Error field exists: %s", transaction["error"])
else:
    logger.debug("No error field in transaction")

# Iterating over dictionary
logger.debug("Iterating over transaction fields:")
for key, value in transaction.items():
    logger.debug("  %s: %s", key, value)

# Common testbench pattern: configuration dictionary
test_config = {
    "timeout_cycles": 1000,
    "clock_freq_mhz": 100,
    "max_transactions": 100,
    "verbose": True
}

logger.info("Test configuration loaded: timeout=%d cycles, freq=%d MHz", 
            test_config["timeout_cycles"], test_config["clock_freq_mhz"])

# Safe access with .get() (returns None if key missing)
verbosity = test_config.get("verbose", False)  # True
debug_level = test_config.get("debug", 0)      # 0 (default)
logger.debug("Logger verbosity: %s, debug level: %d", verbosity, debug_level)


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

logger.debug("SECTION 7: Binary Types")

# Bytes: Immutable sequence of integers (0-255)
register_value_bytes = b'\xFF\x00\xAA'  # 3 bytes
logger.info("Register bytes: first_byte=0x%02X, hex=%s", 
            register_value_bytes[0], register_value_bytes.hex())

# Bytearray: Mutable equivalent of bytes
packet_data = bytearray([0x12, 0x34, 0x56, 0x78])
logger.debug("Packet before modification: %s", packet_data.hex())

packet_data[1] = 0xFF               # Modify second byte
logger.debug("Packet after modifying index 1: %s", packet_data.hex())

# Memoryview: Efficient read/write without copying
buffer = bytearray([1, 2, 3, 4, 5])
view = memoryview(buffer)
logger.debug("Memoryview value at index 2: %d", view[2])

view[2] = 99                        # Modify in-place
logger.debug("After modifying via memoryview: %s", list(buffer))


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

logger.debug("SECTION 8: None Type")

# None as default value
response_data = None

if response_data is None:
    logger.info("Response not yet received (None)")
    response_data = 0xCAFEBABE

logger.debug("Response received: 0x%X", response_data)

# Checking with 'is' operator (not '==')
status = None
if status is None:
    status = "INITIALIZED"  # Set initial value
    logger.info("Status initialized to: %s", status)


# ============================================================================
# SECTION 9: PRACTICAL TESTBENCH EXAMPLE
# ============================================================================
"""
Demonstrate realistic variable usage combining all concepts.
"""

logger.info("SECTION 9: Practical Testbench Example")

# Configuration (mixed types in dict)
testbench_config = {
    "name": "AXI Write Transaction Test",
    "max_transactions": 100,
    "verbose_logging": True,
    "timeout_ns": 10000.0,
    "valid_addresses": [0x0000, 0x1000, 0x2000]
}

logger.info("Starting testbench: %s", testbench_config["name"])
logger.debug("Max transactions: %d", testbench_config["max_transactions"])

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
        logger.info(log_msg)
        tx["status"] = "PASSED"
        passed_count += 1
    else:
        logger.warning("TX[%d]: Invalid address 0x%04X", i, tx["addr"])
        tx["status"] = "FAILED"
        failed_count += 1

# Final report
logger.info("="*60)
logger.info("Results: %d passed, %d failed", passed_count, failed_count)
logger.info("Success Rate: %.1f%%", 100.0 * passed_count / len(transactions))
logger.info("="*60)

logger.info("Variables and Data Types Demo Completed")
