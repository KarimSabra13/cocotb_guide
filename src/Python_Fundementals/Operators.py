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
def demo_arithmetic():
    logger = setup_operators_logger()
    logger.info("=== ARITHMETIC OPERATORS ===")
    
    a = 2
    b = 5
    
    # Basic operations
    logger.info("Addition: %d + %d = %d", b, a, b + a)
    logger.info("Subtraction: %d - %d = %d", b, a, b - a)
    logger.info("Multiplication: %d * %d = %d", b, a, b * a)
    
    # Division types (critical for testbench calculations)
    logger.info("True division: %d / %d = %.2f", b, a, b / a)       # 2.5
    logger.info("Floor division: %d // %d = %d", b, a, b // a)     # 2
    logger.info("Modulo (remainder): %d %% %d = %d", b, a, b % a)  # 1
    logger.info("Exponent: %d ** %d = %d", b, a, b ** a)            # 25
    
    # Register calculations
    reg_addr = 0x1000
    offset = 0x004
    logger.info("Register address calculation: 0x%X + 0x%X = 0x%X", 
                reg_addr, offset, reg_addr + offset)


# ============================================================================
# SECTION 2: Comparison Operators
# ============================================================================
def demo_comparison():
    logger = setup_operators_logger()
    logger.info("=== COMPARISON OPERATORS ===")
    
    addr_a = 0x1000
    addr_b = 0x2000
    data = 0xDEADBEEF
    expected = 0xDEADBEEF
    
    logger.info("Equal (==): 0x%X == 0x%X → %s", data, expected, data == expected)
    logger.info("Not equal (!=): 0x%X != 0x%X → %s", addr_a, addr_b, addr_a != addr_b)
    logger.info("Greater than (>): %d > %d → %s", addr_b, addr_a, addr_b > addr_a)
    logger.info("Less than (<): %d < %d → %s", addr_a, addr_b, addr_a < addr_b)
    logger.info("Greater or equal (>=): %d >= %d → %s", addr_a, addr_a, addr_a >= addr_a)
    logger.info("Less or equal (<=): %d <= %d → %s", addr_b, addr_a + 1000, 
                addr_b <= addr_a + 1000)
    
    # Chained comparisons (unique to Python)
    cycle = 42
    logger.info("Chained comparison: 10 < %d < 100 → %s", cycle, 10 < cycle < 100)


# ============================================================================
# SECTION 3: Logical Operators (Control Flow)
# ============================================================================
def demo_logical():
    logger = setup_operators_logger()
    logger.info("=== LOGICAL OPERATORS ===")
    
    test_passed = True
    dut_ready = True
    timeout = False
    
    logger.info("AND (both true): test_passed=%s and dut_ready=%s → %s",
                test_passed, dut_ready, test_passed and dut_ready)
    logger.info("OR (at least one): test_passed=%s or timeout=%s → %s",
                test_passed, timeout, test_passed or timeout)
    logger.info("NOT (negate): not timeout → %s", not timeout)
    
    # Practical testbench condition
    condition = (test_passed and dut_ready) or (not timeout)
    logger.info("Complex condition result: %s", condition)


# ============================================================================
# SECTION 4: Bitwise Operators (Low-Level Protocol Handling)
# ============================================================================
def demo_bitwise():
    logger = setup_operators_logger()
    logger.info("=== BITWISE OPERATORS ===")
    
    mask_a = 0b1100  # 12
    mask_b = 0b0101  # 5
    
    # Bitwise AND, OR, XOR
    logger.info("AND (&): 0b%s & 0b%s = 0b%s", 
                format(mask_a, '04b'), format(mask_b, '04b'), 
                format(mask_a & mask_b, '04b'))
    
    logger.info("OR (|): 0b%s | 0b%s = 0b%s",
                format(mask_a, '04b'), format(mask_b, '04b'),
                format(mask_a | mask_b, '04b'))
    
    logger.info("XOR (^): 0b%s ^ 0b%s = 0b%s",
                format(mask_a, '04b'), format(mask_b, '04b'),
                format(mask_a ^ mask_b, '04b'))
    
    logger.info("NOT (~): ~0b%s = 0x%X", format(mask_a, '04b'), ~mask_a & 0xFFFF)
    
    # Shifts (critical for register field extraction)
    data = 0b11110000
    logger.info("Right shift (>>): 0b%s >> 2 = 0b%s",
                format(data, '08b'), format(data >> 2, '08b'))
    
    logger.info("Left shift (<<): 0b%s << 2 = 0b%s",
                format(0b00001111, '08b'), format(0b00001111 << 2, '08b'))


# ============================================================================
# SECTION 5: Assignment Operators
# ============================================================================
def demo_assignment():
    logger = setup_operators_logger()
    logger.info("=== ASSIGNMENT OPERATORS ===")
    
    counter = 0
    logger.info("Initial counter: %d", counter)
    
    counter += 5  # Shorthand for counter = counter + 5
    logger.info("After += 5: %d", counter)
    
    counter -= 2
    logger.info("After -= 2: %d", counter)
    
    counter *= 3
    logger.info("After *= 3: %d", counter)
    
    counter //= 2
    logger.info("After //= 2: %d", counter)
    
    # Bit operations via assignment
    flags = 0b0000
    flags |= 0b0001  # Set bit 0
    logger.info("After |= 0b0001: 0b%s", format(flags, '04b'))
    
    flags &= 0b1110  # Clear bit 0
    logger.info("After &= 0b1110: 0b%s", format(flags, '04b'))


# ============================================================================
# SECTION 6: Complete Testbench Example
# ============================================================================
def demo_testbench_example():
    logger = setup_operators_logger()
    logger.info("=== COMPLETE TESTBENCH TRANSACTION ===")
    
    # Stimulus generation
    base_addr = 0x1000
    tx_id = 5
    burst_size = 4
    addr = base_addr + (tx_id * burst_size * 4)  # Calculate transaction address
    
    logger.info("Generated address: base=0x%X, tx_id=%d, burst=%d → addr=0x%X",
                base_addr, tx_id, burst_size, addr)
    
    # Data packing with bitwise ops
    control_bits = 0b11  # [1:0] = control
    burst_type = 0b001   # [4:2] = burst
    priority = 0b00      # [6:5] = priority
    
    control_word = (priority << 5) | (burst_type << 2) | control_bits
    logger.info("Control word assembly: 0x%02X = [priority:%d, burst:%d, control:%d]",
                control_word, priority, burst_type, control_bits)
    
    # Result verification
    expected_data = 0xCAFEBABE
    received_data = 0xCAFEBABE
    match = (expected_data == received_data)
    logger.info("Data verification: expected=0x%X, received=0x%X, match=%s",
                expected_data, received_data, match)
    
    # Pass/Fail determination
    timeout_cycles = 50
    max_cycles = 100
    no_timeout = (timeout_cycles < max_cycles)
    test_result = match and no_timeout and True  # All conditions met
    
    logger.info("Test result: %s", "PASSED" if test_result else "FAILED")


if __name__ == "__main__":
    demo_arithmetic()
    demo_comparison()
    demo_logical()
    demo_bitwise()
    demo_assignment()
    demo_testbench_example()