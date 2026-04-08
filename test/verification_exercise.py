"""
VERIFICATION EXERCISE - DV Junior Interview Level

SCENARIO:
You are building a testbench for an AXI write transaction verification system.
Your task is to implement a stimulus generator and response checker that:

1. Generates multiple transactions with specific address patterns
2. Encodes control signals using bitwise operations
3. Verifies responses with proper logging and assertions
4. Handles edge cases and reports detailed status

REQUIREMENTS:

Task 1: Transaction Generator
===============================
Create a function that generates transactions with this specification:
- Base address: 0x1000
- Each transaction accesses a different address (increment by 16 bytes per transaction)
- Support burst patterns: FIXED (don't increment address), INCR (increment by 4)
- Generate N transactions based on input parameter

Example output format:
  Transaction 0: addr=0x1000, data=0xDEADBEEF, burst_type=INCR
  Transaction 1: addr=0x1010, data=0xCAFEBABE, burst_type=FIXED
  ...

Task 2: Control Word Encoder
=============================
Create a function that packs transaction fields into a single 16-bit control word:

Bit layout:
  [15:14] = priority (00=low, 01=normal, 10=high, 11=critical)
  [13:12] = burst_type (00=FIXED, 01=INCR, 10=WRAP, 11=reserved)
  [11:8]  = transaction_id (0-15)
  [7:4]   = write_strobe (0xF=all bytes, 0xA=even bytes, 0x5=odd bytes)
  [3:0]   = control flags (bit 3=valid, bit 2=last, bit 1=exclusive, bit 0=reserved)

Example: priority=01, burst=01, tx_id=5, strobe=0xF, flags=0x8 (valid+reserved)
Expected control_word = 0x____ (your job to calculate!)

Task 3: Response Checker with Logging
=======================================
Create a function that:
- Takes expected and received transaction dictionaries
- Logs each comparison at DEBUG level (use printf-style)
- Logs mismatches at ERROR level
- Returns True if all fields match, False otherwise
- Track match_count and fail_count

Use logging module with:
  - Logger name: "ResponseChecker"
  - Console output: INFO and above
  - File output: verif_exercise.log (DEBUG and above)

Task 4: Complete Test Sequence
===============================
Write a main test that:
1. Generates 5 transactions (mix of INCR and FIXED bursts)
2. Encodes control words for each
3. Simulate DUT response (modify some transactions to introduce errors)
4. Run response checker against all transactions
5. Print final statistics

HINTS (Don't look until you try!):
=============================
- Use dictionaries to store transaction fields
- Bit shifts and masks are your friends
- Test edge cases: All bytes enabled vs masked bursts
- Think about what happens when you try to set burst_type on a FIXED burst
- Consider data width calculations (32-bit bus vs 64-bit bus)

YOUR TASK:
===========
Write the complete implementation below. You can call functions in sequence
or create a class-based approach. Choose the style that makes sense to you.

"""

# ============================================================================
# YOUR CODE HERE - IMPLEMENTATION SECTION
# ============================================================================

# TASK 1: Transaction Generator
def generate_transactions(num_transactions, base_addr=0x1000):
    """
    Generate N transactions with specified address pattern.
    
    Parameters:
        num_transactions: How many transactions to generate
        base_addr: Starting address for transactions
    
    Returns:
        List of transaction dictionaries
    
    Specification:
    - Each transaction increments address by 16 bytes
    - Alternate between INCR and FIXED burst types
    - Data patterns: 0xDEADBEEF, 0xCAFEBABE, 0x12345678, 0xABCDEF00, 0xFEDCBA00
    """
    pass  # Your implementation here


# TASK 2: Control Word Encoder
def encode_control_word(priority, burst_type, tx_id, write_strobe, control_flags):
    """
    Pack transaction fields into 16-bit control word.
    
    Bit layout (revisited):
      [15:14] = priority (0-3)
      [13:12] = burst_type (0-3)
      [11:8]  = transaction_id (0-15)
      [7:4]   = write_strobe (0-15)
      [3:0]   = control_flags (0-15)
    
    Parameters:
        priority: 0-3 (2 bits)
        burst_type: 0=FIXED, 1=INCR, 2=WRAP, 3=reserved
        tx_id: 0-15 (4 bits)
        write_strobe: 0x0-0xF (4 bits)
        control_flags: 0x0-0xF (4 bits)
    
    Returns:
        16-bit control word (integer)
    
    HINT: Use bit shifts and bitwise OR to combine fields
    """
    pass  # Your implementation here


# TASK 3: Response Checker with Logging
def setup_checker_logger(log_file="verif_exercise.log"):
    """
    Setup logger for response checker.
    Returns configured logger object.
    """
    pass  # Your implementation here


def check_response(expected_tx, received_tx, logger=None):
    """
    Compare expected vs received transaction.
    Log all comparisons at DEBUG level.
    Log mismatches at ERROR level.
    
    Parameters:
        expected_tx: Expected transaction dict
        received_tx: Received transaction dict
        logger: Logger object (will create if None)
    
    Returns:
        (match: bool, comparison_details: dict)
    """
    pass  # Your implementation here


# TASK 4: Complete Test Sequence
def run_verification_test():
    """
    Complete test sequence:
    1. Generate 5 transactions
    2. Create simulated DUT responses (introduce controlled errors)
    3. Run response checker
    4. Report statistics
    """
    pass  # Your implementation here


# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    # Uncomment when ready:
    # run_verification_test()
    
    print("Exercise ready! Implement the functions above.")
    print("\nEXPECTED OUTPUT when complete:")
    print("=" * 60)
    print("INFO | Starting verification test")
    print("DEBUG | Transaction 0 comparison")
    print("DEBUG |   addr: 0x1000 == 0x1000 ? True")
    print("... (more comparisons)")
    print("ERROR | Transaction 2 MISMATCH: data expected=0x12345678, received=0x99999999")
    print("... (more results)")
    print("INFO | =================================================")
    print("INFO | Test Statistics:")
    print("INFO |   Total transactions: 5")
    print("INFO |   Passed: 4")
    print("INFO |   Failed: 1")
    print("INFO |   Success rate: 80.0%")
    print("=" * 60)
