import sys
import subprocess
import importlib.util

def install_package(package_name):
    """Installs a python package using pip from within Blender."""
    try:
        # Check if package is already installed
        if importlib.util.find_spec(package_name.replace("-", "_")):
            return True

        print(f"Installing {package_name}...")
        python_exe = sys.executable
        subprocess.check_call([python_exe, "-m", "pip", "install", package_name])
        return True
    except Exception as e:
        print(f"Failed to install {package_name}: {e}")
        return False

def ensure_dependencies():
    """Ensures all required dependencies are installed."""
    packages = ["google-generativeai", "pywebview"]
    success = True
    for pkg in packages:
        if not install_package(pkg):
            success = False
    return success
