# bootstrap.py
import sys
import subprocess
import importlib
import os


# ------------------------------------------------------------
# Detect if running inside VS Code
# ------------------------------------------------------------

def is_running_in_vscode() -> bool:
    return (
        "VSCODE_GIT_IPC_HANDLE" in os.environ
        or ("TERM_PROGRAM" in os.environ and "vscode" in os.environ["TERM_PROGRAM"].lower())
    )


# ------------------------------------------------------------
# Detect if SQLite Viewer extension is installed
# ------------------------------------------------------------

def is_sqlite_viewer_installed() -> bool:
    home = os.path.expanduser("~")
    ext_dir = os.path.join(home, ".vscode", "extensions")
    if not os.path.isdir(ext_dir):
        return False

    for folder in os.listdir(ext_dir):
        if folder.lower().startswith("qwtel.sqlite-viewer"):
            return True

    return False


def suggest_sqlite_viewer():
    print("\nSQLite Viewer Extension Check")
    print("-----------------------------")

    if not is_running_in_vscode():
        print("You are not running inside VS Code. Skipping extension check.\n")
        return

    if is_sqlite_viewer_installed():
        print("SQLite Viewer extension is already installed.\n")
        return

    print("The SQLite Viewer extension is not installed.")
    print("You can install it here:")
    print("  https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer\n")
    print("This extension lets you browse your env_explorer.db file directly inside VS Code.\n")


# ------------------------------------------------------------
# Dependency installer
# ------------------------------------------------------------

def ensure_package(pkg: str):
    try:
        importlib.import_module(pkg)
        return True
    except ImportError:
        print(f"Installing required package: {pkg}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            return True
        except Exception:
            print(f"Failed to install '{pkg}'. Please install it manually:")
            print(f"    pip install {pkg}")
            return False


# ------------------------------------------------------------
# Python version check
# ------------------------------------------------------------

def check_python_version():
    if sys.version_info < (3, 9):
        print("Python 3.9 or higher is required.")
        sys.exit(1)


# ------------------------------------------------------------
# Launch main program
# ------------------------------------------------------------

def run_main_program():
    if not os.path.exists("run.py"):
        print("Error: run.py not found in the current directory.")
        sys.exit(1)

    subprocess.call([sys.executable, "run.py"])


# ------------------------------------------------------------
# Main bootstrap logic
# ------------------------------------------------------------

def main():
    print("Bootstrapping EnviroStation CLI...\n")

    check_python_version()

    ok = True
    for pkg in ("requests", "rapidfuzz"):
        ok = ok and ensure_package(pkg)

    if not ok:
        sys.exit(1)

    suggest_sqlite_viewer()

    print("All checks passed. Launching program...\n")
    run_main_program()


if __name__ == "__main__":
    main()
