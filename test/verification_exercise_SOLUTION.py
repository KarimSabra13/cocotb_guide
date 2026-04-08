"""
REFERENCE SOLUTION - DV Junior Verification Exercise
(Don't look until you submit your attempt!)

This solution demonstrates:
- Professional logging integration
- Efficient use of data structures
- Bitwise operations for hardware encoding
- Comprehensive error reporting
- Interview-level Python practices for verification
"""

import logging
from pathlib import Path


# ============================================================================
# TASK 1: Transaction Generator - SOLUTION
# ============================================================================
def generate_transactions(num_transactions, base_addr=0x1000):
    """
    Generate N transactions with specified address pattern.
    
    KEY POINTS:
    1. Use data pool for realistic transaction variety
    2. Alternate burst types using modulo arithmetic
    3. Dictionaries are perfect for transaction storage
    4. Address calculation uses arithmetic operators
    """
    
    # Data pool - realistic values for AXI transactions
    data_pool = [0xDEADBEEF, 0xCAFEBABE, 0x12345678, 0xABCDEF00, 0xFEDCBA00]
    
    # Burst type names
    burst_names = {0: "FIXED", 1: "INCR", 2: "WRAP"}
    
    transactions = []
    
    for i in range(num_transactions):
        # Address calculation: base + (transaction_id * stride)
        # Stride is 16 bytes (0x10) - common for 4-byte words
        addr = base_addr + (i * 0x10)
        
        # Alternate between INCR (odd) and FIXED (even) bursts
        burst_type_code = 1 if (i % 2) == 0 else 0
        burst_name = burst_names[burst_type_code]
        
        # Data cycling - use modulo to wrap around pool
        data = data_pool[i % len(data_pool)]
        
        # Transaction dictionary
        tx = {
            "tx_id": i,
            "addr": addr,
            "data": data,
            "burst_type": burst_name,
            "burst_code": burst_type_code,
            "write_strobe": 0xF,  # All bytes enabled
            "priority": 1,         # Normal priority
            "control_flags": 0x8,  # Valid bit set
        }
        
        transactions.append(tx)
    
    return transactions


# ============================================================================
# TASK 2: Control Word Encoder - SOLUTION
# ============================================================================
def encode_control_word(priority, burst_type, tx_id, write_strobe, control_flags):
    """
    Pack transaction fields into 16-bit control word.
    
    BIT LAYOUT:
    15 14 | 13 12 | 11 10 9 8 | 7 6 5 4 | 3 2 1 0
    priority | burst  | tx_id     | strobe  | flags
    
    BITWISE TECHNIQUE EXPLANATION:
    1. Shift each field to its position
    2. Use bitwise OR to combine (since no field overlaps)
    3. Mask inputs to ensure no overflow
    
    Example calculation:
    - priority=1 (01) → shift left 14 → 0100000000000000
    - burst=1 (01) → shift left 12 → 0001000000000000
    - tx_id=5 (0101) → shift left 8 → 0000010100000000
    - strobe=0xF (1111) → shift left 4 → 0000000011110000
    - flags=0x8 (1000) → shift left 0 → 0000000000001000
    - Result: OR all together → 0101010111111000 = 0x5578
    """
    
    # Ensure inputs don't exceed bit width
    priority = priority & 0x3        # Mask to 2 bits
    burst_type = burst_type & 0x3    # Mask to 2 bits
    tx_id = tx_id & 0xF              # Mask to 4 bits
    write_strobe = write_strobe & 0xF # Mask to 4 bits
    control_flags = control_flags & 0xF # Mask to 4 bits
    
    # Shift fields to their positions and combine with OR
    control_word = (priority << 14) | (burst_type << 12) | (tx_id << 8) | \
                   (write_strobe << 4) | control_flags
    
    return control_word


# ============================================================================
# TASK 3: Response Checker with Logging - SOLUTION
# ============================================================================
def setup_checker_logger(log_file="verif_exercise.log"):
    """
    Setup logger for response checker.
    
    LOGGING BEST PRACTICES:
    1. Named logger: "ResponseChecker" - identifies which component logged it
    2. Console: INFO and above - important messages only
    3. File: DEBUG and above - detailed analysis
    4. Uses FileHandler + StreamHandler (from Logging section)
    """
    
    logger = logging.getLogger("ResponseChecker")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()  # Clear any existing handlers
    
    # Console handler: INFO level and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)-8s | %(message)s'))
    
    # File handler: DEBUG and above for detailed logging
    log_path = Path(__file__).parent / log_file
    file_handler = logging.FileHandler(str(log_path), mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)-8s | %(message)s')
    )
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def check_response(expected_tx, received_tx, logger=None):
    """
    Compare expected vs received transaction.
    
    VERIFICATION TECHNIQUE:
    1. Compare each field individually
    2. Log each comparison at DEBUG (verbose detail)
    3. Log mismatches at ERROR (highlight problems)
    4. Collect comparison data for analysis
    
    DYNAMIC TYPING ADVANTAGE:
    - Both dicts have same keys but values can be different types
    - Python doesn't care about type, just equality
    - This flexibility is why Python rocks for rapid verification!
    """
    
    if logger is None:
        logger = setup_checker_logger()
    
    tx_id = expected_tx.get("tx_id", "?")
    logger.debug("Transaction %d comparison", tx_id)
    
    comparison_details = {}
    all_pass = True
    
    # Compare each field
    for key in expected_tx.keys():
        expected_val = expected_tx.get(key)
        received_val = received_tx.get(key, "MISSING")
        
        # Compare values
        match = (expected_val == received_val)
        comparison_details[key] = match
        
        # Log at appropriate level
        if match:
            # DEBUG for passing comparisons (verbose detail)
            if isinstance(expected_val, int) and expected_val > 0xFF:
                # For large values, use hex format
                logger.debug("  %15s: 0x%X == 0x%X ? PASS", 
                           key, expected_val, received_val)
            else:
                logger.debug("  %15s: %s == %s ? PASS",
                           key, expected_val, received_val)
        else:
            # ERROR for failures - easy to spot in logs
            all_pass = False
            logger.error("  MISMATCH in %s: expected=%s, received=%s",
                        key, expected_val, received_val)
    
    return (all_pass, comparison_details)


# ============================================================================
# TASK 4: Complete Test Sequence - SOLUTION
# ============================================================================
def run_verification_test():
    """
    Complete test sequence with controlled error injection.
    
    DESIGN PATTERN:
    1. Setup infrastructure (logging)
    2. Generate expected transactions
    3. Simulate DUT responses (include some errors)
    4. Compare and report
    5. Collect statistics for analysis
    
    TRICK FOR INTERVIEWS:
    - Show that you understand realistic testbenches have errors
    - Demonstrate how to systematically verify against them
    - Always track statistics (pass/fail counts)
    """
    
    logger = setup_checker_logger()
    logger.info("Starting verification test")
    
    # STEP 1: Generate expected transactions
    logger.info("Generating 5 transactions...")
    expected_transactions = generate_transactions(5)
    
    # STEP 2: Simulate DUT responses (some with errors)
    logger.info("Creating simulated DUT responses...")
    received_transactions = []
    
    for i, expected_tx in enumerate(expected_transactions):
        # Copy expected transaction (simulates DUT response)
        received_tx = expected_tx.copy()
        
        # Inject controlled errors for testing
        if i == 2:
            # Transaction 2: Data mismatch (common failure mode)
            received_tx["data"] = 0x99999999
            logger.info("  [Injected] Transaction %d: data error", i)
        elif i == 4:
            # Transaction 4: Address mismatch (different data width error)
            received_tx["addr"] = 0x2000
            logger.info("  [Injected] Transaction %d: address error", i)
        
        received_transactions.append(received_tx)
    
    # STEP 3: Run response checker on all transactions
    logger.info("Comparing transactions...")
    logger.info("=" * 60)
    
    stats = {"total": 0, "passed": 0, "failed": 0}
    
    for expected, received in zip(expected_transactions, received_transactions):
        stats["total"] += 1
        match, details = check_response(expected, received, logger)
        
        if match:
            stats["passed"] += 1
        else:
            stats["failed"] += 1
    
    # STEP 4: Report final statistics
    logger.info("=" * 60)
    logger.info("Test Statistics:")
    logger.info("  Total transactions: %d", stats["total"])
    logger.info("  Passed: %d", stats["passed"])
    logger.info("  Failed: %d", stats["failed"])
    
    # Calculate success rate
    if stats["total"] > 0:
        success_rate = 100.0 * stats["passed"] / stats["total"]
        logger.info("  Success rate: %.1f%%", success_rate)
        
        # Result verdict
        if stats["failed"] == 0:
            logger.info("VERDICT: ALL TESTS PASSED")
        else:
            logger.warning("VERDICT: %d TESTS FAILED - Review errors above", 
                          stats["failed"])
    
    return stats


# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    run_verification_test()
    print("\nCheck verif_exercise.log for detailed DEBUG output")
