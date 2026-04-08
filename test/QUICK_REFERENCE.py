"""
QUICK REFERENCE - Common Patterns Used in Verification

This file contains code snippets from Sections 1-3 that you might need.
Feel free to reference while doing the exercise.
"""

# ============================================================================
# PYTHON PATTERN 1: Dynamic Typing & Type Inference
# ============================================================================

# Python figures out the type based on the value
transaction_id = 5              # int
address = 0x1000                # also int (hex literal)
data = 0xDEADBEEF              # int
name = "AXI_WRITE"             # str
is_valid = True                 # bool
response_time = 2.5             # float

# You can change the type by reassigning
my_var = 42                     # int
my_var = "now it's a string"    # str (no problem in Python!)
my_var = [1, 2, 3]             # list


# ============================================================================
# PYTHON PATTERN 2: Dictionary for Transaction Storage
# ============================================================================

# Single transaction as dictionary
transaction = {
    "tx_id": 0,
    "addr": 0x1000,
    "data": 0xDEADBEEF,
    "burst_type": "INCR",
    "control_flags": 0x8
}

# Access fields
print(transaction["addr"])              # 0x1000
print(transaction.get("addr"))          # 0x1000 (safer - won't crash if missing)
print(transaction.get("missing", 0))    # 0 (default if not found)

# Modify fields
transaction["data"] = 0xCAFEBABE
transaction["status"] = "PASSED"        # Add new field

# Copy dictionary (important for response checking!)
response = transaction.copy()           # Shallow copy - good enough for simple dicts
response["data"] = 0x99999999           # Won't affect original


# ============================================================================
# PYTHON PATTERN 3: Lists and Iteration
# ============================================================================

# Create list of dictionaries (perfect for transactions!)
transactions = []

for i in range(5):
    tx = {
        "id": i,
        "addr": 0x1000 + (i * 0x10)  # Increment by stride
    }
    transactions.append(tx)

# Iterate with index
for i, tx in enumerate(transactions):
    print(f"Transaction {i}: addr=0x{tx['addr']:04X}")

# List comprehension (concise alternative)
data_pool = [0xDEADBEEF, 0xCAFEBABE, 0x12345678]
cycled_values = [data_pool[i % len(data_pool)] for i in range(10)]


# ============================================================================
# ARITHMETIC OPERATORS - Common Calculations
# ============================================================================

# Address calculation with stride
BASE_ADDR = 0x1000
STRIDE = 0x10                           # 16 bytes
tx_id = 3

calculated_addr = BASE_ADDR + (tx_id * STRIDE)  # 0x1030

# Modulo for cycling through patterns
burst_type_code = 1 if (tx_id % 2) == 0 else 0  # Alternate 1,0,1,0,...

# Division for calculations
bytes_needed = 128
word_size = 4
num_words = bytes_needed // word_size   # Floor division -> 32

# Remainder check
if tx_id % 2 == 0:
    print("Even index")
else:
    print("Odd index")


# ============================================================================
# COMPARISON OPERATORS - Verification Checks
# ============================================================================

expected = 0xDEADBEEF
received = 0xDEADBEEF

# Basic checks
if expected == received:
    print("Data matches!")

if expected != received:
    print("Data mismatch!")

# Range checking
addr = 0x1234
if 0x1000 <= addr <= 0x2000:
    print("Address in valid range")

# Multiple conditions with logical operators
test_passed = True
dut_ready = True
timeout = False

if test_passed and dut_ready:
    print("Ready to continue")

if (not timeout) and (test_passed or recovery_mode):
    print("Proceed")


# ============================================================================
# BITWISE OPERATORS - Register Encoding (THE TRICKY PART!)
# ============================================================================

# Bit layout specification:
# [15:14] = priority (2 bits)
# [13:12] = burst_type (2 bits)
# [11:8]  = tx_id (4 bits)
# [7:4]   = write_strobe (4 bits)
# [3:0]   = control_flags (4 bits)

# Extract single values
priority = 1        # 0-3
burst_type = 0      # 0-3
tx_id = 5           # 0-15
strobe = 0xF        # 0-15
flags = 0x8         # 0-15

# STEP 1: Shift each field to its position
field1 = priority << 14         # Shift left by 14 positions
field2 = burst_type << 12       # Shift left by 12 positions
field3 = tx_id << 8             # Shift left by 8 positions
field4 = strobe << 4            # Shift left by 4 positions
field5 = flags << 0             # No shift needed (already at position 0)

# STEP 2: Combine all fields with bitwise OR
control_word = field1 | field2 | field3 | field4 | field5

# SHORTHAND: Do it in one line
control_word = (priority << 14) | (burst_type << 12) | (tx_id << 8) | \
               (strobe << 4) | flags

# EXTRACT FIELDS from a control_word (reverse operation)
extracted_priority = (control_word >> 14) & 0x3      # Shift right and mask
extracted_strobe = (control_word >> 4) & 0xF
extracted_flags = control_word & 0xF                 # Already at position 0


# ============================================================================
# LOGGING - From Section 1
# ============================================================================

import logging
from pathlib import Path

def setup_logger(logger_name, log_file):
    """Setup multi-handler logger (console + file)."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # Console: INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))
    
    # File: DEBUG and above
    log_path = Path(__file__).parent / log_file
    file_handler = logging.FileHandler(str(log_path), mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)-8s | %(message)s')
    )
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger

# Usage
logger = setup_logger("MyTest", "test.log")

logger.debug("Detailed info: addr=0x%X, data=0x%X", 0x1000, 0xDEADBEEF)
logger.info("Test started")
logger.warning("Timeout approaching!")
logger.error("Data mismatch: expected=0x%X, received=0x%X", 
            0xDEADBEEF, 0x99999999)


# ============================================================================
# TIPS & TRICKS FROM PROS
# ============================================================================

# TIP 1: Use f-strings for display, printf-style for logging
data = 0xCAFEBABE
print(f"Display: 0x{data:08X}")                     # For stdout
logger.info("Log: data=0x%08X", data)              # For logging (printf-style)

# TIP 2: Dictionary comprehension for packing multiple transactions
transactions = [
    {"id": i, "addr": 0x1000 + (i * 0x10)}
    for i in range(5)
]

# TIP 3: Use 'in' to check if key exists
if "addr" in transaction:
    print(transaction["addr"])

# TIP 4: Get with default to avoid KeyError
value = transaction.get("status", "UNKNOWN")

# TIP 5: Hex formatting hints
x = 255
print(f"0x{x:02X}")    # 0xFF   (2-digit hex)
print(f"0x{x:04X}")    # 0x00FF (4-digit hex)
print(f"0b{x:08b}")    # 0b11111111 (binary)

# TIP 6: Copy vs reference
original = [1, 2, 3]
copy1 = original.copy()      # Copy the list
copy1.append(4)              # Doesn't affect original

reference = original         # Just a reference
reference.append(5)          # DOES affect original!
