# test_all.py
"""
Runs both offline and online tests.
"""

import subprocess
import sys

print("\n=== OFFLINE TESTS ===\n")
subprocess.call([sys.executable, "test_offline.py"])

print("\n=== ONLINE TESTS ===\n")
subprocess.call([sys.executable, "test_online.py"])

print("\nAll tests complete.\n")
