# my_package/__init__.py
print("Initializing my_package...")

VERSION = "1.0.0"
AUTHOR = "zxc4we"

from .BrowserHelper import Helper
from .reg_gmx import gmxHelper

__all__ = ["Helper", "gmxHelper", "VERSION", "AUTHOR"]

def greet():
    print("Hello from my_package!")