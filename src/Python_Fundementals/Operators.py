"""
Python Operators for Hardware Verification

Covers: Arithmetic, Comparison, Logical, Bitwise, and Assignment operators
used in testbench stimulus generation and result verification.
"""

import logging
from pathlib import Path

# Logger setup (following Logging section best practices)
def setup_operators_logger(log_file="operators_demo.log"):
    """Configure logger for operators demonstration."""
    logger = logging.getLogger("OperatorsDemo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # Console handler: INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))
    
    # File handler: Everything DEBUG and above
    log_path = Path(__file__).parent / log_file
    file_handler = logging.FileHandler(str(log_path), mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-8s | %(message)s'))
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


# ============================================================================
# SECTION 1: Arithmetic Operators
# ============================================================================
# WHY: Arithmetic operators are fundamental for stimulus generation:
#      - Address calculation (base + offset, stride-based access patterns)
#      - Cycle counting and timing calculations
#      - Data transformations (scaling, alignment)
def demo_arithmetic():
    logger = setup_operators_logger()
    logger.info("=== ARITHMETIC OPERATORS ===")
    
    a = 2
    b = 5
    
    # Basic operations: addition, subtraction, multiplication
    # These map directly to hardware calculations in testbenches
    logger.info("Addition: %d + %d = %d", b, a, b + a)
    logger.info("Subtraction: %d - %d = %d", b, a, b - a)
    logger.info("Multiplication: %d * %d = %d", b, a, b * a)
    
    # Division types (CRITICAL DISTINCTION FOR VERIFICATION):
    # - True division (/) always returns float: Use for timing calculations
    # - Floor division (//) returns integer: Use for address/count calculations
    # - Modulo (%) returns remainder: Use for wraparound and alignment checks
    logger.info("True division: %d / %d = %.2f", b, a, b / a)       # 2.5
    logger.info("Floor division: %d // %d = %d", b, a, b // a)     # 2 (discards remainder)
    logger.info("Modulo (remainder): %d %% %d = %d", b, a, b % a)  # 1 (wrapped value)
    logger.info("Exponent: %d ** %d = %d", b, a, b ** a)            # 25 (power)
    
    # PRACTICAL: Register address calculation
    # Transaction i accesses address: base + (i * stride)
    reg_addr = 0x1000  # Base address
    offset = 0x004     # Fixed offset (e.g., register width in bytes)
    logger.info("Register address calculation: 0x%X + 0x%X = 0x%X", 
                reg_addr, offset, reg_addr + offset)


# ============================================================================
# SECTION 2: Comparison Operators
# ============================================================================
# WHY: Every testbench assertion relies on comparisons:
#      - Verify data matches expected value (== or !=)
#      - Check if address is within valid range (< > <= >=)
#      - Validate protocol timing (cycle_count < timeout_cycles)
def demo_comparison():
    logger = setup_operators_logger()
    logger.info("=== COMPARISON OPERATORS ===")
    
    addr_a = 0x1000
    addr_b = 0x2000
    data = 0xDEADBEEF
    expected = 0xDEADBEEF
    
    # All comparison operators return boolean (True/False)
    # Used in if statements, assertions, and loop conditions
    logger.info("Equal (==): 0x%X == 0x%X → %s", data, expected, data == expected)
    logger.info("Not equal (!=): 0x%X != 0x%X → %s", addr_a, addr_b, addr_a != addr_b)
    logger.info("Greater than (>): %d > %d → %s", addr_b, addr_a, addr_b > addr_a)
    logger.info("Less than (<): %d < %d → %s", addr_a, addr_b, addr_a < addr_b)
    logger.info("Greater or equal (>=): %d >= %d → %s", addr_a, addr_a, addr_a >= addr_a)
    logger.info("Less or equal (<=): %d <= %d → %s", addr_b, addr_a + 1000, 
                addr_b <= addr_a + 1000)
    
    # PYTHON-SPECIFIC: Chained comparisons are more readable than C
    # Instead of: (cycle > 10) and (cycle < 100)
    # Write:      10 < cycle < 100
    cycle = 42
    logger.info("Chained comparison: 10 < %d < 100 → %s", cycle, 10 < cycle < 100)


# ============================================================================
# SECTION 3: Logical Operators (Control Flow)
# ============================================================================
# WHY: Logical operators (and/or/not) control testbench sequencing:
#      - and: All conditions must be true (AND multiple checks)
#      - or: At least one condition must be true (OR as fallback)
#      - not: Negate a boolean (invert logic)
# IMPORTANT: Python uses short-circuit evaluation (stops early if result known)
def demo_logical():
    logger = setup_operators_logger()
    logger.info("=== LOGICAL OPERATORS ===")
    
    test_passed = True
    dut_ready = True
    timeout = False
    
    # AND: Both conditions MUST be True
    # Common usage: Check that DUT is ready AND test conditions are met
    logger.info("AND (both true): test_passed=%s and dut_ready=%s → %s",
                test_passed, dut_ready, test_passed and dut_ready)
    
    # OR: At least ONE condition is True
    # Common usage: Transaction succeeded OR we're in recovery mode
    logger.info("OR (at least one): test_passed=%s or timeout=%s → %s",
                test_passed, timeout, test_passed or timeout)
    
    # NOT: Negate the boolean
    # Common usage: If we didn't timeout, continue
    logger.info("NOT (negate): not timeout → %s", not timeout)
    
    # COMPLEX CONDITIONS: Chain multiple operators
    # Useful for: "If (test passed AND device ready) OR recovery mode enabled"
    condition = (test_passed and dut_ready) or (not timeout)
    logger.info("Complex condition result: %s", condition)


# ============================================================================
# SECTION 4: Bitwise Operators (Low-Level Protocol Handling)
# ============================================================================
# WHY: Bitwise operations are fundamental to register manipulation and protocol encoding:
#      - Extract specific bit fields from register data
#      - Pack multiple fields into a single control word
#      - Check/set/clear individual bits
# CONCEPT: Treat numbers as binary sequences (strings of 0s and 1s)
def demo_bitwise():
    logger = setup_operators_logger()
    logger.info("=== BITWISE OPERATORS ===")
    
    mask_a = 0b1100  # 12 in decimal: bits [3,2] are set
    mask_b = 0b0101  # 5 in decimal: bits [2,0] are set
    
    # AND (&): Result has 1 only where BOTH operands have 1
    # Use case: Extract specific bits (e.g., status = control_word & 0x3)
    logger.info("AND (&): 0b%s & 0b%s = 0b%s", 
                format(mask_a, '04b'), format(mask_b, '04b'), 
                format(mask_a & mask_b, '04b'))
    
    # OR (|): Result has 1 where EITHER operand has 1
    # Use case: Combine multiple fields into one word
    logger.info("OR (|): 0b%s | 0b%s = 0b%s",
                format(mask_a, '04b'), format(mask_b, '04b'),
                format(mask_a | mask_b, '04b'))
    
    # XOR (^): Result has 1 where bits DIFFER
    # Use case: Toggle specific bits or compare data
    logger.info("XOR (^): 0b%s ^ 0b%s = 0b%s",
                format(mask_a, '04b'), format(mask_b, '04b'),
                format(mask_a ^ mask_b, '04b'))
    
    # NOT (~): Flip all bits (1→0, 0→1)
    # CAUTION: Python integers have infinite precision; mask the result
    logger.info("NOT (~): ~0b%s = 0x%X (masked to 16-bit)", 
                format(mask_a, '04b'), ~mask_a & 0xFFFF)
    
    # RIGHT SHIFT (>>): Divide by 2^n and discard remainder
    # Use case: Extract high-order bits (e.g., extract priority field from word)
    data = 0b11110000  # 240 in decimal
    logger.info("Right shift (>>): 0b%s >> 2 = 0b%s (result: %d)",
                format(data, '08b'), format(data >> 2, '08b'), data >> 2)
    
    # LEFT SHIFT (<<): Multiply by 2^n
    # Use case: Pack fields into specific bit positions before ORing together
    logger.info("Left shift (<<): 0b%s << 2 = 0b%s (result: %d)",
                format(0b00001111, '08b'), format(0b00001111 << 2, '08b'), 0b00001111 << 2)


# ============================================================================
# SECTION 5: Assignment Operators
# ============================================================================
# WHY: Assignment operators combine an operation with assignment (convenience + readability)
#      They're useful for counters, accumulators, and register state modifications
# SYNTAX: x += 5 is shorthand for x = x + 5 (same result, fewer characters)
def demo_assignment():
    logger = setup_operators_logger()
    logger.info("=== ASSIGNMENT OPERATORS ===")
    
    counter = 0
    logger.info("Initial counter: %d", counter)
    
    # Arithmetic assignment operators
    counter += 5  # Increment counter (counter = counter + 5)
    logger.info("After += 5: %d", counter)
    
    counter -= 2  # Decrement counter
    logger.info("After -= 2: %d", counter)
    
    counter *= 3  # Multiply counter
    logger.info("After *= 3: %d", counter)
    
    counter //= 2  # Divide counter (floor division)
    logger.info("After //= 2: %d", counter)
    
    # BITWISE ASSIGNMENT: Directly manipulate register bits
    # Use case: Set/clear/toggle individual bits in a control register
    flags = 0b0000  # Start with all bits clear
    
    flags |= 0b0001  # Set bit 0 (set specific bits)
    logger.info("After |= 0b0001 (set bit 0): 0b%s", format(flags, '04b'))
    
    flags &= 0b1110  # Clear bit 0 (AND with inverted mask)
    logger.info("After &= 0b1110 (clear bit 0): 0b%s", format(flags, '04b'))


# ============================================================================
# SECTION 6: Complete Testbench Example
# ============================================================================
# SCENARIO: Generate an AXI transaction, pack control fields, verify results
# DEMONSTRATES: All operator types working together in realistic testbench code
def demo_testbench_example():
    logger = setup_operators_logger()
    logger.info("=== COMPLETE TESTBENCH TRANSACTION ===")
    
    # STEP 1: STIMULUS GENERATION (Arithmetic operators)
    # Calculate the address for transaction N based on stride pattern
    base_addr = 0x1000     # Base address of testbench region
    tx_id = 5              # Transaction number (0-indexed)
    burst_size = 4         # Transactions per burst
    # Address = Base + (Transaction_ID * Burst_Size * Word_Size)
    addr = base_addr + (tx_id * burst_size * 4)
    
    logger.info("Generated address: base=0x%X, tx_id=%d, burst=%d → addr=0x%X",
                base_addr, tx_id, burst_size, addr)
    
    # STEP 2: CONTROL WORD ASSEMBLY (Bitwise operators)
    # Pack multiple fields into a single 8-bit control word
    # Bit layout: [7:6]=priority, [5:3]=burst_type, [2:0]=control_bits
    priority = 0b00        # [7:6] = 00 (low priority)
    burst_type = 0b001     # [5:3] = 001 (INCR burst)
    control_bits = 0b11    # [2:0] = 11 (write enable + valid)
    
    # Shift and combine fields using bitwise OR
    control_word = (priority << 5) | (burst_type << 2) | control_bits
    logger.info("Control word assembly: 0x%02X = [priority:%d, burst:%d, control:%d]",
                control_word, priority, burst_type, control_bits)
    
    # STEP 3: DATA VERIFICATION (Comparison operators)
    # Compare DUT's response against expected value
    expected_data = 0xCAFEBABE
    received_data = 0xCAFEBABE
    match = (expected_data == received_data)  # True if equal
    logger.info("Data verification: expected=0x%X, received=0x%X, match=%s",
                expected_data, received_data, match)
    
    # STEP 4: TEST RESULT DETERMINATION (Logical operators)
    # Combine multiple pass/fail criteria using AND/OR
    timeout_cycles = 50
    max_cycles = 100
    no_timeout = (timeout_cycles < max_cycles)  # True if no timeout
    
    # Test PASSES if: data matches AND no timeout occurred AND burst_size > 0
    test_result = match and no_timeout and (burst_size > 0)
    
    logger.info("Test result: %s", "PASSED" if test_result else "FAILED")


if __name__ == "__main__":
    demo_arithmetic()
    demo_comparison()
    demo_logical()
    demo_bitwise()
    demo_assignment()
    demo_testbench_example()