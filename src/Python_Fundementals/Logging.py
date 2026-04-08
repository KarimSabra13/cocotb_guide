"""
================================================================================
Python Logging Fundamentals for Hardware Verification
================================================================================

This module demonstrates the Python logging framework, a powerful alternative 
to print() for debugging and monitoring testbenches. Logging provides:
  - Multiple severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Flexible message formatting with contextual metadata
  - Handler infrastructure for simultaneous console and file output
  - Configurability without code changes via logging configuration

Key Advantages Over print():
  - Print is unstructured; logging provides timestamps, severity levels, and context
  - Print output is difficult to filter or redirect; logging supports multiple outputs
  - Print requires string concatenation which is error-prone; logging uses formatting
  - Print severity cannot be easily controlled; logging supports severity filtering

This code demonstrates logging configuration, formatting, and multi-handler output.
================================================================================
"""

import logging
import os
from pathlib import Path

# ============================================================================
# SECTION 1: LOGGING LEVELS AND SEVERITY FILTERING
# ============================================================================
"""
Python logging defines 5 standard severity levels (plus NOTSET):

  Level      Numeric Value    Typical Use Case
  -----      ---------------  ----------------------------------------
  NOTSET              0        Inherit from parent logger (advanced)
  DEBUG              10        Detailed diagnostic information (verification)
  INFO               20        General informational messages (test progress)
  WARNING             30        Warning messages (default root logger level)
  ERROR               40        Error conditions (test failures)
  CRITICAL            50        Critical errors (test aborted)

The logger acts as a FILTER: only messages at or above the configured
severity level are processed. Messages below the threshold are silently
discarded (no performance penalty).

Default root logger level is WARNING (30), so INFO and DEBUG messages
are suppressed by default.
"""

# Create a reference object to the root logger (default handler for all log())
root_logger = logging.getLogger()

# Set the root logger to DEBUG to capture all messages (we filter at the handler)
# This allows handlers to make their own severity decisions
root_logger.setLevel(logging.DEBUG)

# Example (commented): Set to INFO to suppress DEBUG messages
# root_logger.setLevel(logging.INFO)

# Demonstrate basic logging without custom formatting
print("\n" + "="*70)
print("DEMONSTRATION 1: Basic Logging with Default Format")
print("="*70)

logging.debug("This is a DEBUG message (detailed diagnostic)")
logging.info("This is an INFO message (general information)")
logging.warning("This is a WARNING message (something unexpected)")


# ============================================================================
# SECTION 2: CUSTOM FORMATTING AND BASICCONFIG
# ============================================================================
"""
logging.basicConfig() initializes the default handler with common settings.
It should be called BEFORE any log messages (typically at module start).

Format codes used in the 'format' string:
  %(levelname)s     - Severity level (DEBUG, INFO, WARNING, etc.)
  %(message)s       - The log message itself
  %(msecs)d         - Milliseconds portion of the timestamp
  %(asctime)s       - Human-readable timestamp (default format)
  %(name)s          - Logger name (helpful for multi-module logging)
  %(filename)s      - Source filename
  %(lineno)d        - Line number in source file
  %(funcName)s      - Function name where log was called
  %(process)d       - Process ID
  %(thread)d        - Thread ID

Note: After basicConfig() is called once, subsequent basicConfig() calls
are silently ignored. To reconfigure, create explicit Formatter/Handler objects.
"""

# Configure the ROOT logger with a custom format
logging.basicConfig(
    format='%(levelname)s: [TESTBENCH] %(message)s @ %(msecs)dms',
    level=logging.DEBUG
)

print("\n" + "="*70)
print("DEMONSTRATION 2: Logging with Custom Format")
print("="*70)

logging.info("This message includes custom formatting")
logging.warning("This message includes custom formatting")


# ============================================================================
# SECTION 3: PARAMETER SUBSTITUTION (Printf-style Formatting)
# ============================================================================
"""
The logging module supports three formatting styles:

1. %-formatting (Printf-style):  logging.info("x=%d", value)
2. str.format style:             logging.info("x={0}", value) 
3. f-string style:               logging.info(f"x={value}")

%-formatting is preferred in logging because:
  - Arguments are only formatted if the message will actually be logged
    (saving CPU when the level is filtered out)
  - f-strings eagerly evaluate, wasting CPU on suppressed messages
  
Example: If DEBUG is disabled, logging.debug("x=%d", expensive_calc())
will NOT call expensive_calc(), but f"x={expensive_calc()}" WILL.
"""

# Define test variables for demonstration
a = 3
b = 4
y = 7

print("\n" + "="*70)
print("DEMONSTRATION 3: Printf-style Parameter Substitution")
print("="*70)

# Decimal format: %d
logging.info("Decimal values: a = %d, b = %d, y = %d", a, b, y)

# String format: %s (with bin() to show binary representation)
logging.info("Binary values: a = %s, b = %s, y = %s", bin(a), bin(b), bin(y))

# String format: %s (with hex representation)
logging.info("Hex values: a = %s, b = %s, y = %s", hex(a), hex(b), hex(y))

# Multiple format types in one message
logging.info("Mixed formats: decimal=%d, binary=%s, hex=%s", a, bin(b), hex(y))


# ============================================================================
# SECTION 4: MULTIPLE HANDLERS (CONSOLE + FILE OUTPUT)
# ============================================================================
"""
A Logger can have multiple HANDLERS, each responsible for a different output.
Common handlers:
  - StreamHandler:    Output to console (stdout or stderr)
  - FileHandler:      Output to a file
  - RotatingFileHandler: File output with automatic rotation (size/time-based)
  - SMTPHandler:      Send log entries via email (for production systems)
  - HTTPHandler:      Send logs to a web server

Each handler can have its own:
  - Formatter:        Custom format string
  - Level:            Minimum severity to process (handler-level filtering)

This allows different verbosity levels to different outputs.
For example: Console shows INFO+, File shows DEBUG+.
"""

print("\n" + "="*70)
print("DEMONSTRATION 4: File and Console Handlers")
print("="*70 + "\n")

# Create a dedicated logger for this section (instead of using root logger)
file_logger = logging.getLogger("FileDemo")
file_logger.setLevel(logging.DEBUG)

# Remove any existing handlers to avoid duplicates
file_logger.handlers.clear()

# CONSOLE HANDLER: Print to console with custom format
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO and above to console
console_format = logging.Formatter(
    '%(levelname)-8s | %(message)s'
)
console_handler.setFormatter(console_format)
file_logger.addHandler(console_handler)

# FILE HANDLER: Write to log file with detailed format
log_dir = Path(__file__).parent
log_file = log_dir / "testbench.log"

file_handler = logging.FileHandler(str(log_file), mode='w')
file_handler.setLevel(logging.DEBUG)  # ALL levels to file
file_format = logging.Formatter(
    '[%(asctime)s] %(levelname)-8s | %(message)s | [%(funcName)s:%(lineno)d]'
)
file_handler.setFormatter(file_format)
file_logger.addHandler(file_handler)

# Log messages demonstrate handler-level filtering
file_logger.debug("This DEBUG message goes ONLY to file (INFO threshold blocks console)")
file_logger.info("This INFO message goes to BOTH console and file")
file_logger.warning("This WARNING message goes to BOTH console and file")

print(f"\nLog file written to: {log_file}")
print("Check the file to see DEBUG message that was filtered from console.\n")


# ============================================================================
# SECTION 5: PRACTICAL PATTERNS FOR HARDWARE VERIFICATION
# ============================================================================
"""
Best practices for verification logging:

1. Use module-level loggers:
   logger = logging.getLogger(__name__)
   
2. Log at appropriate levels:
   - DEBUG: Signal/register changes, low-level operations
   - INFO:  Test phase transitions, key milestones
   - WARNING: Assertions near threshold, suspicious patterns
   - ERROR: Test failures, unexpected conditions
   - CRITICAL: Simulation abort conditions

3. Include context in messages:
   - Use parameter substitution for values (allows filtering)
   - Include operation scope (testcase name, interface, etc.)
   
4. Avoid logging in tight loops:
   - Log is slower than inline computation
   - Pre-aggregate data before logging summary statistics
"""

print("\n" + "="*70)
print("DEMONSTRATION 5: Verification-Style Logging Pattern")
print("="*70 + "\n")

verification_logger = logging.getLogger("HardwareVerification")
verification_logger.setLevel(logging.DEBUG)
verification_logger.handlers.clear()

# Verification console handler
verify_console = logging.StreamHandler()
verify_console.setLevel(logging.DEBUG)
verify_format = logging.Formatter(
    '[%(name)s] %(levelname)s: %(message)s'
)
verify_console.setFormatter(verify_format)
verification_logger.addHandler(verify_console)

# Simulate testbench operations
verification_logger.info("Testbench initialization started")
verification_logger.debug("Clock frequency set to %d MHz", 100)
verification_logger.debug("Reset signal asserted")
verification_logger.info("Reset released; beginning stimulus application")

# Simulate transaction logging
tx_data = [0xDEADBEEF, 0xCAFEBABE, 0x12345678]
verification_logger.info("Transmitting %d transactions", len(tx_data))
for i, data in enumerate(tx_data):
    verification_logger.debug("Transaction %d: data=0x%08X", i, data)

verification_logger.info("All transactions completed successfully")

print("\n" + "="*70)
