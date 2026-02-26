# run_tests.py
import os
import sys
import subprocess
import platform

def ensure_pytest():
    """Install pytest if missing."""
    try:
        import pytest
        return True
    except ImportError:
        print("pytest not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
            return True
        except Exception as e:
            print("Failed to install pytest:", e)
            return False


def run_pytest(args=None):
    """Run pytest with optional arguments."""
    cmd = [sys.executable, "-m", "pytest"]
    if args:
        cmd.extend(args)
    subprocess.call(cmd)


def menu():
    print("\n=== EnviroStation Test Runner ===")
    print("1) Run ALL tests")
    print("2) Run OFFLINE tests only")
    print("3) Run ONLINE tests only")
    print("4) Exit")

    choice = input("Select an option: ").strip()

    if choice == "1":
        run_pytest()
    elif choice == "2":
        run_pytest(["-m", "not online"])
    elif choice == "3":
        run_pytest(["-m", "online"])
    else:
        print("Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    print(f"Detected OS: {platform.system()}")

    if not ensure_pytest():
        sys.exit(1)

    menu()
